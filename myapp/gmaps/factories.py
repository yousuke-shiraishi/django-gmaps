import factory
from factory.django import DjangoModelFactory
from faker import Faker
from .models import Gmap, User
import random

fake = Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.LazyAttribute(lambda _: fake.user_name())
    email = factory.LazyAttribute(lambda _: fake.email())
    birth = factory.LazyFunction(lambda: fake.date_of_birth(minimum_age=22, maximum_age=50).strftime("%Y-%m-%d"))
    password = factory.PostGenerationMethodCall('set_password', 'password')



class GmapFactory(DjangoModelFactory):
    class Meta:
        model = Gmap

    title = factory.LazyAttribute(lambda _: fake.pystr(max_chars=25))
    comment = factory.LazyAttribute(lambda _: fake.text())
    latitude = factory.LazyAttribute(lambda _: random.uniform(24.0, 45.0))
    longitude = factory.LazyAttribute(lambda _: random.uniform(122.0, 153.0))
    picture = factory.django.ImageField(color='blue')
    magic_word = 'magic_word'
    user = factory.SubFactory(UserFactory)


class GmapFactoryNoMagicWord(DjangoModelFactory):
    class Meta:
        model = Gmap

    title = factory.LazyAttribute(lambda _: fake.pystr(max_chars=25))
    comment = factory.LazyAttribute(lambda _: fake.text())
    latitude = factory.LazyAttribute(lambda _: random.uniform(24.0, 45.0))
    longitude = factory.LazyAttribute(lambda _: random.uniform(122.0, 153.0))
    picture = factory.django.ImageField(color='blue')
    magic_word = ''
    user = factory.SubFactory(UserFactory)
