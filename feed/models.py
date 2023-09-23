from django.db import models
from accounts.models import CustomUser
from social_media_assignment.base_models import BaseModel


class Post(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='file/', blank=True, null=True)

    class Meta:
        """
        to set table name in database
        """
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class Like(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        """
        to set table name in database
        """
        verbose_name = 'like'
        verbose_name_plural = 'likes'
        unique_together = ('user', 'post')


class Comment(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()

    class Meta:
        """
        to set table name in database
        """
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
