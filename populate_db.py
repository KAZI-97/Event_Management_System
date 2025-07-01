import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta
from events.models import Category, Event, Participant 

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')  # Replace with your project name
django.setup()

def populate_db():
    fake = Faker()

    # Create Categories
    category_names = ['Music', 'Tech', 'Sports', 'Education', 'Health', 'Business', 'Art', 'Gaming']
    categories = []
    for name in category_names:
        cat = Category.objects.create(
            name=name,
            description=fake.paragraph()
        )
        categories.append(cat)
    print(f"Created {len(categories)} categories.")

    # Create Participants
    participants = []
    for _ in range(30):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    # Create Events with status
    events = []
    for _ in range(50):
        event_status = random.choice(['UPCOMING', 'COMPLETED'])
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=fake.date_between(start_date='-1y', end_date='+6M'),
            time=fake.time_object(),
            location=fake.city(),
            category=random.choice(categories),
            status=event_status
        )
        event.participant_set.set(random.sample(participants, random.randint(2, 6)))
        events.append(event)
    print(f"Created {len(events)} events with status (UPCOMING/COMPLETED).")

    print("✅ Database populated successfully!")

populate_db()
