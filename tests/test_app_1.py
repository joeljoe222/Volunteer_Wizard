import pytest
from flask import Flask, session
from app import app, db, users, profiles

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            populate_db()
        yield client
        db.session.remove()
        db.drop_all()

def populate_db():
    user1 = users.User(username='testuser', email='test@example.com')
    profile1 = profiles.Profile(user_id=user1.id, bio='Test bio')
    
    db.session.add(user1)
    db.session.add(profile1)
    db.session.commit()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Select an Event' in response.data

def test_event_page(client):
    response = client.get('/event/1')
    assert response.status_code == 200
    assert b'Test Event' in response.data

def test_volunteer_matching(client):
    response = client.get('/volunteer/matching')
    assert response.status_code == 200
    assert b'Volunteer Matching Form' in response.data

def test_admin_events(client):
    response = client.get('/admin/events')
    assert response.status_code == 200
    assert b'Select an Event' in response.data

def test_admin_matching(client):
    response = client.get('/admin/matching')
    assert response.status_code == 200
    assert b'Admin Volunteer Matching' in response.data

def test_event_create_page(client):
    response = client.get('/event/create')
    assert response.status_code == 200
    assert b'Create Event' in response.data

def test_event_manage_page(client):
    response = client.get('/event/manage/1')
    assert response.status_code == 200
    assert b'Manage Event' in response.data

def test_event_view_page(client):
    response = client.get('/event/view/1')
    assert response.status_code == 200
    assert b'Test Event' in response.data
    assert b'View Event' in response.data

def test_notification_create_page(client):
    response = client.get('/notification/create')
    assert response.status_code == 200
    assert b'Create Notification' in response.data

def test_notification_main_page(client):
    response = client.get('/notification')
    assert response.status_code == 200
    assert b'Reminders' in response.data
    assert b'Updates' in response.data

def test_event_main_page(client):
    response = client.get('/events')
    assert response.status_code == 200
    assert b'List of Events' in response.data

def test_history_page(client):
    response = client.get('/history')
    assert response.status_code == 200
    assert b'Volunteer History Form' in response.data

def test_admin_events_page(client):
    response = client.get('/admin/events')
    assert response.status_code == 200
    assert b'Event List' in response.data
