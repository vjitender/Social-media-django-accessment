from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import UserTokenObtainPairSerializer, UserSerializer, UserFollowSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from accounts.models import CustomUser, UserProfile


class UserObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUserView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserFollowSerializer

    def create(self, request, *args, **kwargs):
        user_to_follow = CustomUser.objects.get(pk=kwargs['pk'])

        if user_to_follow != self.request.user:
            user_to_follow.profile.followers.add(self.request.user)
            return Response({"message": "Followed successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class UnfollowUserView(generics.DestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserFollowSerializer

    def destroy(self, request, *args, **kwargs):
        user_to_unfollow = CustomUser.objects.get(pk=self.kwargs['pk'])
        user_to_unfollow.profile.followers.remove(request.user)
        return Response({"message": "User unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)
