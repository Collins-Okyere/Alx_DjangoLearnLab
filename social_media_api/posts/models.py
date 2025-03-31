from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=100, default='Untitled')
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this line
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field is added

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can like a post only once

    def __str__(self):
        return f"{self.user} liked {self.post.title}"


class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_notifications',  # Add related_name
        related_query_name='post_notification',  # Optional: for reverse queries
    )    
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actor_notifications', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} by {self.actor}"
