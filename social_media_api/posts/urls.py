from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, FeedView
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)  # For Comment viewset

urlpatterns = [
    path('', include(router.urls)),  # Include the generated URLs
    router.register(r'posts', PostViewSet)
]

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
]