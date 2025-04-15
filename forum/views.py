
from django.urls import path
from . import views

urlpatterns = {
    path('', views.index, name='index'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('create', views.ad_create, name='ad_create'),

}
# Create your views here.
