# Library Management System

A simple library management project built with Python, Flask, and MySQL, with DevOps examples using Docker, Docker Compose, Jenkins, and Kubernetes YAML.

## Files
- `app.py` — Flask application with home, book list, add-book, and health routes.
- `schema.sql` — MySQL database and sample book records.
- `Dockerfile` — builds the Flask app image.
- `docker-compose.yml` — runs the app and MySQL database.
- `Jenkinsfile` — example CI pipeline.
- `deployment.yaml` — example Kubernetes Deployment and Service.
- `templates/` — HTML pages.
- `static/style.css` — page styling.

## Important
Never commit real passwords or secret keys. For Docker Compose, create a local `.env` file with `DB_PASSWORD`, `MYSQL_ROOT_PASSWORD`, and `FLASK_SECRET_KEY`. Do not upload `.env` to GitHub.

This repository is an educational template. The Kubernetes and Jenkins files are examples and require a configured environment to run.
