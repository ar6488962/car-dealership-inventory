# Test Report

## Latest backend test run

- Command: `..\.venv\Scripts\python.exe -m pytest -q` (run from `backend/`)
- Location: `backend/`
- Result: **20 passed, 1 warning**
- Runtime: 7.01 seconds
- Environment used for this run: Python 3.14.0, package versions from `backend/requirements.txt`
- Database for test cases: temporary in-memory SQLite via SQLAlchemy `StaticPool` (the application itself defaults to persistent file-backed SQLite and supports PostgreSQL).

## Covered cases

- Registration succeeds and does not expose password hashes.
- Duplicate email registration is rejected.
- Login returns a bearer token and rejects an incorrect password.
- Short passwords are rejected.
- Vehicle listing returns an empty list initially.
- Vehicle creation requires admin access.
- Unauthenticated vehicle creation is rejected.
- Search filters by make and price.
- Purchase decreases stock and records a purchase.
- Out-of-stock purchases are rejected.
- Regular users cannot restock or delete vehicles.
- Admin restocking and deletion work for eligible vehicles.
- Vehicle updates require authentication.
- Invalid bearer tokens are rejected.
- Registration cannot escalate a user to admin through an extra request field.
- Blank vehicle update fields are rejected.
- Missing-vehicle update, purchase and restock operations return `404`.
- Admin deletion is rejected with `409` after purchase history exists.
- Restock rejects zero and negative quantities.

## Frontend verification

- Command: `npm run build` (run from `frontend/`)
- Result: **success**
- Vite output: 1,937 modules transformed; production bundle generated in `frontend/dist/`.
- Frontend unit-test command: not configured in this project. Important UI behavior was reviewed through the build and API integration code; add a browser test runner if the assessment requires automated frontend tests.

## Other checks

- Admin bootstrap CLI: `..\.venv\Scripts\python.exe -m app.admin --help` — success.
- Pylance diagnostics for changed Python and JSX files — no errors.
- Docker Compose/PostgreSQL — not run in this environment; Docker availability and container startup remain unverified.
- Browser smoke check — Vite served the application at `http://127.0.0.1:5173/`, the API health endpoint returned `200`, and the empty inventory state rendered from the backend response.
- Screenshot — `screenshots/inventory-empty-state.png` captured from that running application. Authenticated/admin screenshots were not captured.
- This report records observed commands and results only; it does not claim that the historical code was developed through a verified Red-Green-Refactor commit sequence.

## TDD history

There was no pre-existing local Git history available to verify a historical Red-Green-Refactor sequence. The additional tests in this review were added before the corresponding fixes were validated, but this submission does not manufacture historical commits or claim that earlier work followed a verifiable TDD sequence.
