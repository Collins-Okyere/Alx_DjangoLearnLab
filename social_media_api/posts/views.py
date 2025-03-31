from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from .models import Post, Like
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    following_users = request.user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

class LikePostView(APIView):
    def post(self, request, post_id):
        user = request.user
        post = Post.objects.get(id=post_id)

        if Like.objects.filter(user=user, post=post).exists():
            return Response({"message": "You already liked this post."}, status=400)

        Like.objects.create(user=user, post=post)
        return Response({"message": "Post liked successfully."}, status=201)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        user = request.user
        like = Like.objects.filter(user=user, post=post).first()
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()

        return Response({"detail": "Post unliked successfully."}, status=status.HTTP_200_OK)


