# 🧠 Project Summary
This repository contains a full-stack web application that allows users to compare a resume to a job posting. It intelligently analyzes the match between a candidate's resume and job requirements, making it easier to tailor resumes for better chances of success.

# Authors
Shobhit Rajain
Navjot Kaur
Benjamin Ramos-Armstrong
Michael Tettey Tamatey
Izaak Ford Dow

# The project is split into two parts:

Frontend – Resume_comparator_frontend (built with React.js)
Backend – ResumeComparatorBackend (built with Django & NLP tools)

# 🚀 Getting Started
1. Clone the Repository

# ⚙️ Prerequisites
Visual Studio Code
PyCharm (optional for backend)
Node.js and npm
Python 3.11

# 📁 Project Structure
📦 Resume Comparator
├── Resume_comparator_frontend
└── ResumeComparatorBackend


# 🖥️ Frontend Setup (React)
Open the Resume_comparator_frontend folder in VS Code.
Open a terminal and run:
npm install
npm run dev
Your frontend should now be running locally.

# 🔧 Backend Setup (Django + NLP)
You can use either VS Code or PyCharm for the backend.
Open the ResumeComparatorBackend folder.
Open a terminal and run the following:

# 💻 Create and Activate Virtual Environment
On macOS/Linux:
python3.11 -m venv .venv
source .venv/bin/activate

On Windows:
py -3.11 -m venv .venv
.venv\Scripts\activate

# 📦 Install Requirements
pip install -r requirements.txt
pip install spacy-transformers
python -m spacy download en_core_web_sm
pip install django djangorestframework djangorestframework-simplejwt
pip install httpx
pip install python-dotenv
pip install llama-cpp-python

# 🔐 Environment Variables
Create a .env file in the root of the ResumeComparatorBackend folder and add your API key as follows:
API_KEY=your_api_key_here
⚠️ The API key will be provided separately.

# ▶️ Run the Backend
python manage.py runserver
The backend server should now be running and connected to your frontend.

# ✅ All Set!
Once both frontend and backend are running, your Resume Comparator web app is ready to use!
