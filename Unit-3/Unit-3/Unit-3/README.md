# Enterprise Smart Library Management Platform

A database-backed Flask starter project based on the uploaded Unit 3 reference: DevOps, version control, CI/CD, containerization, and deployment. The reference identifies the library domain entities as books, borrowers, inventory, loans, and overdue fines, and names Python, Flask, Pytest, Jenkins, Docker, and Minikube as target technologies. This starter implements core book, borrower, and loan workflows; fines, login/roles, and production monitoring are not implemented.

## Features
- Add and browse books, with unique ISBN and copy-count validation
- Register borrowers, with unique email
- Record book loans and due dates
- Record returns and update available-copy counts
- Show overdue loans
- SQLite relational database and schema file
- Pytest tests, Jenkins pipeline example, Docker/Compose, Kubernetes Deployment and NodePort Service manifests

## Database
SQLite is used by default. `database.py` opens the database and `schema.sql` creates the `books`, `borrowers`, and `loans` tables. The `library.db` file is generated automatically when the app starts and is excluded from Git. The schema is committed, so another developer can recreate the structure.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create a virtual environment: `python -m venv .venv`
4. Activate it on Windows PowerShell: `.\\.venv\\Scripts\\Activate.ps1` (macOS/Linux: `source .venv/bin/activate`)
5. Install packages: `pip install -r requirements.txt`
6. Start the app: `python app.py`
7. Open `http://127.0.0.1:5000`

## Run tests
Run `pytest -q`.

## Run with Docker Compose
Run `docker compose up --build`, then open `http://localhost:5000`. The database is stored in a named Docker volume.

## Minikube / Kubernetes
The `deployment.yaml` file is an educational example using image `library-platform:v1.0.0`. Build/tag that image and make it available to your Minikube environment before applying the manifest. For durable data, configure a PersistentVolume or use a managed database; the current manifest does not mount persistent storage.

## Git workflow suggested by the reference
Use short-lived feature branches and Pull Requests, for example `feature/book-catalog`, then merge reviewed and tested changes to `main`. Configure Jenkins and a GitHub webhook separately; the included Jenkinsfile demonstrates checkout, dependency installation, syntax validation, and Pytest execution.

## Limitations
This is an academic starter, not a production-ready enterprise system. Authentication, authorization, fines calculation/payment, robust transaction locking, backups, secrets management, monitoring, and production-grade persistent Kubernetes storage need further work. Replace the development Flask secret before deployment.
