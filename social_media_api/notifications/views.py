# notifications/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from rest_framework.permissions import IsAuthenticated

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
        unread_notifications = notifications.filter(read=False)
        
        unread_notifications.update(read=True)
        
        from .serializers import NotificationSerializer
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        notification = Notification.objects.get(pk=pk)
        if notification.recipient != request.user:
            return Response({"detail": "You can't mark this notification as read."}, status=status.HTTP_403_FORBIDDEN)

        notification.read = True
        notification.save()

        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
