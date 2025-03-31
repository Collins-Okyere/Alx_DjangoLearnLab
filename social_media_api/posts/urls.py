from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),  # Ensure accounts URLs are included
    path('api/', include('posts.urls')),  # ✅ Include posts and comments URLs
]
