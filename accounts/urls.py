from django.urls import path

from accounts.views import UserObtainTokenPairView, UserRegistrationView, FollowUserView, UnfollowUserView

app_name = 'account'

urlpatterns = [
    path('token/', UserObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('follow/<uuid:pk>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<uuid:pk>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
