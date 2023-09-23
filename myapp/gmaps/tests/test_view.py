import pytest
from gmaps.models import Gmap,User
from django.core.files.uploadedfile import SimpleUploadedFile
from factories import UserFactory,GmapFactory,GmapFactoryNoMagicWord
pytestmark = pytest.mark.django_db
from django.urls import reverse
import hashlib
from django.db.models import Q




@pytest.fixture
def create_users_and_gmaps():
    user_list = UserFactory.create_batch(5)

    for user in user_list:
        GmapFactory.create_batch(3, user=user)

    return user_list


@pytest.fixture
def create_users_and_gmaps_no_magic_word():
    user_list = UserFactory.create_batch(5)

    for user in user_list:
        GmapFactoryNoMagicWord.create_batch(3, user=user)

    return user_list


@pytest.mark.django_db
def test_create_gmap_view(client):
    with open('/myapp/media/images/images.jpeg', 'rb') as image_file:
        uploaded_image = SimpleUploadedFile(name='images.jpeg', content=image_file.read(), content_type='image/jpeg')


    user = User.objects.create_user(username='testuser',email='example@gmail.com',birth='2000-05-05', password='12345')


    is_logged_in = client.login(username='testuser', password='12345')
    assert is_logged_in == True
    response = client.post('/gmaps/create/', {
        'title': 'Test title',
        'comment': 'Test comment',
        'latitude': 35.6895,
        'longitude': 139.6917,
        'picture' :uploaded_image,
        'magic_word': "magic_word",
        'user' : user.id
    })

    assert response.status_code == 302  # 成功時のステータスコードが201であることを確認
    assert Gmap.objects.count() == 1
    client.logout()



@pytest.mark.django_db
def test_create_gmap_view_unauthenticated(client):
    with open('/myapp/media/images/images.jpeg', 'rb') as image_file:
        uploaded_image = SimpleUploadedFile(name='images.jpeg', content=image_file.read(), content_type='image/jpeg')

    user = User.objects.create_user(username='testuser',email='example@gmail.com',birth='2000-05-05', password='12345')

    response = client.post('/gmaps/create/', {
        'title': 'Test title',
        'comment': 'Test comment',
        'latitude': 35.6895,
        'longitude': 139.6917,
        'picture' :uploaded_image,
        'magic_word': "magic_word",
        'user' : user.id
    })
    assert response.status_code == 302
    assert user.gmaps.all().count() == 0


@pytest.mark.django_db
def test_delete_gmap_view(client,create_users_and_gmaps):
    user_list = create_users_and_gmaps

    for user in user_list:
        is_logged_in = client.login(username=user.username,password='password')
        assert is_logged_in == True
        g = 3
        for gmap in user.gmaps.all():

            response1 = client.get(f'/gmaps/show/{gmap.id}/')
            assert response1.status_code == 200

            response = client.post(f'/gmaps/delete/{gmap.id}/')

            g = g - 1
            assert response.status_code == 302
            assert user.gmaps.all().count() == g

    client.logout()


@pytest.mark.django_db
def test_delete_gmap_view_unauthenticated(client,create_users_and_gmaps):
    user_list = create_users_and_gmaps
    assert Gmap.objects.count() == 15


    for user in user_list:
        g = 3
        for gmap in user.gmaps.all():
            response1 = client.get(f'/gmaps/show/{gmap.id}/')
            assert response1.status_code == 302

            response = client.post(f'/gmaps/delete/{gmap.id}/')

            g = g - 1
            assert response.status_code == 403
            assert user.gmaps.all().count() == 3

@pytest.mark.django_db
def test_private_search(client,create_users_and_gmaps):
    user_list = create_users_and_gmaps
    assert Gmap.objects.count() == 15

    for user in user_list:
        is_logged_in = client.login(username=user.username,password='password')
        assert is_logged_in == True
        email = user.email
        magic_word = "magic_word"  # この値はテスト環境で適切に設定してください
        magic_word_hash = hashlib.md5(magic_word.encode()).hexdigest()

        # パラメータを指定してリクエスト
        url = reverse('gmap_private_search')  # URL名に合わせて変更
        response = client.get(url, {'email': email, 'magic_word': magic_word})

        # ステータスコードと返されるオブジェクトを確認
        assert response.status_code == 200
        queryset = Gmap.objects.filter(user__email=email).filter(Q(magic_word=magic_word_hash) & ~Q(magic_word=""))

        assert list(response.context['gmaps']) == list(queryset)

    client.logout()


@pytest.mark.django_db
def test_private_search_unauthenticated(client,create_users_and_gmaps):
    user_list = create_users_and_gmaps
    assert Gmap.objects.count() == 15

    for user in user_list:
        email = user.email
        magic_word = "magic_word"  # この値はテスト環境で適切に設定してください
        magic_word_hash = hashlib.md5(magic_word.encode()).hexdigest()

        # パラメータを指定してリクエスト
        url = reverse('gmap_private_search')  # URL名に合わせて変更
        response = client.get(url, {'email': email, 'magic_word': magic_word})

        # ステータスコードと返されるオブジェクトを確認
        assert response.status_code == 302
    

@pytest.mark.django_db
def test_gmap_list_unauthenticated(client):
    url = reverse('gmap_list')
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_public_search(client, create_users_and_gmaps_no_magic_word):
    user_list = create_users_and_gmaps_no_magic_word
    assert Gmap.objects.count() == 15

    for user in user_list:
        url = reverse('gmap_public_search')
        data = {'username': user.username, 'birth': user.birth}

        response = client.get(url, data)

        assert response.status_code == 200
        queryset = Gmap.objects.filter(user__username=user.username, user__birth=user.birth, magic_word="")

        assert list(response.context['gmaps']) == list(queryset)


# def test_private_search_authenticated(api_client, token, user, gmap):
#     url = reverse('gmaps-private_search')
#     api_client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

#     gmap.magic_word = "test"
#     gmap.save()

#     data = {'email': user.email, 'magic_word': "test"}

#     response = api_client.get(url, data)

#     assert response.status_code == HTTP_200_OK
#     assert response.data[0]['id'] == str(gmap.id)


# def test_private_search_unauthenticated(api_client, user, gmap):
#     url = reverse('gmaps-private_search')

#     gmap.magic_word = "test"
#     gmap.save()

#     data = {'email': user.email, 'magic_word': "test"}

#     response = api_client.get(url, data)

#     assert response.status_code == HTTP_401_UNAUTHORIZED


