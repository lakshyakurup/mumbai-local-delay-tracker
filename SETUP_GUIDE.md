# Setup & Installation Guide

Follow these instructions to set up, run, and deploy the **Mumbai Local Train Delay Tracker** locally on your development machine.

## Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- Git & GitHub Desktop
- Visual Studio Code

## 1. Clone the Repository
```bash
git clone https://github.com/lakshyakurup/mumbai-local-delay-tracker.git
cd mumbai-local-delay-tracker
```

## 2. Backend Setup (Python & FastAPI)
```bash
cd backend
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## 3. Frontend Setup (Next.js)
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
Access the dashboard locally at `http://localhost:3000`.
