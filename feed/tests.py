from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import CustomUser, UserProfile
from feed.models import Post, Like, Comment
from feed.serializers import PostSerializer, LikeSerializer, CommentSerializer


class PostListCreateAPIViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/feed/posts/'
        self.valid_payload = {
            'content': 'This is a test post content.'
        }
        self.user1 = CustomUser.objects.create_user(username='user1', password='password1', email='test1@example.com')
        self.user1_profile = UserProfile.objects.create(user=self.user1)
        self.client.force_authenticate(user=self.user1)

    def test_list_posts(self):
        # Create some sample posts
        Post.objects.create(content='Content 1', user=self.user1)
        Post.objects.create(content='Content 2', user=self.user1)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data matches the created posts
        # posts = Post.objects.all()
        # serializer = PostSerializer(posts, many=True)
        # self.assertEqual(response.data, serializer.data)

    def test_create_post(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify a new post object is created in the database
        self.assertEqual(Post.objects.count(), 1)

        # Verify the response data matches the created post
        post = Post.objects.get()
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)

    def test_create_post_invalid_data(self):
        # Send a POST request with invalid data (missing title)
        invalid_payload = {}
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Verify no new post object is created in the database
        self.assertEqual(Post.objects.count(), 0)


class PostDetailViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = CustomUser.objects.create_user(username='user1', password='password1', email='test1@example.com')
        self.user1_profile = UserProfile.objects.create(user=self.user1)

        self.post = Post.objects.create(content='This is a test post content.', user=self.user1)
        self.url = f'/feed/posts/{self.post.id}/'
        self.valid_payload = {
            'content': 'This is the updated post content.'
        }
        self.client.force_authenticate(user=self.user1)

    def test_retrieve_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response data matches the retrieved post
        serializer = PostSerializer(self.post)
        self.assertEqual(response.data, serializer.data)

    def test_update_post(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the post from the database
        self.post.refresh_from_db()

        # Verify the post has been updated
        self.assertEqual(self.post.content, self.valid_payload['content'])

        # Verify the response data matches the updated post
        serializer = PostSerializer(self.post)
        self.assertEqual(response.data, serializer.data)

    def test_delete_post(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the post has been deleted from the database
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())


class LikeCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(content='This is a test post content.', user=self.user)
        self.url = f'/feed/like/'
        self.valid_payload = {'user': self.user.id, 'post': self.post.id}

    def test_create_like(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify a new like object is created in the database
        self.assertEqual(Like.objects.count(), 1)

        # Verify the response data matches the created like
        like = Like.objects.get()
        serializer = LikeSerializer(like)
        self.assertEqual(response.data, serializer.data)

    def test_create_like_unauthenticated(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Like.objects.count(), 0)

    def test_create_like_duplicate(self):
        self.client.force_authenticate(user=self.user)
        Like.objects.create(user=self.user, post=self.post)  # Create a duplicate like
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)

    def test_create_like_missing_fields(self):
        self.client.force_authenticate(user=self.user)
        invalid_payload = {'user': self.user.id}  # Missing 'post' field
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 0)


class CommentCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(content='This is a test post content.', user=self.user)
        self.url = f'/feed/comment/'
        self.valid_payload = {'user': self.user.id, 'post': self.post.id, 'content': 'Test comment content'}

    def test_create_comment(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify a new comment object is created in the database
        self.assertEqual(Comment.objects.count(), 1)

        # Verify the response data matches the created comment
        comment = Comment.objects.get()
        serializer = CommentSerializer(comment)
        self.assertEqual(response.data, serializer.data)

    def test_create_comment_unauthenticated(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), 0)

    def test_create_comment_missing_fields(self):
        self.client.force_authenticate(user=self.user)
        invalid_payload = {'user': self.user.id, 'post': self.post.id}
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)
