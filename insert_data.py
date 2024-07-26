#RUNNING THIS WILL CLEAR ALL DATA IN FOLLOWING DATABASES : 
#	EVENTS, NOTIFICATIONS, USERS

#ERASE PREVIOUS DATA AND ADD PLACEHOLDER
from app import app, db, Event, Notification, User
from datetime import datetime

with app.app_context():
    # Clear existing data
    db.session.query(Notification).delete()
    db.session.query(Event).delete()
    db.session.query(User).delete()

	# Create a sample user
    user = User(name='Sample', email='sample@example.com', password='password', role='1', address='address', skills='skills', preferencess='preference', availability='avalability')
    db.session.add(user)
    db.session.commit()

    # Create sample events
    events = [
        {
            'name': 'Event One',
            'description': 'Description for Event One',
            'date': datetime(2025, 1, 1),
            'urgency': '1',
            'address': '1111 Street Name',
            'state': 'TX',
            'zipcode': '11111',
            'skills': '1',
            'user_id': user.id
        },
        {
            'name': 'Event Two',
            'description': 'Description for Event Two',
            'date': datetime(2025, 2, 2),
            'urgency': '2',
            'address': '2222 Street Name',
            'state': 'FL',
            'zipcode': '22222',
            'skills': '3',
            'user_id': user.id
        }
    ]

    for event_data in events:
        event = Event(**event_data)
        db.session.add(event)
    db.session.commit()

    # Create sample notifications for each event
    event_one = Event.query.filter_by(name='Event One').first()
    event_two = Event.query.filter_by(name='Event Two').first()

    notifications = [
        {
            'name': 'Notification ONE for Event ONE',
            'description': 'Notification ONE Description for Event ONE',
            'event_id': event_one.id
        },
        {
            'name': 'Notification TWO for Event ONE',
            'description': 'Notification TWO Description for Event ONE',
            'event_id': event_one.id
        },
        {
            'name': 'Notification ONE for Event TWO',
            'description': 'Notification ONE Description for Event TWO',
            'event_id': event_two.id
        },
        {
            'name': 'Notification TWO for Event TWO',
            'description': 'Notification TWO Description for Event TWO',
            'event_id': event_two.id
        },
        {
            'name': 'Notification THREE for Event TWO',
            'description': 'Notification THREE Description for Event TWO',
            'event_id': event_two.id
        }
    ]

    for notification_data in notifications:
        notification = Notification(**notification_data)
        db.session.add(notification)
    db.session.commit()

    print("Sample data inserted.")
