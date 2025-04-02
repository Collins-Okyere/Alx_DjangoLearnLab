from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets, permissions, filters, generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Post, Like, Comment
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification

User = get_user_model()

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')  # Get the pk from URL kwargs
        return get_object_or_404(Post, pk=pk)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="liked your post",
        target_content_type=ContentType.objects.get_for_model(Post),
        target_object_id=post.id
    )

    return Response({"detail": "Post liked successfully!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
    except Like.DoesNotExist:
        return Response({"detail": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

    Notification.objects.create(
        recipient=post.author,
        actor=request.user,
        verb="unliked your post",
        target_content_type=ContentType.objects.get_for_model(Post),
        target_object_id=post.id
    )

    return Response({"detail": "Post unliked successfully!"}, status=status.HTTP_200_OK)


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            following_users = user.following.all()
            if following_users.exists():
                return Post.objects.filter(author__in=following_users).order_by('-created_at')

        return Post.objects.all().order_by('-created_at')  # Default to all posts if not following anyone


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()

        if following_users.exists():
            posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        else:
            posts = Post.objects.none()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
