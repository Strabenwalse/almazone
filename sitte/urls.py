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
from .views import profile_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('save-theme/', views.save_theme, name='save_theme'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.user_edit, name='user_edit'),
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



