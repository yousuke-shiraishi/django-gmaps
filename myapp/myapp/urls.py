from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from gmaps.views import GmapListView, GmapCreateOrUpdateView, GmapDeleteView, GmapsSearchView
from gmaps.views import (
    UserDetailView,
    UserCreateView,
    UserUpdateView,
)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('', GmapListView.as_view(), name='gmap_list'),
    path('gmaps/create_or_update/<str:pk>/', GmapCreateOrUpdateView.as_view(), name='gmap_update'),
    path('gmaps/create_or_update/', GmapCreateOrUpdateView.as_view(), name='gmap_create'),
    path('gmaps/delete/<str:pk>/', GmapDeleteView.as_view(), name='gmap_delete'),
    path('gmaps/search/', GmapsSearchView.as_view(), name='gmap_search'),
    path('accounts/',include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


