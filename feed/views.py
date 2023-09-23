from rest_framework import generics
from feed.models import Post, Like, Comment
from feed.serializers import PostSerializer, LikeSerializer, CommentSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        users = [user.id]
        followed_to_users = user.profile.followers.all().values_list('id', flat=True).distinct()
        if followed_to_users.exists():
            users = users + list(followed_to_users)
        return Post.objects.filter(user_id__in=users).order_by('-created_date')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
