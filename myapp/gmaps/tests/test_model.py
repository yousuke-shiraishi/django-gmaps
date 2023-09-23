import uuid
from faker import Faker
from factories import UserFactory, GmapFactory
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password





@pytest.fixture
def create_users_and_gmaps():
    user_list = UserFactory.create_batch(5)

    for user in user_list:
        GmapFactory.create_batch(3, user=user)

    return user_list


import hashlib
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from gmaps.models import Gmap, User
@pytest.fixture
def test_user():
    return User.objects.create_user(username='testuser', password='12345',email='example0@gmail.com',birth='2000-01-01')

fake = Faker()


@pytest.mark.django_db
def test_create_gmap(test_user):
    user = test_user
    id = uuid.uuid4()
    title = "Test Title"
    comment = "This is a test comment."
    latitude = 123.456
    longitude = 65.432
    picture = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
    magic_word = "magic_word"
    user_id = 1

    gmap = Gmap.objects.create(
        id=id,
        title=title,
        comment=comment,
        latitude=latitude,
        longitude=longitude,
        picture=picture,
        magic_word=magic_word,
        user_id=user.id
    )

    assert gmap.id == id
    assert gmap.title == title
    assert gmap.comment == comment
    assert gmap.latitude == latitude
    assert gmap.longitude == longitude
    # assert gmap.picture == picture
    assert gmap.magic_word == hashlib.md5(magic_word.encode()).hexdigest()
    assert gmap.user_id == user_id



@pytest.mark.django_db
def test_delete_gmap_feature(create_users_and_gmaps):

    user_list = create_users_and_gmaps
    first_user = user_list[0]

    gmaps_of_first_user = Gmap.objects.filter(user=first_user)

    assert gmaps_of_first_user.count() == 3

    for gmap in gmaps_of_first_user:
        gmap.delete()


    assert Gmap.objects.filter(user=first_user).count() == 0


@pytest.mark.django_db
def test_delete_user_feature(create_users_and_gmaps):

    user_list = create_users_and_gmaps


    assert len(user_list) == 5

    for user in user_list:
        user.delete()


    assert User.objects.all().count() == 0



@pytest.mark.django_db
def test_create_user():
    username = 'Yosuke'
    email = 'example@gmail.com'
    birth = '1990-01-01'
    password = 'password'

    user = User.objects.create(
        username=username,
        email=email,
        birth=birth,
        password=password
    )

    assert user.username == username
    assert user.email == email
    assert user.birth == birth
    assert user.password == password


@pytest.mark.django_db
def test_update_user(test_user):
    
    user = test_user
    data = {
    'username' : 'Yosuke',
    'email' : 'example@gmail.com',
    'birth' : '2020-01-01',
    'password' : 'password'
    }

    User.objects.filter(pk=user.id).update(**data)
    updated_user = User.objects.get(pk=user.id)

    assert updated_user.username == data['username']
    assert updated_user.email == data['email']
    assert str(updated_user.birth) == data['birth']
    assert updated_user.password == data['password']
