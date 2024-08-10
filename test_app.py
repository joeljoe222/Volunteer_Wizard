import pytest
from app import app, db, User, Event, Notification, Skill, State
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    #Setup a test client for the Flask application
    app.config['TESTING'] = True
    with app.test_client() as client:
        '''
        with app.app_context():
            db.create_all()
            # Add sample data to the database here


            sample_user = User(
                email='testuser@example.com',
                password=generate_password_hash('password123'),
                role='volunteer',
                name='Test User',
                address='123 Main St',
                state_id=1,
                preferences='Preference',
                availability='Monday, Wednesday'
            )

            sample_event = Event(
                name='Sample Event',
                description='Sample Description',
                urgency='Medium',
                address='123 Event St',
                city='cityz',
                zipcode='12345',
                state_id=1,
                user_id=1
            )

            db.session.add(sample_user)
            db.session.add(sample_event)
            db.session.commit()
            '''
        yield client


def test_home(client):
    #Test the home page
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the home page!" in response.data


def test_login(client):
    #Test user login
    response = client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome back, Test User!" in response.data


def test_register(client):
    #Test user registration
    response = client.post('/register', data={'email': 'newuser@example.com', 'password': 'newpassword123', 'role': 'volunteer'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"User added, please finish setting up." in response.data

def test_event_creation(client):
    #Test event creation
    # Simulate login as admin first
    admin_user = User.query.filter_by(email='testuser@example.com').first()
    with client.session_transaction() as sess:
        sess['user_id'] = admin_user.id
    response = client.post('/event/create', data={
        'name': 'New Event',
        'description': 'This is a new event',
        'urgency': 'High',
        'address': '456 Event St',
        'state': 1,  # Assuming California is in the database
        'zipcode': '90210'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"The Event : New Event has been successfully created" in response.data

def test_notification_create(client):
    #Test notification creation
    sample_event = Event.query.filter_by(name='Sample Event').first()
    response = client.post(f'/notification/create/{sample_event.id}', data={
        'name': 'New Notification',
        'description': 'This is a new notification'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Notification Sent! : New Notification" in response.data

def test_logout(client):
    #Test user logout
    client.post('/login', data={'email': 'testuser@example.com', 'password': 'password123'}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out." in response.data
