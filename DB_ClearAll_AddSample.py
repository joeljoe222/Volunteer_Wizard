#THIS WILL CLEAR ALL DATABASES
#This will add skills and states to respective DB
#This adds sample data to Event, Notification, User DBs
from app import app, db, Event, Notification, User, Skill, State
from datetime import datetime

#PLACE HOLDER SKILLS PLEASE ADD ACTUAL SKILLS LIST LATER
skills = {
    'skill 1','skill 2','skill 3','skill 4','skill 5'
}

#Dictionary of all US states 'TX': 'Texas'
states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}


with app.app_context():
    db.drop_all()
    db.create_all()
    print("All Database cleared and recreated.")

    #Populate Skill Database
    skill_objs = []
    for skill_name in skills:
        existing_skill = Skill.query.filter_by(name=skill_name).first()
        if not existing_skill:
            new_skill = Skill(name=skill_name)
            db.session.add(new_skill)
            skill_objs.append(new_skill)
    db.session.commit()
    
    #Populate State Database
    state_objs = []
    for state_code, state_name in states.items():
        existing_state = State.query.filter_by(code=state_code).first()
        if not existing_state:
            new_state = State(code=state_code, name=state_name)
            db.session.add(new_state)
            state_objs.append(new_state)
    db.session.commit()

    print('Skill Database and State Database initialized')


    #Create a sample users
    #prefrences is commented out in the model add later if missing argument
    #Admin Sample
    user_admin = User(name='Admin', email='Admin@example.com', password='password', role='2', address='address', state_id=state_objs[1].id, availability='avalability')
    user_admin.skills.extend(skill_objs[:3])

    db.session.add(user_admin)
    db.session.commit()
    print('=============================')
    print('Sample Admin User Created')
    print('=============================')
    print(f'Name: {user_admin.name}')
    print(f'Email: {user_admin.email}')
    print(f'Password: {user_admin.password}')
    
    #Volunteer Sample
    user_volunteer = User(name='Volunteer', email='Volunteer@example.com', password='password', role='1', address='address', state_id=state_objs[2].id, availability='avalability')
    user_volunteer.skills.extend(skill_objs[:3])

    db.session.add(user_volunteer)
    db.session.commit()
    print('=============================')
    print('Sample Volunteer User Created')
    print('=============================')
    print(f'Name: {user_volunteer.name}')
    print(f'Email: {user_volunteer.email}')
    print(f'Password: {user_volunteer.password}')
    print('=============================')


    #Create sample events
    events = [
        {
            'name': 'Event One',
            'description': 'Description for Event One',
            'date': datetime(2025, 1, 1),
            'urgency': '1',
            'address': '1111 Street Name',
            'city': 'city',
            'state': state_objs[1],
            'zipcode': '11111',
            'user_id': user_admin.id
        },
        {
            'name': 'Event Two',
            'description': 'Description for Event Two',
            'date': datetime(2025, 2, 2),
            'urgency': '2',
            'address': '2222 Street Name',
            'city': 'city222',
            'state': state_objs[15],
            'zipcode': '22222',
            'user_id': user_admin.id
        }
    ]

    for event_data in events:
        event = Event(**event_data)
        event.skills.extend(skill_objs[1:3])
        db.session.add(event)
    db.session.commit()

    print('Sample Events Created')

    #Create sample notifications for each event
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

    print('Sample Notifications Created')
    print('Succesfully Cleared Databases and Added Sample Data')