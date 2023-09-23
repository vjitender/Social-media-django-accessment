from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import CustomUser, UserProfile


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = '/accounts/register/'
        self.valid_payload = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'profile': {
                'first_name': 'Test',
                'last_name': 'User'
            }
        }

    def test_valid_registration(self):
        response = self.client.post(self.registration_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'testuser')

    def test_invalid_registration_missing_required_field(self):
        invalid_payload = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.registration_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_existing_username(self):
        CustomUser.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(self.registration_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_existing_email(self):
        CustomUser.objects.create_user(username='existinguser', password='testpassword', email='test@example.com')
        response = self.client.post(self.registration_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FollowUnfollowUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = CustomUser.objects.create_user(username='user1', password='password1', email='test1@example.com')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password2', email='test2@example.com')
        self.user1_profile = UserProfile.objects.create(user=self.user1)
        self.user2_profile = UserProfile.objects.create(user=self.user2)
        self.follow_url = f'/accounts/follow/{self.user2.id}/'
        self.unfollow_url = f'/accounts/unfollow/{self.user2.id}/'
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        response = self.client.post(self.follow_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user2_profile.followers.filter(id=self.user1.id).exists())

    def test_unfollow_user(self):
        self.user2_profile.followers.add(self.user1)
        response = self.client.delete(self.unfollow_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user2_profile.followers.filter(id=self.user1.id).exists())
