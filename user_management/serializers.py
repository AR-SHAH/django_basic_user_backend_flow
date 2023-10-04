from rest_framework import serializers
from user_management.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, help_text="This is parameter for user's first name")
    last_name = serializers.CharField(required=False, help_text="This is parameter for user's last name")
    date_of_birth = serializers.DateField(required=False, help_text="This is parameter for user's date of birth")
    profile_picture = serializers.ImageField(required=False, help_text="This is parameter for user's profile picture")
    email = serializers.EmailField(required=True, help_text="This is parameter for user's email")
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'email', 'password', 'profile_picture']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
