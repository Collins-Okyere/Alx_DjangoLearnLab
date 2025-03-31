from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post  # Import the Post model from the posts app

# Comment Model (for the comments app)
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments_in_comments_app', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comment_comments')  # Avoids conflict
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]  # To display first 20 characters in the admin panel
