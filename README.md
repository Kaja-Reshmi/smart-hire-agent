# SMART HIRE — AI Job Search Agent

An AI-powered job search and recommendation platform built with Python and FastAPI. SMART HIRE helps candidates discover suitable job opportunities, understand their skill matches, analyze resumes, and track job applications.

## Features

- **Job Search:** Search jobs by title, company, location, and skills.
- **Skill Matching:** Calculate job-match scores and identify matched, related, and missing skills.
- **Job Recommendations:** Get personalized job recommendations based on candidate skills and preferences.
- **Resume Analysis:** Upload a PDF or DOCX resume to extract and analyze relevant information.
- **Application Tracking:** Save jobs, update application statuses, and add notes.
- **Dashboard:** View application statistics and track your job search progress.
- **Sample Job Dataset:** Explore 500 sample job listings stored in SQLite.

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **API Server:** Uvicorn
- **Resume Processing:** PDF and DOCX text extraction
- **Version Control:** Git and GitHub

## Project Structure

```text
smart-hire-agent/
├── frontend/
│   └── index.html
├── agent.py
├── applications.py
├── database.py
├── main.py
├── matching.py
├── resume_parser.py
├── resume_upload.py
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Kaja-Reshmi/smart-hire-agent.git
cd smart-hire-agent
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic python-multipart
```

Install any additional dependencies required by your project if needed.

### 4. Start the backend

```bash
uvicorn main:app --reload
```

Open the API documentation at:

http://127.0.0.1:8000/docs

### 5. Start the frontend

Open a second terminal in the project directory and run:

```bash
python3 -m http.server 5500 --directory frontend
```

Open the application at:

http://127.0.0.1:5500

Keep both terminal sessions running while using the application.

## How It Works

1. Search the available job listings or enter your skills.
2. Review job-match scores and personalized recommendations.
3. Upload a resume to analyze its contents.
4. Identify missing skills and areas for improvement.
5. Save suitable jobs and track application progress.

## Important Note

The current job listings are sample data and should not be treated as verified live vacancies. Resume analysis and recommendations depend on the project's implemented matching and parsing logic.

## Future Improvements

- Integration with verified live job listings.
- More advanced semantic resume-to-job matching.
- Enhanced recommendation models.
- Deployment to a cloud platform.
- Additional career guidance and analytics.

## Author

**Kaja Reshmi**

GitHub: [@Kaja-Reshmi](https://github.com/Kaja-Reshmi)

---

If you find this project useful, consider giving the repository a star!
