from django.urls import path
from .views import signup, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
