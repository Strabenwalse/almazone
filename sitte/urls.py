from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('ad_list'), name='home'),  # Редирект с главной на список объявлений

    # Профиль пользователя
    # Профиль пользователя
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    # Аутентификация
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Смена пароля
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    # Объявления
    path('ads/', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('my-ads/', views.my_ads, name='my_ads'),
    path('ad/<int:pk>/', views.ad_detail, name='ad_detail'),
    path('ad/edit/<int:pk>/', views.ad_edit, name='ad_edit'),
    path('ad/delete/<int:pk>/', views.ad_delete, name='ad_delete'),

    # Настройки темы
    path('save-theme/', views.save_theme, name='save_theme'),
]

# Для загрузки медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
