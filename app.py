from __future__ import annotations

import json
import os
from io import BytesIO
from typing import Any

import streamlit as st
from docx import Document
from google import genai
from pypdf import PdfReader

APP_TITLE = "Resume ATS Reviewer"
MODEL_NAME = "gemini-3.8-flash"
MAX_UPLOAD_MB = 10
MAX_RESUME_CHARS = 30_000

st.set_page_config(page_title=APP_TITLE, page_icon="📄", layout="wide")


def get_api_key() -> str | None:

    try:
        secret_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        secret_key = ""
    return secret_key or os.getenv("GEMINI_API_KEY") or None


def extract_resume_text(uploaded_file: Any) -> str:
    
    raw = uploaded_file.getvalue()
    suffix = uploaded_file.name.rsplit(".", 1)[-1].lower() if "." in uploaded_file.name else ""

    if suffix == "pdf":
        reader = PdfReader(BytesIO(raw))
        text_parts = [(page.extract_text() or "") for page in reader.pages]
        text = "\n".join(text_parts)
    elif suffix == "docx":
        document = Document(BytesIO(raw))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        table_text = [cell.text for table in document.tables for row in table.rows for cell in row.cells]
        text = "\n".join(paragraphs + table_text)
    elif suffix == "txt":
        text = raw.decode("utf-8", errors="replace")
    else:
        raise ValueError("Unsupported file type. Upload a PDF, DOCX, or TXT file.")

    text = text.strip()
    if not text:
        raise ValueError(
            "No readable text was found. If this is a scanned/image-only PDF, use an OCR-enabled version or upload a text-based PDF/DOCX."
        )
    return text[:MAX_RESUME_CHARS]


def build_prompt(resume_text: str, job_description: str) -> str:
    job_context = job_description.strip() or "No job description supplied. Assess general resume quality and ATS-readiness."
    return f"""You are a careful resume reviewer. Review the resume for ATS-readiness and useful improvements.

Important rules:
- The score is an ESTIMATE for guidance, not a real score from any specific ATS vendor.
- Judge only job-relevant skills, experience, evidence, clarity, and formatting. Do not infer or score age, gender, race, religion, disability, nationality, or other protected/personal traits.
- Never invent qualifications, employment, education, metrics, or skills. Suggestions must be truthful and conditional where facts are missing.
- If a job description is supplied, assess alignment with it. If not, assess general ATS-readiness.
- Give practical, specific, constructive feedback. Do not guarantee interviews or hiring outcomes.
- Return valid JSON only, matching this schema exactly. Scores must be integers. Overall score and each category score must be between 0 and 100.

JSON schema:
{{
  "overall_score": 0,
  "score_label": "Needs work | Fair | Good | Strong",
  "summary": "short overall assessment",
  "score_breakdown": [
    {{"category": "Keyword alignment", "score": 0, "max_score": 100, "feedback": "..."}},
    {{"category": "Experience and achievements", "score": 0, "max_score": 100, "feedback": "..."}},
    {{"category": "Skills relevance", "score": 0, "max_score": 100, "feedback": "..."}},
    {{"category": "Structure and readability", "score": 0, "max_score": 100, "feedback": "..."}},
    {{"category": "ATS-friendly formatting", "score": 0, "max_score": 100, "feedback": "..."}}
  ],
  "strengths": ["..."],
  "improvements": [
    {{"priority": "High | Medium | Low", "action": "specific action", "why": "why it helps", "example": "truthful example or template; do not invent facts"}}
  ],
  "keywords_to_consider": ["keywords supported by the job description or clearly relevant to the role"],
  "formatting_notes": ["..."],
  "rewritten_summary": "A suggested professional summary using only facts present in the resume; if insufficient facts, provide a fill-in template instead."
}}

JOB DESCRIPTION:
{job_context[:12_000]}

RESUME TEXT:
{resume_text}


def parse_json_response(response_text: str) -> dict[str, Any]:
    """Parse model JSON, tolerating an occasional Markdown code fence."""
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError("The model response was not a JSON object.")

    score = data.get("overall_score")
    if not isinstance(score, (int, float)):
        raise ValueError("The model response did not include a numeric overall_score.")
    data["overall_score"] = max(0, min(100, int(round(score))))

    for key in ("strengths", "improvements", "keywords_to_consider", "formatting_notes", "score_breakdown"):
        if not isinstance(data.get(key), list):
            data[key] = []
    return data


def review_resume(api_key: str, resume_text: str, job_description: str) -> dict[str, Any]:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=build_prompt(resume_text, job_description),
        config={"response_mime_type": "application/json"},
    )
    if not getattr(response, "text", None):
        raise RuntimeError("Gemini returned an empty response. Please try again.")
    return parse_json_response(response.text)


def safe_text(value: Any, fallback: str = "Not provided.") -> str:
    return str(value).strip() if value is not None and str(value).strip() else fallback


st.title("📄 Resume ATS Reviewer")
st.write(
    "Upload a resume to get an AI-estimated ATS-readiness score, strengths, and prioritized improvements. "
    "Optionally add a job description for a more targeted review."
)
st.info(
    "**Important:** This is an AI-generated estimate, not an official score from an applicant tracking system. "
    "Different employers and ATS products evaluate resumes differently."
)

with st.sidebar:
    st.header("How it works")
    st.markdown(
        "1. Upload a PDF, DOCX, or TXT resume.\n"
        "2. Optionally paste the job description.\n"
        "3. Get a score estimate and improvement plan."
    )
    st.caption(f"AI model: `{MODEL_NAME}`")
    st.caption("Uploads are processed for this review and are not saved by this app to a database.")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx", "txt"],
    help=f"Maximum file size: {MAX_UPLOAD_MB} MB. Text-based PDFs work best.",
)
job_description = st.text_area(
    "Job description (optional)",
    placeholder="Paste the target role's job description here for a targeted review...",
    height=180,
)

if uploaded_file is not None and uploaded_file.size > MAX_UPLOAD_MB * 1024 * 1024:
    st.error(f"The file is too large. Please upload a file smaller than {MAX_UPLOAD_MB} MB.")
    st.stop()

if st.button("Analyze resume", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.warning("Please upload a resume first.")
        st.stop()

    api_key = get_api_key()
    if not api_key:
        st.error(
            "Gemini API key not found. Add `GEMINI_API_KEY` to Streamlit Secrets, "
            "or set it as an environment variable when running locally. See README.md."
        )
        st.stop()

    try:
        with st.spinner("Reading your resume and reviewing it with Gemini…"):
            resume_text = extract_resume_text(uploaded_file)
            results = review_resume(api_key, resume_text, job_description)
        st.session_state["review_results"] = results
        st.session_state["review_filename"] = uploaded_file.name
    except ValueError as exc:
        st.error(str(exc))
        st.stop()
    except Exception as exc:
        # Keep user-facing errors helpful without exposing secrets or request internals.
        st.error(
            "The review could not be completed. Check that your Gemini API key is valid, "
            "the model is available to your account, and your internet connection is working. "
            f"Technical detail: {type(exc).__name__}: {exc}"
        )
        st.stop()

results = st.session_state.get("review_results")
if results:
    st.divider()
    st.subheader(f"Results for: {st.session_state.get('review_filename', 'Resume')}")
    left, right = st.columns([1, 2])
    with left:
        st.metric("Estimated ATS-readiness", f"{results['overall_score']}/100")
        st.progress(results["overall_score"] / 100)
        st.caption(safe_text(results.get("score_label"), "AI estimate"))
    with right:
        st.markdown("#### Overall assessment")
        st.write(safe_text(results.get("summary")))

    breakdown = results.get("score_breakdown", [])
    if breakdown:
        st.markdown("### Score breakdown")
        for item in breakdown:
            if not isinstance(item, dict):
                continue
            category = safe_text(item.get("category"), "Category")
            score = item.get("score", 0)
            try:
                score = max(0, min(100, int(score)))
            except (TypeError, ValueError):
                score = 0
            st.markdown(f"**{category}: {score}/100**")
            st.progress(score / 100)
            st.caption(safe_text(item.get("feedback")))

    tab_strengths, tab_improvements, tab_keywords, tab_summary = st.tabs(
        ["Strengths", "Improvements", "Keywords & format", "Suggested summary"]
    )
    with tab_strengths:
        strengths = results.get("strengths", [])
        if strengths:
            for item in strengths:
                st.markdown(f"- {item}")
        else:
            st.write("No strengths were returned. Try analyzing again.")
    with tab_improvements:
        improvements = results.get("improvements", [])
        if improvements:
            for index, item in enumerate(improvements, start=1):
                if not isinstance(item, dict):
                    continue
                priority = safe_text(item.get("priority"), "Priority not set")
                st.markdown(f"#### {index}. {safe_text(item.get('action'))}  ·  {priority}")
                st.write(safe_text(item.get("why")))
                example = item.get("example")
                if example and str(example).strip():
                    st.markdown("**Example / template**")
                    st.write(example)
        else:
            st.write("No improvement items were returned. Try analyzing again.")
    with tab_keywords:
        st.markdown("#### Keywords to consider")
        keywords = results.get("keywords_to_consider", [])
        st.write(", ".join(str(k) for k in keywords) if keywords else "No keywords suggested.")
        st.markdown("#### Formatting notes")
        notes = results.get("formatting_notes", [])
        if notes:
            for note in notes:
                st.markdown(f"- {note}")
        else:
            st.write("No formatting notes returned.")
    with tab_summary:
        st.write(safe_text(results.get("rewritten_summary")))
        st.caption("Check every statement for accuracy before using it in your resume.")

    st.download_button(
        "Download review as JSON",
        data=json.dumps(results, indent=2, ensure_ascii=False),
        file_name="resume_review.json",
        mime="application/json",
    )
