from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def follow(self, user):
        """Follow another user"""
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow another user"""
        self.following.remove(user)

