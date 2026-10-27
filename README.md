# RheinClean Gebäudeservice

A demonstration website for a **fictional** cleaning company in Duisburg. It is a portfolio project: a German public site in Vue 3 and a FastAPI API that stores quote requests in SQLite and shows them in a protected admin area.

Nothing on the site is a real business. There is no street address, tax number, company register entry, staff list, award, or customer review. Legal pages are placeholders and must be rewritten before any public deployment.

## Stack

- Frontend: Vue 3, TypeScript, Vite, Vue Router, Tailwind CSS
- Backend: Python 3.12+, FastAPI, Pydantic v2, SQLAlchemy 2, SQLite, Argon2
- Tests: pytest and Vitest

Pinia is not used. The short admin session lives in an HTTP-only cookie, not in the browser storage.

## Run it locally

Use two terminals. Python 3.12 or newer is required (3.13 works).

```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Edit `.env` and set `SECRET_KEY` and `ADMIN_PASSWORD` (at least 12 characters, not a common word). Then create the tables and the only administrator. There is no signup page.

```bash
python -m app.cli create-admin
uvicorn app.main:app --reload
```

The API documentation is at http://127.0.0.1:8000/docs while `ENVIRONMENT` is not `production`.

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173. The dev server proxies `/api` to the API, so the session cookie stays on one origin.

## What you can click through

- Home, services, about, quote form, impressum placeholder, privacy placeholder, and a 404 page.
- The quote form posts to `POST /api/v1/quote-requests` and shows a reference such as `RC-7K2M9Q4P`. Sending the form does not create an order.
- Sign in at http://127.0.0.1:5173/admin/login with the email and password from `.env`.
- The dashboard lists, filters, and pages enquiries. Open one to change its status or delete it.

Enquiry statuses: Neu, Kontaktiert, Angebot erstellt, Abgeschlossen, Abgelehnt.

## Authentication

The API sets two cookies:

- `rc_session` is HTTP-only and expires after one hour. It holds a signed id, not a password.
- `rc_csrf` is readable by the page. Changing requests must send the same value in `X-CSRF-Token`.

Passwords are hashed with Argon2. A wrong login and a missing account return the same message. Login is limited to 5 attempts per 15 minutes per address, and the public form to 5 submissions per 10 minutes. The limit is kept in memory, so it resets when the API process restarts. That is enough for this demo and is not a substitute for a shared limiter in production.

The cookie `Secure` flag is off for local HTTP. Set `COOKIE_SECURE=true` only behind HTTPS.

## Personal data

Quote requests store the name, email, message, and the optional phone, company, area, and date. The success response returns only the public reference. Application logs do not include the message or the email. Access logs can still contain a search term typed into the admin search box.

There is no legally claimed retention period. Delete a single enquiry in the admin detail view, or remove older rows from the `backend` directory:

```bash
RETAIN_DAYS=365 python -m app.cli purge-enquiries
```

Choose the number yourself. The command does not claim that 365 days is required by law.

## Tests

```bash
cd backend && .venv/bin/pytest
cd frontend && npm test
```

The API tests use an in-memory SQLite database and do not touch `backend/data/rheinclean.db`.

## Production notes

Before this could be a real site it needs HTTPS, a secret manager, database backups, monitoring, a reviewed Impressum and privacy policy, and a decision about how long enquiries are kept. Do not deploy the placeholder legal pages. The pages send `noindex` so a demo host is not presented to search engines as a trading company.

Schema changes currently use `create_all` at startup. That creates missing tables and does not migrate existing columns. For a real database, add Alembic before changing the models.
