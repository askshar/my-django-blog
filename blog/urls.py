from django.urls import path
from .views import (
    PostListView, PostCreateView,
    PostUpdateView, PostDeleteView,
    UserPostListView, post_detail_view,
    update_comment, delete_comment
)

urlpatterns = [
    path('', PostListView.as_view(), name="index"),
    path('user/<str:username>/', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:post_id>/', post_detail_view, name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('post/<int:post_id>/comment/<int:comment_id>/', update_comment, name="update-comment"),
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', delete_comment, name="delete-comment"),
]