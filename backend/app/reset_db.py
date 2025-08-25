from app.core.database import engine, Base
from app.models import *

def reset_database():
    print("Resetting all tables...")
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)
    print("Database recreated.")

if __name__ == "__main__":
    reset_database()