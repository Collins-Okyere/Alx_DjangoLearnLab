from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, generics
from .models import Post, Like
from notifications.models import Notification


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        # Get the Post object or raise a 404 error if not found
        pk = self.kwargs.get('pk')  # Get the pk from URL kwargs
        return get_object_or_404(Post, pk=pk)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer  # Replace with your actual serializer class

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer  # Replace with your actual serializer class



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post, Like, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def like_post(request, pk):
    # Get the post object or return 404 if not found
    post = get_object_or_404(Post, pk=pk)
    
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the user has already liked the post
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:  # If the like already exists, we return a response indicating that
        return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification about the like
    Notification.objects.create(
        recipient=post.author,  # The author of the post is notified
        action="liked",  # You can customize this field to show what action took place
        target=post
    )

    return Response({"detail": "Post liked successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def unlike_post(request, pk):
    # Get the post object or return 404 if not found
    post = get_object_or_404(Post, pk=pk)

    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    # Find the like record to delete
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()  # Remove the like
    except Like.DoesNotExist:
        return Response({"detail": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

    # Create a notification about the unlike
    Notification.objects.create(
        recipient=post.author,  # The author of the post is notified
        action="unliked",  # You can customize this field to show what action took place
        target=post
    )

    return Response({"detail": "Post unliked successfully!"}, status=status.HTTP_200_OK)
