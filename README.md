# Motorstock — Car Dealership Inventory System

A full-stack car dealership inventory kata built for the Incubyte Software Craftsperson Intern assessment. It includes a React single-page application, FastAPI REST API, persistent SQL database, token authentication, role-based permissions, inventory operations, and automated backend tests.

> **Assessment honesty note:** This repository was prepared with AI assistance. Review the implementation, run it locally, understand the code, and update this README with your actual test results and development experience before submission. Do not claim a historical Red-Green-Refactor commit history unless you actually create it.

## Features

- Register and log in with password hashing and JWT access tokens.
- Public vehicle listing and search by make, model, category, minimum price and maximum price.
- Authenticated vehicle updates and purchases.
- Admin-only vehicle creation, deletion and restocking. Public registration always creates a regular user; it does not accept a role from the client.
- Persistent users, vehicles and purchase records. SQLite is the easy local default; PostgreSQL is supported through `DATABASE_URL`.
- Atomic conditional stock decrement to prevent overselling the last unit.
- React SPA with responsive layouts, filters, login/register, purchase actions and admin inventory controls.
- Backend tests for authentication, authorization, search, purchases and restocking.

## Technology

- Backend: Python, FastAPI, SQLAlchemy, Pydantic, PyJWT
- Database: SQLite by default; PostgreSQL supported
- Frontend: React, Vite, HTML5, CSS3 and Tailwind CSS
- Tests: pytest and FastAPI TestClient

## Requirements

- Python 3.11+ recommended
- Node.js 20+ and npm
- Git
- Optional: Docker Desktop, if you want PostgreSQL via Docker Compose

## Run locally (SQLite — simplest path)

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Windows PowerShell: Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`; interactive API documentation is at `http://localhost:8000/docs`. The SQLite database file is created in `backend/dealership.db`.

### 2. Frontend (new terminal)

```bash
cd frontend
npm install
cp .env.example .env.local  # Windows PowerShell: Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:5173`. The frontend calls the API at `http://localhost:8000` by default.

## Run with PostgreSQL

From the project root, start PostgreSQL: `docker compose up -d db`. Then set `DATABASE_URL` in `backend/.env` to:

```env
DATABASE_URL=postgresql+psycopg://dealership:dealership_local_password@localhost:5432/dealership
JWT_SECRET=replace-with-a-long-random-secret
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Install backend requirements and run Uvicorn as above. Never use the sample database password or development JWT secret in a public deployment.

## Authentication and admin access

Registration creates a `user` account. Admin access is not granted by passing a role during registration. The supported local bootstrap command promotes an already-registered account without accepting a password or creating an unexpected user:

```powershell
cd backend
..\.venv\Scripts\python.exe -m app.admin --email admin@example.com
```

The command is idempotent and fails if the account does not exist. Do not expose public admin promotion functionality.

After login, the frontend stores only the bearer token and non-sensitive user profile in localStorage for this assessment demo; it never stores passwords. A `401` response clears the session and asks the user to sign in again. For production systems, consider a secure HttpOnly cookie, refresh-token strategy, rate limiting, audit logging, migrations and stricter deployment hardening.

## API overview

| Method | Endpoint | Access | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Register a user |
| POST | `/api/auth/login` | Public | Receive JWT |
| GET | `/api/vehicles` | Public | List vehicles |
| GET | `/api/vehicles/search` | Public | Filter inventory |
| POST | `/api/vehicles` | Admin | Add vehicle |
| PUT | `/api/vehicles/{id}` | Authenticated | Update vehicle |
| DELETE | `/api/vehicles/{id}` | Admin | Delete vehicle if no purchase history exists |
| POST | `/api/vehicles/{id}/purchase` | Authenticated | Purchase one unit |
| POST | `/api/vehicles/{id}/restock` | Admin | Add stock |
| GET | `/api/health` | Public | Health check |

Example search: `/api/vehicles/search?make=Toyota&min_price=5000&max_price=50000`. Vehicle prices in the sample UI are displayed as USD; the assignment does not specify a currency, so adjust the UI/seed data if your evaluator expects another currency.

## Test-driven development workflow

The intended cycle for each feature is **Red → Green → Refactor**:

1. Add one focused failing test before implementing a behavior.
2. Run it and capture the failure.
3. Implement the smallest change that passes.
4. Run the test again.
5. Refactor, rerun the suite and commit the change with a descriptive message.

Run the backend tests:

```bash
cd backend
pytest -v
```

Optional coverage report (install `pytest-cov` first): `pytest --cov=app --cov-report=term-missing -v`. Record actual output in `TEST_REPORT.md`. The test suite uses a temporary SQLite test database and does not require a running PostgreSQL server.

On Windows PowerShell with the repository virtual environment:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -v
```

Build the frontend:

```powershell
cd frontend
npm run build
```

## Git and AI co-authorship

Commit small changes with descriptive messages. For each commit where AI contributed, add the co-author trailer required by the assessment and identify the actual tool used. Example format:

```text
test: add vehicle search cases

Used ChatGPT to brainstorm edge cases, then reviewed and adjusted the tests.

Co-authored-by: ChatGPT <AI@users.noreply.github.com>
```

Follow the assignment's required two blank lines before the trailer. This project bundle does not pretend to contain a verified, historical TDD commit sequence. Establish and document your own real Red-Green-Refactor commits as you review and work through the code.

## My AI Usage

### Tools used
- ChatGPT (OpenAI), for requirements breakdown, architecture discussion, drafting initial implementation files, test ideas, UI scaffolding and documentation.
- Copilot SDK in VS Code, for the verification pass, targeted backend/frontend fixes, regression tests, documentation updates, runtime API/browser checks and submission preparation.

### How I used AI
- I used ChatGPT to organise the assessment into backend, database, authentication, frontend, testing and documentation tasks.
- I used it to draft an initial code structure and suggest backend test cases for authentication, permissions, search and inventory.
- I used it to help create a responsive UI and explain how the frontend communicates with the REST API.
- I am responsible for reviewing the generated code, running it, fixing problems and making sure I can explain the final implementation.
- In this verification pass, I reviewed the existing implementation, removed the frontend demo-data path, added session-expiry handling and an admin bootstrap CLI, added regression tests, ran the application, exercised the real API and browser flow, and recorded only observed results.

### Reflection
AI helped accelerate the initial structure and the later verification work, but generated code still required review, tests, runtime checks and corrections. I verified the final behavior against the local API and browser rather than assuming the implementation was correct.

> Personal reflection placeholder: [Add your own reflection about what you learned and what you would improve before submission.]

## PROMPTS.md and raw prompt logs

See [`PROMPTS.md`](./PROMPTS.md). The assessment asks for raw, unedited AI chat logs or public chat links, not summaries. Keep the original prompts and responses you actually used, and add the remaining raw conversation content or a share link you have checked. Do not label a summary as a raw log.

## Screenshots

Save screenshots of the running application in `screenshots/` and embed them here, for example:

```markdown
![Vehicle dashboard](screenshots/vehicle-dashboard.png)
![Admin inventory](screenshots/admin-inventory.png)
```

Captured from the running Vite application with the backend connected and an empty persistent inventory:

![Inventory empty state](screenshots/inventory-empty-state.png)

Capture additional authenticated/admin screenshots before submission if you want to demonstrate those flows; do not use mock or generated screenshots.

## Deployment

Deployment is optional. Before deploying, configure a production database, a strong secret, CORS origins, HTTPS and platform environment variables. Never commit `.env` files.
