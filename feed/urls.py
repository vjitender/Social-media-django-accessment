from django.urls import path
from feed.views import PostListCreateAPIView, PostDetailView, LikeCreateView, CommentCreateView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<uuid:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('like/', LikeCreateView.as_view(), name='like-create'),
    path('comment/', CommentCreateView.as_view(), name='comment-create'),
]
