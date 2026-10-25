# Test Report

This file lists checks that were really run. It does not claim that checks were run when they were not.

## Backend tests

Command:

```powershell
cd backend
..\.venv\Scripts\python.exe -m pytest -q
```

Result:

```text
20 passed, 1 warning in 11.78s
```

The tests ran with Python 3.14.0. They use a temporary in-memory SQLite database. They do not use the real local database file.

The warning is an existing Starlette/httpx deprecation warning. It did not fail any test.

The tests cover:

- User registration.
- Duplicate email addresses.
- Login and bad passwords.
- Short passwords.
- Invalid tokens.
- Attempts to register as an admin.
- Vehicle listing and search.
- Admin-only vehicle creation.
- Signed-in vehicle updates.
- Blank update values.
- Missing vehicles.
- Purchases and stock decrease.
- Purchases when stock is zero.
- Admin-only restocking.
- Invalid restock amounts.
- Admin-only deletion.
- Deletion after a purchase history exists.

## Frontend build

Command:

```powershell
cd frontend
npm run build
```

Result: **Success**.

Vite transformed 1,937 modules and created the production files in `frontend\dist\`. The build folder is ignored by Git.

Frontend behavior was also checked with the automated tests below, real API checks, and a browser smoke check.

## Frontend automated tests

Command:

```powershell
cd frontend
npm test
```

Result: **3 passed**.

The tests check vehicle search, the disabled purchase button when stock is zero, and stock refresh after a successful purchase. The tests use Vitest and React Testing Library.

## Other checks

- The admin help command worked:
  `..\.venv\Scripts\python.exe -m app.admin --help`
- Changed Python and JSX files had no editor diagnostics.
- The API health check returned HTTP 200.
- The frontend opened at `http://127.0.0.1:5173/`.
- The empty inventory page showed data from the backend.
- A real API vehicle was created, purchased, restocked, and deleted in the earlier smoke test.
- The browser showed the new stock after a purchase.
- The screenshots in `screenshots\inventory-empty-state.png` and `screenshots\admin-inventory.png` are real captures from the running app.

## Not tested

- Docker Compose was not run.
- PostgreSQL was not run.
- The old work does not have enough commit history to prove a complete Red-Green-Refactor process. The current commits do not pretend otherwise.

## Final assignment check

| Requirement | Status | Notes |
|---|---|---|
| Backend API | Done | FastAPI routes cover login, users, vehicles, search, purchase, restock, and health check. |
| Persistent database | Done | SQLite works by default. PostgreSQL support is in the settings but was not tested. |
| Login and token security | Done | Passwords are hashed. JWT tokens are checked and expire. |
| Admin permissions | Done | Admin creation, restock, delete, and vehicle creation are protected. |
| React frontend | Done | The page uses React, Vite, CSS, and the real backend API. |
| Search and filters | Done | Make, model, category, minimum price, and maximum price are supported. |
| Purchase and stock rules | Done | Stock decreases safely. Empty stock is rejected. |
| Backend tests | Done | 20 tests passed with 1 warning. |
| Frontend automated tests | Done | 3 Vitest tests passed. |
| Docker/PostgreSQL check | Not tested | Docker and PostgreSQL were not run. |
| Real screenshots | Done | Empty inventory and admin inventory screenshots are real browser captures. |
| Admin or signed-in screenshots | Done | The admin inventory panel screenshot was captured from a signed-in admin session. |
| AI usage section | Done | README explains the tools and the work they helped with. |
| Full raw AI chat evidence | Missing | PROMPTS.md has genuine excerpts only. Add the full export or a checked public link. |
| Personal reflection | Done | A personal reflection is present in README. |
| Public GitHub repository | Done | The project is pushed to the `main` branch. |
