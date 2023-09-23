from rest_framework import serializers
from feed.models import Post, Like, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('modified_by', 'created_by', 'date_modified')
        extra_kwargs = {
            'created_date': {'read_only': True},
        }


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        exclude = ('modified_by', 'created_by', 'date_modified')
        extra_kwargs = {
            'user': {'allow_null': True, 'required': False},
            'created_date': {'read_only': True},
        }

    def get_comments(self, obj):
        serializer = CommentSerializer(obj.comments.all().order_by('-created_date'), many=True)
        return serializer.data


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ('modified_by', 'created_by', 'date_modified')
        extra_kwargs = {
            'created_date': {'read_only': True},
        }



