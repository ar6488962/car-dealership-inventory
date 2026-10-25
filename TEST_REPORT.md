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
20 passed, 1 warning in 7.01s
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

There is no frontend unit-test command in this project. Frontend behavior was checked with the build, code diagnostics, real API checks, and a browser smoke check. This is not the same as automated frontend tests.

## Other checks

- The admin help command worked:
  `..\.venv\Scripts\python.exe -m app.admin --help`
- Changed Python and JSX files had no editor diagnostics.
- The API health check returned HTTP 200.
- The frontend opened at `http://127.0.0.1:5173/`.
- The empty inventory page showed data from the backend.
- A real API vehicle was created, purchased, restocked, and deleted in the earlier smoke test.
- The browser showed the new stock after a purchase.
- The screenshot in `screenshots\inventory-empty-state.png` is a real capture from the running app.

## Not tested

- Docker Compose was not run.
- PostgreSQL was not run.
- No frontend automated test runner is configured.
- No authenticated or admin screenshot is included.
- The old work does not have enough commit history to prove a complete Red-Green-Refactor process. The current commits do not pretend otherwise.
