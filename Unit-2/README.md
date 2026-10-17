# Student Record and Academic Management Platform

A starter Flask web application based on the Unit-2 Agile Mini-Project brief. It provides basic student and course records, attendance entry, and marks entry using a local SQLite database.

## Features
- Dashboard with record counts
- Add and list students; delete students
- Add and list courses
- Record and view attendance
- Enter and view marks (0–100)
- Simple responsive interface
- Starter Docker, Docker Compose, Jenkins, and Kubernetes files

## Requirements
- Python 3.10 or newer

## Run locally (optional)
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

The database is created automatically as `students.db` when the app starts. This is a learning/demo starter, not a production-ready system. Authentication, password reset, role-based access, editing records, and production database configuration are not implemented yet.

## Agile scope notes
Suggested epics: Student Management, Course Management, Attendance Management, Marks and Academic Performance, Authentication and Security, Notifications, and Reporting. This starter implements basic student/course/attendance/marks workflows; the remaining epics can be planned as future user stories and sprints.
