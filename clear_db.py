#WARNING RUNNING THIS WILL CLEAR ALL DATABASES
from app import app, db

with app.app_context():
    # Drop all tables
    db.drop_all()
    # Recreate all tables
    db.create_all()
    print("Database cleared and recreated.")
