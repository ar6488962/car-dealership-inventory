"""Promote an existing local account to administrator.

Usage from the backend directory:
    python -m app.admin --email admin@example.com
"""

import argparse
import sys

from sqlalchemy import select

from app.database import SessionLocal
from app.models import User


def promote(email: str) -> int:
    normalized_email = email.strip().lower()
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == normalized_email))
        if user is None:
            print(f"No account found for {normalized_email}. Register it first.", file=sys.stderr)
            return 1
        if user.role == "admin":
            print(f"{normalized_email} is already an administrator.")
            return 0
        user.role = "admin"
        db.commit()
        print(f"Promoted {normalized_email} to administrator.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote an existing account to administrator.")
    parser.add_argument("--email", required=True, help="Email address of the existing account")
    args = parser.parse_args()
    return promote(args.email)


if __name__ == "__main__":
    raise SystemExit(main())
