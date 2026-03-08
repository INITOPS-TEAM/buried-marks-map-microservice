# Map microservice on MariaDB

This microservice gets requests via Django REST API and serves such methods according to provided in `permissions.py` user permissions basing on `user_role` .
The general flow is:

1. Getting user roles from JWT
2. Converting custom roles to permissions in classes that inherit from `BasePermission`
3. For specific view actions, check if user has required permissions

To get more details please refer to the [Custom permissions
 section](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions) of Django REST framework Documentation.

## Variables

Variables should be included in `.env` file.
File with examples provided `.env.example`

## JWT

Unified token should be used for well-coordinated application flow.
In this case microservice uses `algorithms=['ES256']` which requires to set public key `JWT_PUBLIC_KEY` in `settings.py`.

## WSGI

Application is served via WSGI server using `config/wsgi.py`.
For production use Gunicorn instead of Django development server.

## API Endpoints

| Method | Endpoint                   | Permission | Description         |
|--------|----------------------------|------------|---------------------|
| GET    | /api/markers/              | viewer+    | List all markers    |
| POST   | /api/markers/              | editor+    | Create marker       |
| DELETE | /api/markers/{id}/         | admin      | Delete marker       |
| POST   | /api/markers/{id}/confirm/ | viewer+    | Confirm marker      |
| DELETE | /api/markers/{id}/confirm/ | viewer+    | Remove confirmation |
| POST   | /api/markers/{id}/image/   | editor+    | Upload image to S3  |
| GET    | /api/categories/           | viewer+    | List categories     |
| POST   | /api/categories/           | admin      | Create category     |

## AWS S3

Images are stored in AWS S3. Required variables in .env:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`

## Running locally

1. Start MariaDB `buried-marks-maria-db` container: `docker compose up -d`.
2. Create venv: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`.
3. If you changed `models.py`, run `python manage.py makemigrations`.
4. Run migrations: `python manage.py migrate`.
5. Start server: `python manage.py runserver`.

## Tests

Run all tests:
```bash
make test
```

Run specific test suites:
```bash
make test-markers
```

```bash
make test-confirmations
```

```bash
make test-permissions
```

Tests use SQLite in-memory database and mocked AWS S3 via `moto` - no external dependencies required.

## Code Quality

### Automated Linting & Formatting

GitHub Actions workflow runs on every pull request and push:

- **markdownlint**: Markdown formatting
- **Prettier**: Code formatting (JS, JSON, YAML, Markdown)
- **CSpell**: Spell checking
- **Black & isort** - Python formatting
- **Pylint** - Python linting (fail under 7.5)
- **Gitleaks** - Secret scanning.
  To enable Gitleaks pre-commit hooks locally, install Gitleaks following [the official installation guide.](https://github.com/gitleaks/gitleaks#installing)

Most checks run as warnings. **Pylint failures will block the merge** - fix syntax errors before merging.
