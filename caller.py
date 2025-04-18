import os
from datetime import date

import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HairSaloon.settings")
django.setup()

UserModel = get_user_model()

from HairSaloon.services.models import Service
from HairSaloon.hairdressers.models import HairDresser

# Create all services
services_data = [
    {
        "name": "Tousled Lob Haircut",
        "male_female_child": "female",
        "description": "If you want that glamorous edge that a crop can give but with the flexibility of longer locks, then a lob haircut is a perfect choice.",
        "duration": 45,
        "price": 25,
        "haircut_url": "https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/12-long-shaggy-bob-haircut-B56DTa0BthM.jpg?w=877&ssl=1",
    },
    {
        "name": "Curtain Bangs and Shag Haircut",
        "male_female_child": "female",
        "description": "A fringe is a thing to puzzle over. In 2024 bangs are on-trend, so a shag with curtain bangs can be one of the best haircuts to try asap.",
        "duration": 45,
        "price": 20,
        "haircut_url": "https://i1.wp.com/www.hadviser.com/wp-content/uploads/2020/02/1-trending-hairstyle-for-women-CNfIfNdDDYf.jpg?w=718&ssl=1",
    },
    {
        "name": "Textured Haircut",
        "male_female_child": "female",
        "description": "Another great way to take advantage of short bob haircuts without high maintenance is to try a textured look.",
        "duration": 40,
        "price": 22.50,
        "haircut_url": "https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/2-short-trendy-bob-B42RYXnFLyy.jpg?w=504&ssl=1",
    },
    {
        "name": "Lob with Face-Framing Bangs",
        "male_female_child": "female",
        "description": "A voluminous lob is one of the trendiest haircuts for women, and it looks so charming with long face-framing bangs.",
        "duration": 35,
        "price": 28.50,
        "haircut_url": "https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/1-voluminous-lob-haircut-with-bangs-CLJg371BdpY.jpg?w=810&ssl=1",
    },
    {
        "name": "Razored Brunette Comb Over Bob",
        "male_female_child": "female",
        "description": "Hop on the 2024 hair trends train and give yourself a makeover with a deep side-parted lob.",
        "duration": 25,
        "price": 20,
        "haircut_url": "https://i2.wp.com/www.hadviser.com/wp-content/uploads/2020/02/2-brunette-side-parted-lob-CH4GHndsPDO.jpg?w=636&ssl=1",
    },
    {
        "name": "Layers and Highlights",
        "male_female_child": "female",
        "description": "Not yet ready for a full-blown new color and haircut? Then go for some soft, highlighted layers.",
        "duration": 45,
        "price": 28.50,
        "haircut_url": "https://i0.wp.com/www.hadviser.com/wp-content/uploads/2021/08/1-long-haircut-with-layers-and-highlights-CUfIAwoMmcm.jpg?w=622&ssl=1",
    },
    {
        "name": "Shoulder-Length Shag for Thick Hair",
        "male_female_child": "female",
        "description": "If you’re after a sophisticated, trouble-free hairstyle, then try this wavy shag.",
        "duration": 40,
        "price": 25.50,
        "haircut_url": "https://i2.wp.com/www.hadviser.com/wp-content/uploads/2021/08/2-thick-shoulder-length-shag-CUxMWlZr8dd.jpg?w=746&ssl=1",
    },
    {
        "name": "Below-the-Shoulders Textured Haircut",
        "male_female_child": "female",
        "description": "You can also opt to texture it a bit and add some golden highlights to elevate your overall glow.",
        "duration": 20,
        "price": 20,
        "haircut_url": "https://i2.wp.com/www.hadviser.com/wp-content/uploads/2021/08/6-textured-haircut-with-highlights-CU_EUnGLCnQ.jpg?w=502&ssl=1",
    },
    {
        "name": "The French Bob",
        "male_female_child": "female",
        "description": "A short and sophisticated haircut that gives you the edge. Haircuts with bangs are becoming a big trend this year.",
        "duration": 25,
        "price": 23.50,
        "haircut_url": "https://i2.wp.com/www.hadviser.com/wp-content/uploads/2020/02/10-short-franch-bob-with-bangs-B7R4xBRJpox.jpg?w=661&ssl=1",
    },
    {
        "name": "Straight Collarbone Bob",
        "male_female_child": "female",
        "description": "If you’re tired of wearing extremely long hair, we recommend a straight collarbone bob.",
        "duration": 65,
        "price": 35.00,
        "haircut_url": "https://i1.wp.com/www.hadviser.com/wp-content/uploads/2020/02/10-trending-bob-hairstyle-CLYK_IqjV1i.jpg?w=614&ssl=1",
    },
]

services_created = []
for service_data in services_data:
    service, _ = Service.objects.get_or_create(**service_data)
    services_created.append(service)

print("Services created.")

# Create admin and users
admin, _ = UserModel.objects.get_or_create(
    email='admin@salon.com',
    defaults={'is_superuser': True, 'is_staff': True}
)
admin.set_password('1234')
admin.save()

staff1, _ = UserModel.objects.get_or_create(
    email='ivana@staff.com',
    defaults={
        'is_staff': True,
        'first_name': 'Ivana',
        'last_name': 'Ivanova',
    }
)
staff1.set_password('1234')
staff1.save()

staff2, _ = UserModel.objects.get_or_create(
    email='marin@staff.com',
    defaults={
        'is_staff': True,
        'first_name': 'Marin',
        'last_name': 'Marinov',
    }
)
staff2.set_password('1234')
staff2.save()

user1, _ = UserModel.objects.get_or_create(email='stan@user.com')
user1.set_password('1234')
user1.save()

user2, _ = UserModel.objects.get_or_create(email='iv@user.com')
user2.set_password('1234')
user2.save()

print("Users created.")

# Create hairdressers and assign services
hd1, created1 = HairDresser.objects.get_or_create(
    user=staff1,
    defaults={
        'background': "Ivana has been with us for many years and she has proven to be a great asset! Some other details just to get it good looking",
        'working_since': date(2005, 1, 11),
    }
)
if created1:
    hd1.services.set(services_created[:5])  # First 5 services
else:
    # Make sure data is updated if already existed
    hd1.background = "Ivana has been with us for many years and she has proven to be a great asset! Some other details just to get it good looking"
    hd1.working_since = date(2005, 1, 11)
    hd1.save()
    hd1.services.set(services_created[:5])

hd2, created2 = HairDresser.objects.get_or_create(
    user=staff2,
    defaults={
        'background': "Something else that is describing the hairdresser as an excellent professional!",
        'working_since': date(2025, 7, 18),
    }
)
if created2:
    hd2.services.set(services_created[5:])  # Last 5 services
else:
    hd2.background = "Something else that is describing the hairdresser as an excellent professional!"
    hd2.working_since = date(2025, 7, 18)
    hd2.save()
    hd2.services.set(services_created[5:])
