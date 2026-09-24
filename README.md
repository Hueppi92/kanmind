# KanMind Backend

This repository contains the Django backend for the KanMind frontend. The frontend is maintained separately and is intentionally not part of this repository.

## Current Status

The project is currently a Django 6.1.1 backend foundation. The database models, authentication flow, board API, and task API still need to be implemented and connected to the separate frontend. At the moment, Django's default admin route is the only registered application route.

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
KanMind/
	auth/       Authentication app
	boards/     Board app
	tasks/      Task app
	settings.py Django settings
	urls.py     Root URL configuration
manage.py     Django command-line entry point
requirements.txt
```

The `auth`, `boards`, and `tasks` apps are currently scaffolds for the backend implementation.

## Frontend Integration

The frontend is kept in a separate repository. Run this backend first, then configure the frontend's API base URL to point to the local server. API routes will be added as the backend implementation progresses.

## Database and Local Files

The development SQLite database is created locally as `db.sqlite3`. Database files, virtual environments, environment files, logs, Python caches, and local frontend files are ignored by Git and must never be committed to GitHub.

For production, use environment variables for secrets and a production database instead of the local SQLite database. Never publish credentials or secret keys.

## License

This project is intended for the Developer Akademie course environment and is not intended for unrestricted redistribution.
