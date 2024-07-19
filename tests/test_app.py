import pytest
from flask import Flask, session
from app import app, users, profiles

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index page (login)."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register(client):
    """Test user registration."""
    response = client.post('/register', data={
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': '1'
    })
    assert response.status_code == 302  # Redirect after registration
    assert b'Profile successfully updated!' not in response.data

def test_login(client):
    """Test user login."""
    # Register a user first
    client.post('/register', data={
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': '1'
    })
    
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    
    assert response.status_code == 302  # Redirect after login
    assert b'Welcome back' in response.data

def test_profile_update(client):
    """Test profile update."""
    # Register and login the user
    client.post('/register', data={
        'email': 'test@example.com',
        'password': 'testpassword',
        'role': '1'
    })
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    
    response = client.post('/profile/test@example.com', data={
        'full_name': 'Test User',
        'address1': '123 Main St',
        'address2': '',
        'city': 'Test City',
        'state': 'CA',
        'zip_code': '90001',
        'skills': ['skill1'],
        'preferences': 'None',
        'availability[]': ['2024-07-01']
    })
    
    assert response.data == b'Profile successfully updated!'
    assert 'Test User' in profiles['test@example.com']['full_name']

def test_validation(client):
    """Test form validation (missing required fields)."""
    response = client.post('/register', data={})
    assert b'This field is required' in response.data

def test_about_page(client):
    """Test the about page."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data
