import os
import django
import random
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from django.contrib.auth.models import User, Group
from events.models import Category, Event

def populate_db():
    fake = Faker()
    Faker.seed(123)
    random.seed(123)

    participant_group, _ = Group.objects.get_or_create(name='Participant')

    # Create Categories only if none exist
    if Category.objects.count() == 0:
        category_names = ['Music', 'Tech', 'Sports', 'Education', 'Health', 'Business', 'Art', 'Gaming']
        categories = []
        for name in category_names:
            cat = Category.objects.create(
                name=name,
                description=fake.paragraph()
            )
            categories.append(cat)
        print(f"✅ Created {len(categories)} categories.")
    else:
        categories = list(Category.objects.all())
        print("✅ Categories already exist, skipped creation.")

    # Create Users only if none exist in Participant group
    if User.objects.filter(groups__name='Participant').count() == 0:
        participants = []
        for _ in range(30):
            username = fake.unique.user_name()
            email = fake.unique.email()
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                password='testpass123'
            )
            user.groups.add(participant_group)
            participants.append(user)
        print(f"✅ Created {len(participants)} users with 'Participant' group.")
    else:
        participants = list(User.objects.filter(groups__name='Participant'))
        print("✅ Participants already exist, skipped creation.")

    # Create Events only if none exist
    if Event.objects.count() == 0:
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
            rsvp_participants = random.sample(participants, random.randint(2, 6))
            event.rsvped_users.set(rsvp_participants)
            event.save()
            events.append(event)
        print(f"✅ Created {len(events)} events with RSVP participants.")
    else:
        print("✅ Events already exist, skipped creation.")

    print("🎉 Database populated successfully!")

if __name__ == '__main__':
    populate_db()
