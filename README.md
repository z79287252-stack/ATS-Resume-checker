# ATS-Resume-checker

hi

Hi! 😊 How are you doing today?

What would you like to study or discuss today? I'm ready to help you! 💪


I want to create an app in which user will upload a resume and the app will tell the ATS score and the improvements in the resume. I will use streamlit for Ul. I will use Gemini flash model for Al models. Give me three files app.py, readme and requirement.txt and make sure to review and test it before you give me code. Also tell me how to push on github using Ul and dploy it on streamlit.

use gemini 3.8 flash model

I've prepared your Resume ATS Reviewer app using Streamlit for the UI and Google's Gemini 3.8 Flash for AI-powered resume analysis.

The app is designed for beginners and includes the three project files, setup instructions, GitHub upload instructions, and Streamlit deployment steps.

I've also checked the Python syntax and tested several important helper functions. The live Gemini API integration still needs to be tested with your own API key.

1. Download your three project files
You can download each file separately or download the complete project as a ZIP.

Complete project
Recommended: Download all three files together.

📦 

Individual files
File	Purpose	Download
app.py	Main application and AI integration	
README.md	Installation, GitHub, and deployment instructions	
requirements.txt	Python dependencies	
Important: You mentioned requirement.txt. I've used requirements.txt instead because this is the standard filename recognized by Streamlit Community Cloud.

2. What will your app do?
The application will have the following features.

Feature 1: Upload a resume
Users can upload their resumes in these formats:

PDF

DOCX

TXT

The app extracts the text from the uploaded file and sends it for analysis.

Feature 2: Calculate an estimated ATS score
The app displays an estimated score out of 100.

For example:

Estimated ATS-readiness score: 78/100

The score breakdown covers:

Category	What it evaluates
Keyword alignment	Relevant keywords for the target job
Experience and achievements	How clearly experience and achievements are presented
Skills relevance	How relevant the listed skills are
Structure and readability	Organization and clarity
ATS-friendly formatting	Potential formatting and readability problems
These are AI-generated estimates, not scores calculated by a real employer's ATS.

Feature 3: Identify improvements
The app provides:

Resume strengths.

Problems that need attention.

High-, medium-, and low-priority improvements.

Relevant keywords to consider.

Formatting recommendations.

A suggested professional summary.

Users can also paste a job description to receive more targeted recommendations.

Feature 4: Download the results
Users can download their analysis as a JSON file for future reference.

3. Which AI model does it use?
Your application is configured to use Gemini 3.8 Flash, with the model ID:

gemini-3.8-flash

This is the model identifier listed in Google's official documentation. 

Official documentation: Gemini 3.8 Flash documentation

The app uses Google's google-genai Python SDK to communicate with the model.

How the application works
The basic process is:

A user uploads a resume.

Python extracts its text.

The user optionally supplies a job description.

The app sends the relevant text to Gemini.

Gemini returns structured analysis.

Streamlit displays the score and recommendations.

The user can download the results.

4. How to run the app on your computer
Since you're using a computer, follow these steps.

Step 1: Extract the ZIP
Download the ZIP file above and extract it.

Your folder should look like this:

resume_ats_app/
│
├── app.py
├── README.md
└── requirements.txt
Step 2: Open the folder in your code editor
Open the folder using VS Code or another Python editor.

Open the terminal in that folder.

Step 3: Install the dependencies
Run:

pip install -r requirements.txt
This installs Streamlit, the Gemini SDK, and the document-reading libraries.

Step 4: Obtain a Gemini API key
Visit Google AI Studio and create an API key.

Keep your key private.

For local testing in Windows PowerShell, run:

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
Replace YOUR_GEMINI_API_KEY with your actual key.

Do not put your API key directly into app.py or upload it to GitHub.

Step 5: Start the application
Run:

streamlit run app.py
Streamlit will provide a local address, usually:

http://localhost:8501

Open that address in your browser.

Your app should now display its resume-upload interface.

5. How to upload your project to GitHub using the website UI
You don't need to use Git commands for this method.

Step 1: Open GitHub
Visit GitHub and sign in.

Step 2: Create a repository
Click the + icon in the upper-right corner.

Select New repository.

Enter this repository name:

resume-ats-reviewer

Choose Public or Private.

Click Create repository.

Step 3: Upload app.py
On your new repository page:

Click Add file.

Select Create new file.

Enter app.py as the filename.

Open your downloaded app.py locally.

Copy its entire contents.

Paste the contents into GitHub's editor.

Click Commit changes.

Step 4: Upload the other files
Repeat the same process for:

README.md

requirements.txt

When you're finished, your repository should contain:

resume-ats-reviewer/
│
├── app.py
├── README.md
└── requirements.txt
Security reminder: Never upload your API key or a file containing your secrets.

6. How to deploy your app on Streamlit Community Cloud
Once your code is on GitHub, you can publish the application online.

Step 1: Open Streamlit Community Cloud
Visit Streamlit Community Cloud.

Sign in using your GitHub account and authorize access if requested.

Step 2: Create an app
Click Create app.

Select your GitHub repository.

Choose the main branch.

Set the main file path to:

app.py

Open Advanced settings.

Step 3: Configure your API key
In the Secrets field, enter:

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
Replace the placeholder with your real API key.

Do not commit this secret to GitHub.

Step 4: Deploy
Click Deploy.

Streamlit will install the dependencies listed in requirements.txt and start your application. Once deployment finishes, it will provide a public application address.

You can find the official instructions in the Streamlit deployment guide.

7. Testing and review
Here is what I checked before preparing the files.

Test	Result
Python syntax compilation	Passed
TXT resume extraction helper	Passed
JSON response parsing	Passed
Handling of Markdown-formatted JSON	Passed
Score boundaries	Passed
Prompt construction	Passed
Missing-value fallback helper	Passed
Live Gemini API call	Not tested
Full browser-based Streamlit run	Not tested
Deployment on Streamlit Cloud	Not tested
The untested items require installing the application's dependencies and, for the Gemini API test, configuring a valid API key.

Two important limitations
1. The ATS score is an estimate.

Different applicant tracking systems evaluate resumes differently. Your application provides AI-assisted guidance rather than reproducing the scoring system of a particular employer.

2. Scanned PDFs may not work.

The current version extracts selectable text from PDFs. It does not include OCR for image-only or scanned resumes.

Also, resume text is sent to Google's Gemini API for analysis. Users should avoid uploading confidential resumes unless they have permission and are comfortable with the applicable service terms.

My recommendation
Start by running the app locally before uploading it to GitHub. Upload a sample resume, add a sample job description, and check whether the feedback is useful and accurate.

Once that works, deploy it on Streamlit Community Cloud.

Your next milestone: Get the application running locally with your Gemini API key. After that, you can focus on improving the interface, adding resume comparisons, and eventually introducing additional features such as resume rewriting and downloadable PDF reports.





give it to me step by step

Library
/
README.md



Resume ATS Reviewer
A Streamlit app that reads a resume and uses Google's Gemini 3.8 Flash (gemini-3.8-flash) to estimate ATS-readiness, identify strengths, and recommend practical improvements. A job description is optional but makes the review more targeted.

Important: The score is an AI estimate for guidance, not an official score from an ATS product. ATS tools and employers use different parsing and screening rules. Always verify that suggested edits accurately describe your real experience.

Features
Accepts text-based PDF, DOCX, and TXT resumes.

Optional job description for role-specific keyword and experience alignment.

Overall score estimate plus category-level feedback.

Prioritized improvements, strengths, suggested keywords, formatting notes, and a suggested professional summary.

Download the review as JSON.

Uses Streamlit Secrets or an environment variable for the API key; the key is not hard-coded.

Files
resume-ats-reviewer/
├── app.py
├── README.md
└── requirements.txt
Streamlit Community Cloud expects the dependency file to be named requirements.txt (plural), so keep that exact filename.

1. Get a Gemini API key
Open Google AI Studio and create an API key.

Keep the key private. Do not paste it into app.py, README.md, or a public GitHub repository.

The app uses the model ID gemini-3.8-flash. Model availability and quotas depend on your Google account and API access.

2. Run locally
Use Python 3.10 or newer (Python 3.12 is a good choice).

Windows PowerShell
cd path\to\resume-ats-reviewer
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
streamlit run app.py
Replace YOUR_GEMINI_API_KEY with your real key. Keep that command and key private. The environment variable applies to the current PowerShell session.

macOS / Linux
cd path/to/resume-ats-reviewer
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
streamlit run app.py
Streamlit will print a local address, usually http://localhost:8501.

3. Push the files to GitHub using the website UI
Sign in to GitHub.

Click + (top-right) → New repository.

Name it resume-ats-reviewer. Choose Public or Private, then click Create repository.

On the new repository page, choose Add file → Create new file.

Enter app.py as the filename, paste in the complete contents of your local app.py, and commit the file.

Repeat Add file → Create new file for README.md and requirements.txt, pasting each file's contents and committing.

Check that all three files appear in the repository's root directory.

Never upload your API key or a .streamlit/secrets.toml file to GitHub. If a key is accidentally committed, revoke it and create a new one.

4. Deploy on Streamlit Community Cloud
Open Streamlit Community Cloud and sign in with GitHub.

Connect/authorize your GitHub account if prompted.

Click Create app and select your resume-ats-reviewer repository, branch (usually main), and main file path app.py.

Open Advanced settings before deploying. In the Secrets field, add:

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
Replace the placeholder with your real key. Do not include the key in any repository file.

Select a supported Python version if needed, then click Deploy.

Wait for the build to finish. Open the generated *.streamlit.app address and test with a non-sensitive sample resume.

To update the app later, edit the files on GitHub and commit the changes. Community Cloud detects repository updates and redeploys the app.

Official guides: Deploy an app · Secrets management

Troubleshooting
API key not found: check the environment variable locally or the app's Streamlit Cloud Secrets setting.

Invalid key / permission / model error: confirm the key is active, the Gemini API is enabled for the associated project, and gemini-3.8-flash is available to your account.

No text extracted: the PDF may be scanned or image-only. Upload a text-based PDF or DOCX; OCR is not included in this starter version.

Dependency/build error: verify the file is named requirements.txt and is in the same repository root as app.py.

Privacy and limitations
The app does not write uploaded resumes to a database or local file. Resume text is sent to the Gemini API for analysis, so do not upload confidential or third-party resumes unless you have permission and are comfortable with the applicable service terms. The app limits uploads to 10 MB and sends at most 30,000 characters of extracted resume text to the model. Scanned PDF OCR, multilingual-specific scoring, and real ATS vendor integrations are not included.

