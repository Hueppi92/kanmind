# KanMind Backend

KanMind is a Django REST Framework backend for the KanMind task-management application. The frontend is maintained in a separate repository.

## Features

- Token-based registration and login
- Board and task CRUD APIs
- Assigned-task and reviewer-task lists
- Task comments
- Django admin for boards, tasks, and comments

## Requirements

- Python 3.13 (the pinned Django version is 6.1.1)
- Git
- The separate frontend repository only when testing the complete application

## Installation

Run these commands from the repository root in PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
```

Start the development server:

```powershell
python manage.py runserver
```

The API is served at `http://127.0.0.1:8000/`. The Django admin is at `http://127.0.0.1:8000/admin/`.

Create an administrator account when needed:

```powershell
python manage.py createsuperuser
```

## Authentication

Registration and login are public. All other API endpoints require a DRF token. Send the token in the request header:

```http
Authorization: Token <token>
```

### Register

`POST /api/registration/`

Request:

```json
{
	"fullname": "Ada Lovelace",
	"email": "ada@example.com",
	"password": "example-password",
	"repeated_password": "example-password"
}
```

Success returns `201 Created` with `token`, `user_id`, `email`, and `fullname`. The password must contain at least eight characters, the full name must include at least two words, and the repeated password must match.

### Log in

`POST /api/login/`

Request:

```json
{
	"email": "ada@example.com",
	"password": "example-password"
}
```

Success returns `200 OK` with `token`, `user_id`, `email`, and `fullname`.

### Check an email

`GET /api/email-check/?email=ada%40example.com`

Requires authentication. Returns `200 OK` with the matching user's `id`, `email`, and `fullname`, or `404 Not Found` if no account matches.

## API Endpoints

All paths below are relative to `http://127.0.0.1:8000`. Unless marked public, send the token authentication header described above. JSON request bodies should use `Content-Type: application/json`.

### Boards

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/boards/` | List boards visible to the authenticated user | Owner or member |
| `POST` | `/api/boards/` | Create a board | Authenticated |
| `GET` | `/api/boards/{board_id}/` | Retrieve a board | Owner or member |
| `PUT`, `PATCH` | `/api/boards/{board_id}/` | Update a board | Owner or member |
| `DELETE` | `/api/boards/{board_id}/` | Delete a board | Owner only |

Board fields are `id`, `owner`, `title`, `members`, and `member_count`. The owner is assigned from the authenticated user; `owner` and `member_count` are read-only. A create request can provide a title and, optionally, member IDs.

### Tasks

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/tasks/` | List tasks on boards the user owns or belongs to | Owner or member |
| `POST` | `/api/tasks/` | Create a task | Board member |
| `GET` | `/api/tasks/{task_id}/` | Retrieve a task | Owner or member |
| `PUT`, `PATCH` | `/api/tasks/{task_id}/` | Update a task | Board member |
| `DELETE` | `/api/tasks/{task_id}/` | Delete a task | Task creator or board owner |
| `GET` | `/api/tasks/assigned-to-me/` | List tasks assigned to the user | Authenticated |
| `GET` | `/api/tasks/reviewing/` | List tasks where the user is reviewer | Authenticated |

Task request fields include `board` (board ID), `title`, `description`, `status`, `priority`, `due_date`, `assignee_id`, and `reviewer_id`. `status` supports `to-do`, `in-progress`, `review`, and `done`; `priority` supports `low`, `medium`, and `high`. The response includes task IDs and nested assignee/reviewer details. A task's board cannot be changed through updates.

Example create request:

```json
{
	"board": 1,
	"title": "Prepare release notes",
	"description": "Summarize the changes for this release.",
	"status": "to-do",
	"priority": "medium",
	"due_date": "2026-10-15",
	"assignee_id": 2,
	"reviewer_id": 3
}
```

### Comments

| Method | Path | Description | Access |
| --- | --- | --- | --- |
| `GET` | `/api/tasks/{task_id}/comments/` | List comments for a task | Board member |
| `POST` | `/api/tasks/{task_id}/comments/` | Add a comment | Board member |
| `DELETE` | `/api/tasks/{task_id}/comments/{comment_id}/` | Delete a comment | Comment author |

Create a comment with a JSON body containing `content`. The author is taken from the authenticated user. Creation returns `201 Created`; deletion returns `204 No Content`. Comment responses contain `id`, `created_at`, `author`, and `content`.

## Permissions and Status Codes

- `201 Created`: registration, board/task creation, or comment creation succeeded.
- `200 OK`: a read or update succeeded.
- `204 No Content`: a deletion succeeded.
- `400 Bad Request`: request data failed validation.
- `401 Unauthorized`: authentication is missing or invalid.
- `403 Forbidden`: the authenticated user does not have permission.
- `404 Not Found`: the requested resource does not exist or is not visible to the user.

Board owners and members can access board details. Task creation and updates require board membership; only the creator or board owner can delete a task. Comment operations require board membership, and only the comment author can delete a comment.

## Checks and Tests

Run Django's checks and the available test suite:

```powershell
python manage.py check
python manage.py test
python -m pip install pycodestyle
python -m pycodestyle core manage.py
```

The pycodestyle configuration in `setup.cfg` checks maintained Python code with a 79-character line limit and excludes Django-generated migrations.

## Project Structure

```text
core/
	auth_app/       Registration, login, and email lookup API
	boards_app/     Board models, API, permissions, and admin
	tasks_app/      Task/comment models, API, permissions, and admin
	settings.py     Django and DRF settings
	urls.py         Root URL configuration
manage.py         Django command-line entry point
requirements.txt  Pinned Python dependencies
```

Each app keeps its API views, serializers, URLs, and permissions in its `api/` directory.

## Frontend Integration

Start this backend, then configure the separately maintained frontend to use `http://127.0.0.1:8000` as its API base URL.

## Database and Deployment Notes

The local development database is SQLite at `db.sqlite3`. The database, virtual environments, environment files, logs, Python caches, and local frontend files are excluded from Git and must not be committed.

The checked-in Django settings are for local development only (`DEBUG` is enabled and the secret key is defined in the settings file). Before deployment, move secrets to environment variables, rotate the development key, set `DEBUG` to `False`, configure `ALLOWED_HOSTS`, and use a production database. Never publish credentials or production secret keys.

## License

This project is intended for the Developer Akademie course environment and is not intended for unrestricted redistribution.
