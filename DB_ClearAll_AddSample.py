#THIS WILL CLEAR ALL DATABASES
#This will add skills and states to respective DB
#This adds sample data to Event, Notification, User DBs
from app import app 
from models import db, Event, Notification, User, Skill, State, VolunteerHistory, user_skills, event_skills
from datetime import datetime
from werkzeug.security import generate_password_hash

#PLACE HOLDER SKILLS PLEASE ADD ACTUAL SKILLS LIST LATER
skills = {
    'Lift Heavy Loads',
    'Stand for Long Periods of Time',
    'Walk for Long Distances',
    'Public Speaking',
    'Photography',
    'Multilingual',
    'Organizing Paperwork',
    'Work well with Children',
    'Lead Group Activities',
    'Guide others',
    'Work with Pets',
    'Security',
    'Greet Guests',
    'Clean inside',
    'Clean outside',
    'Conduct Surveys'
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
    #Clear all databases
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
    
    users = [
        {
            'name':'Admin',
            'email':'admin@email.com',
            'password':'password',
            'role':'admin',
            'address':'1234 main st',
            'state_id': 1,
            'preferences':'preferences',
            'availability':'availible',
            'skills':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        },
        {
            'name':'Volunteer',
            'email':'volunteer@email.com',
            'password':'password',
            'role':'volunteer',
            'address':'1234 main st',
            'state_id': 2,
            'preferences':'preferences',
            'availability':'availible',
            'skills':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        },
        {
            'name':'Jane Doe',
            'email':'janedoe@email.com',
            'password':'password',
            'role':'volunteer',
            'address':'1234 main st',
            'state_id': 3,
            'preferences':'preferences',
            'availability':'availible',
            'skills':[1,2,3,4,5]
        },
        {
            'name':'John Smith',
            'email':'johnsmith@email.com',
            'password':'password',
            'role':'volunteer',
            'address':'1234 main st',
            'state_id': 4,
            'preferences':'preferences',
            'availability':'availible',
            'skills':[6,7,8,9,10]
        },
        {
            'name':'Adam Sandler',
            'email':'adamsandler@email.com',
            'password':'password',
            'role':'volunteer',
            'address':'1234 main st',
            'state_id': 4,
            'preferences':'preferences',
            'availability':'availible',
            'skills':[11,12,13,14,15]
        },
    ]
    
    for user_sample in users:
        hashed_password = generate_password_hash(user_sample['password']) #method='sha256'

        user = User(
            name = user_sample['name'],
            email = user_sample['email'],
            password = hashed_password,
            role = user_sample['role'],
            address = user_sample['address'],
            state_id = user_sample['state_id'],
            preferences = user_sample['preferences'],
            availability = user_sample['availability'],
        )

        user.skills = Skill.query.filter(Skill.id.in_(user_sample['skills'])).all()

        db.session.add(user)
    
    db.session.commit()
    print('Sample users added')


    #Create sample events
    events = [
        {
            'name': 'Comminity CleanUp',
            'description': 'Join us for a day of cleaning and beautifying Central Park. Volunteers will work in teams to pick up litter, plant flowers, and improve the parks environment for everyone to enjoy.',
            'date': datetime(2025, 1, 1),
            'urgency': '3',
            'address': '1234 Main St',
            'city': 'Houston',
            'state_id': 43,
            'zipcode': '77035',
            'user_id': 1,
            'skills':[1,2,3,14]
        },
        {
            'name': 'Food Bank Assistance',
            'description': 'Help organize and distribute food to those in need at the Downtown Center. Volunteers will sort donations, prepare packages, and assist with distribution, ensuring a smooth operation.',
            'date': datetime(2025, 2, 2),
            'urgency': '2',
            'address': '2475 Lane Dr',
            'city': 'Miami',
            'state_id': 9,
            'zipcode': '35077',
            'user_id': 1,
            'skills':[2,7,14]
        },
        {
            'name': 'Art Class for Seniors',
            'description': 'Facilitate an art class for seniors at the community hall. Volunteers will assist with art projects, encourage creativity, and provide a supportive and enjoyable environment for participants.',
            'date': datetime(2025, 3, 3),
            'urgency': '1',
            'address': '2468 Street Ln',
            'city': 'Asheville',
            'state_id': 33,
            'zipcode': '88465',
            'user_id': 1,
            'skills':[4,6,7,9,10]
        }
    ]

    for event_sample in events:
        event = Event(
            name = event_sample['name'],
            description = event_sample['description'],
            date = event_sample['date'],
            urgency = event_sample['urgency'],
            address = event_sample['address'],
            city = event_sample['city'],
            state_id = event_sample['state_id'],
            zipcode = event_sample['zipcode'],
            user_id = event_sample['user_id'],
        )
        event.skills = Skill.query.filter(Skill.id.in_(event_sample['skills'])).all()
        db.session.add(event)
    db.session.commit()

    print('Sample Events Created')

    #Create sample notifications for each event

    notifications = [
        {
            'name': 'Community Cleanup Event Tomorrow!',
            'description': 'Just a reminder that our Community Cleanup event is happening tomorrow at Central Park! We’ll be meeting at the park entrance at 9:00 AM. Please wear comfortable clothes and sturdy shoes. All cleanup materials will be provided. We look forward to seeing you there and making a positive impact on our community!',
            'event_id': 1
        },
        {
            'name': 'Weather Update for Community Cleanup',
            'description': 'We wanted to let you know that the weather forecast for tomorrow is sunny and warm. Be sure to bring sunscreen, a hat, and plenty of water to stay hydrated during the Community Cleanup. Let’s enjoy the beautiful weather while we work!',
            'event_id': 1
        },
        {
            'name': 'Important Details for Todays Food Bank Assistance',
            'description': 'Today is the day! We are excited to have you join us for the Food Bank Assistance event. Please arrive at the Downtown Center by 9:45 AM to check in and receive your assignments. Parking is available in the lot behind the building. Remember to wear comfortable clothing and closed-toe shoes. We will provide gloves and aprons for food handling.',
            'event_id': 2
        },
        {
            'name': 'Art Class for Seniors: Event Day Instructions',
            'description': 'Today is the day for our Art Class for Seniors! Please arrive at the Community Hall by 1:30 PM to help set up art materials and welcome participants. Wear comfortable clothing, as we might get a little messy while creating art! Your role is to assist the seniors with their projects, provide encouragement, and ensure they have a fun and rewarding experience.',
            'event_id': 3
        },
    ]

    for notification_data in notifications:
        notification = Notification(**notification_data)
        db.session.add(notification)
    db.session.commit()

    print('Sample Notifications Created')
    print('Succesfully Cleared Databases and Added Sample Data')

    volunteer = User.query.filter_by(email='volunteer@email.com').first()

    history1 = VolunteerHistory(
        volunteer_id=volunteer.id,
        event_id=1,
        participation_date=datetime(2024, 8, 1, 10, 30),
        status="Confirmed"
    )

    history2 = VolunteerHistory(
        volunteer_id=volunteer.id,
        event_id=2,
        participation_date=datetime(2024, 8, 2, 15, 45),
        status="Attended"
    )

    db.session.add(history1)
    db.session.add(history2)
    db.session.commit()

    print("Sample Volunteer History added.")