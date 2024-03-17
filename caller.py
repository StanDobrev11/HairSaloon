import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HairSaloon.settings")
django.setup()

from HairSaloon.services.models import Service

Service.objects.create(
    name='Tousled Lob Haircut',
    male_female_child='female',
    description='If you want that glamorous edge that a crop can give but with the flexibility of longer locks, then a lob haircut is a perfect choice.',
    duration=45,
    price=25,
    haircut_url='https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/12-long-shaggy-bob-haircut-B56DTa0BthM.jpg?w=877&ssl=1',
)
