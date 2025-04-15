from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.create_view, name='ad_create'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



