from django.urls import path
from .views import RegisterUserView, LoginUserView,CustomUserListView
from .views import follow_user, unfollow_user


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('users/', CustomUserListView.as_view(), name='user-list'),  # Define the route for listing users
]
