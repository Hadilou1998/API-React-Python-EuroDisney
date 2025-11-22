import os
import sys

# --- Permet d'exécuter le script depuis n'importe où ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from app.core.database import engine, Base
from app.models import *
from app.seed import seed


def reset_database():
    print("Resetting database...")

    # 1. Drop all tables
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")

    # 2. Re-create all tables
    Base.metadata.create_all(bind=engine)
    print("All tables recreated.")

    # 3. Seed database
    print("Seeding database...")
    seed()

    print("Database reset + seed completed successfully!")


if __name__ == "__main__":
    reset_database()