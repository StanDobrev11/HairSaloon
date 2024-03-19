import datetime
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HairSaloon.settings")
django.setup()

from HairSaloon.services.models import Service
from HairSaloon.bookings.models import Booking
from HairSaloon.hairdressers.models import HairDresser

# Service.objects.create(
#     name='Tousled Lob Haircut',
#     male_female_child='female',
#     description='If you want that glamorous edge that a crop can give but with the flexibility of longer locks, then a lob haircut is a perfect choice.',
#     duration=45,
#     price=25,
#     haircut_url='https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/12-long-shaggy-bob-haircut-B56DTa0BthM.jpg?w=877&ssl=1',
# )
#
# Service.objects.create(
#     name='Curtain Bangs and Shag Haircut',
#     male_female_child='female',
#     description='A fringe is a thing to puzzle over. In 2024 bangs are on-trend, so a shag with curtain bangs can be one of the best haircuts to try asap. Don’t want to regret it? Try clip-in bangs and then make the final decision.',
#     duration=45,
#     price=20,
#     haircut_url='https://i1.wp.com/www.hadviser.com/wp-content/uploads/2020/02/1-trending-hairstyle-for-women-CNfIfNdDDYf.jpg?w=718&ssl=1',
# )
#
# Service.objects.create(
#     name='Textured Haircut',
#     male_female_child='female',
#     description='Another great way to take advantage of short bob haircuts without high maintenance is to try a textured look. The quickest way to style a trendy bob is to make it a bit messy and tousled.',
#     duration=40,
#     price=22.50,
#     haircut_url='https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/2-short-trendy-bob-B42RYXnFLyy.jpg?w=504&ssl=1',
# )
#
# Service.objects.create(
#     name='Lob with Face-Framing Bangs',
#     male_female_child='female',
#     description='A voluminous lob is one of the trendiest haircuts for women, and it looks so charming with long face-framing bangs. If you have dark brown hair, just add some subtle highlights to create a lively, romantic look.',
#     duration=35,
#     price=28.50,
#     haircut_url='https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/02/1-voluminous-lob-haircut-with-bangs-CLJg371BdpY.jpg?w=810&ssl=1',
# )
#
# Service.objects.create(
#     name='Razored Brunette Comb Over Bob',
#     male_female_child='female',
#     description='If you’re a proud wearer of long thick hair, there may come the time when you feel like chopping at least a half of it for the greater good. Hop on the 2024 hair trends train and give yourself a makeover with a deep side-parted lob. A razored lob is easy to style at home, especially for those who’s got slightly wavy hair. Looking drop-dead gorgeous will be easy with this haircut.',
#     duration=25,
#     price=20,
#     haircut_url='https://i2.wp.com/www.hadviser.com/wp-content/uploads/2020/02/2-brunette-side-parted-lob-CH4GHndsPDO.jpg?w=636&ssl=1',
# )
#
# Service.objects.create(
#     name='Layers and Highlights',
#     male_female_child='female',
#     description='Not yet ready for a full-blown new color and haircut? Then go for some soft, highlighted layers and get a subtle yet eye-catching and fashion-forward hairstyle!',
#     duration=45,
#     price=28.50,
#     haircut_url='https://i0.wp.com/www.hadviser.com/wp-content/uploads/2021/08/1-long-haircut-with-layers-and-highlights-CUfIAwoMmcm.jpg?w=622&ssl=1',
# )
#
# Service.objects.create(
#     name='Shoulder-Length Shag for Thick Hair',
#     male_female_child='female',
#     description='If you’re after a sophisticated, trouble-free hairstyle, then try this wavy shag. It’s one of the long-term trending hairstyles that are both elegant and fun!',
#     duration=40,
#     price=25.50,
#     haircut_url='https://i2.wp.com/www.hadviser.com/wp-content/uploads/2021/08/2-thick-shoulder-length-shag-CUxMWlZr8dd.jpg?w=746&ssl=1',
# )
#
# Service.objects.create(
#     name='Below-the-Shoulders Textured Haircut',
#     male_female_child='female',
#     description='One of the hairstyles for women to fit any style. Got more hair ideas? You can also opt to texture it a bit and add some golden highlights to elevate your overall glow.',
#     duration=20,
#     price=20,
#     haircut_url='https://i2.wp.com/www.hadviser.com/wp-content/uploads/2021/08/6-textured-haircut-with-highlights-CU_EUnGLCnQ.jpg?w=502&ssl=1',
# )
#
# Service.objects.create(
#     name='The French Bob',
#     male_female_child='female',
#     description='A short and sophisticated haircut that gives you the edge. Haircuts with bangs are becoming a big trend this year.',
#     duration=25,
#     price=23.50,
#     haircut_url='https://i2.wp.com/www.hadviser.com/wp-content/uploads/2020/02/10-short-franch-bob-with-bangs-B7R4xBRJpox.jpg?w=661&ssl=1',
# )
#
# Service.objects.create(
#     name='Straight Collarbone Bob',
#     male_female_child='female',
#     description='If you’re tired of wearing extremely long hair, we recommend a straight collarbone bob. It’s among trending hairstyles that can refresh your look and bring your hair back to life.',
#     duration=65,
#     price=35.00,
#     haircut_url='https://i1.wp.com/www.hadviser.com/wp-content/uploads/2020/02/10-trending-bob-hairstyle-CLYK_IqjV1i.jpg?w=614&ssl=1',
# )

service = Service.objects.get(pk=25)
# hairdresser = HairDresser.objects.filter(services__id=service.id)[0]


book = Booking(
    date=datetime.date(2024, 3, 22),
    start=datetime.time(12, 0, 0),
    end=datetime.time(12, 30, 0),
    service=service

)
book.save()
print()
