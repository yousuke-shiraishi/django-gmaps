import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from gmaps.factories import UserFactory, GmapFactory, GmapFactoryNoMagicWord

user_list = UserFactory.create_batch(3)

for user in user_list:
    GmapFactoryNoMagicWord.create_batch(3, user=user)


# user_list = UserFactory.create_batch(3)

# for user in user_list:
#     GmapFactory.create_batch(2, user=user)
