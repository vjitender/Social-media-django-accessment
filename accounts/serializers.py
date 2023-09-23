from django.contrib.auth import authenticate
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import CustomUser, UserProfile


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username_or_email'

    def validate(self, attrs):
        user_objs = CustomUser.objects.filter(email=attrs.get(self.username_field)) or CustomUser.objects.filter(
            username=attrs.get(self.username_field))

        if user_objs.exists():
            password = attrs.get('password')
            credentials = {
                'username': user_objs.last().username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user is None:
                    msg = {'password': "Please enter a valid password"}
                    raise ValidationError(code=status.HTTP_400_BAD_REQUEST, detail=msg)

                refresh = self.get_token(user)

                data = {
                    'success': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user.id
                }
                return data

            else:
                msg = f'Must include "{self.username_field}" and "password".'
                msg = msg.format(username_field=self.username_field)
                raise ValidationError(code=status.HTTP_400_BAD_REQUEST, detail=msg)

        else:
            msg = {'username_or_email': 'Account with this email/username does not exists'}
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, detail=msg)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Adding custom claims here
        token['username'] = user.username
        return token

    def user_can_authenticate(self, user):
        return getattr(user, 'is_active', None)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {'allow_null': True, 'required': False}
        }


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user


class UserFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('followers', )
