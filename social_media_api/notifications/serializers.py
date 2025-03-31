# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType
from posts.models import Post

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor', 'recipient', 'verb', 'target', 'timestamp', 'read']

    def get_target(self, obj):
        if isinstance(obj.target, Post):
            return {
                'id': obj.target.id,
                'title': obj.target.title,
                'content': obj.target.content,
                'created_at': obj.target.created_at,
            }
        return None
