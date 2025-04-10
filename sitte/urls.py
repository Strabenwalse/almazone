from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    # path('<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('create/', views.ad_create, name='ad_create'),
    path('', views.index, name='index'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



