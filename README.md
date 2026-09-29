# KanMind Backend

This repository contains the Django backend for the KanMind frontend. The frontend is maintained separately and is intentionally not part of this repository.

## Current Status

The backend provides authentication, board, and task APIs. Task endpoints include assigned/reviewing lists and task comments. Authenticated endpoints use token authentication.

## Requirements

- Python 3.13 or a compatible Python version supported by Django 6.1
- Git
- The separate KanMind frontend repository, when testing frontend integration

## Setup

From the repository root, create and activate a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the pinned dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Create the local database and apply migrations:

```powershell
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

The backend is then available at `http://127.0.0.1:8000/`. The Django admin is available at `http://127.0.0.1:8000/admin/`.

Create an admin user when needed:

```powershell
python manage.py createsuperuser
```

## Testing and Checks

Run Django's system checks and the test suite with:

```powershell
python manage.py check
python manage.py test
```

## Project Structure

```text
core/
	auth/       Authentication API
	boards/     Board models and API
	tasks/      Task and comment models and API
	settings.py Django settings
	urls.py     Root URL configuration
manage.py     Django command-line entry point
requirements.txt
```

## Frontend Integration

The frontend is kept in a separate repository. Run this backend first, then configure the frontend's API base URL to point to the local server.

## Database and Local Files

The development SQLite database is created locally as `db.sqlite3`. Database files, virtual environments, environment files, logs, Python caches, and local frontend files are ignored by Git and must never be committed to GitHub.

For production, use environment variables for secrets and a production database instead of the local SQLite database. Never publish credentials or secret keys.

## License

This project is intended for the Developer Akademie course environment and is not intended for unrestricted redistribution.
