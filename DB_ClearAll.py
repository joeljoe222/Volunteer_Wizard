#WARNING RUNNING THIS WILL CLEAR AND RESET ALL DATABASES
from app import app
from models import db

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Database cleared and recreated")
