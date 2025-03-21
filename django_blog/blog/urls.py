from django.urls import path
from .views import ( register_view, login_view, logout_view, profile_view, profile_update_view, tagged_posts, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView, PostByTagListView, SearchResultsView )

urlpatterns = [

    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/update/", profile_update_view, name="profile_update"),

    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="add_comment"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='post_by_tag'),
    path('search/', SearchResultsView.as_view(), name='search_results'),  # ✅ Add this if missing

]