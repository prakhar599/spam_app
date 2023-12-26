# In populate_data.py
import random
from faker import Faker
from api.models import User, Contact
from django.contrib.auth.hashers import make_password

fake = Faker()

def generate_sample_data():
    # Create some sample users
    for _ in range(10):
        password = make_password(fake.password())
        user = User.objects.create(
            name=fake.name(),
            phone_number=fake.phone_number(),
            email=fake.email(),
            password=password,
        )

        # Create some contacts for each user
        for _ in range(random.randint(0, 5)):
            Contact.objects.create(
                user=user,
                name=fake.name(),
                phone_number=fake.phone_number(),
            )

if __name__ == '__main__':
    generate_sample_data()
