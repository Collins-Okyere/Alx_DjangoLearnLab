from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from .models import Post, Like
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from django.shortcuts import get_object_or_404



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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Correct usage of get_object_or_404 to fetch the post
        post = get_object_or_404(Post, pk=pk)

        # Check if the user already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if created:
            # Create a notification for the post owner
            Notification.objects.create(
                recipient=post.author, 
                actor=request.user,
                verb="liked your post",
                target=post
            )
            return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)

        return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Correct usage of get_object_or_404 to fetch the post
        post = get_object_or_404(Post, pk=pk)

        # Try to get the like object
        like = Like.objects.filter(user=request.user, post=post).first()

        if like:
            like.delete()  # Remove the like
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)

        return Response({"message": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)