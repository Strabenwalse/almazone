from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views
from .views import ad_create
from sitte.views import ad_list
urlpatterns = [
    path('', ad_list, name='index'),
    path('', views.ad_list, name='ad_list'),
    path('create/', ad_create, name='ad_create'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-ads/', views.my_ads, name='my_ads'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/edit/<int:pk>/', views.ad_edit, name='ad_edit'),
    path('ad/delete/<int:pk>/', views.ad_delete, name='ad_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



