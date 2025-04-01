from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)  # For Comment viewset

urlpatterns = [
    path('', include(router.urls)),  # Include the generated URLs
]

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('<int:pk>/unlike/', views.unlike_post, name='unlike_post'),
]
