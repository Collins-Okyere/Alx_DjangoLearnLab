# notifications/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification
from rest_framework import status

@api_view(['GET'])
def notification_list(request):
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    data = [{"actor": n.actor.username, "verb": n.verb, "target": str(n.target), "timestamp": n.timestamp} for n in notifications]

    return Response(data, status=status.HTTP_200_OK)
