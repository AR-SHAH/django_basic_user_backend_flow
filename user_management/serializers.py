from rest_framework import serializers
from user_management.models import User
from django.contrib.auth.hashers import make_password, check_password


class UserSignUpSerializer(serializers.ModelSerializer):
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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        email = attrs.get('email')

        if not email and not username:
            raise serializers.ValidationError("Please enter username or email to login")
        elif username:
            user = User.objects.filter(username=username).exists()
            if not user:
                raise serializers.ValidationError(f"user with {username} doesn't exists")
            else:
                user = User.objects.get(username=username)
                if not check_password(password, user.password):
                    raise serializers.ValidationError(f"Please enter valid credentials")

        elif email:
            user = User.objects.filter(email=email).exists()
            if not user:
                raise serializers.ValidationError(f"user with {email} doesn't exists")
            else:
                user = User.objects.get(email=email)
                if not check_password(password, user.password):
                    raise serializers.ValidationError(f"Please enter valid credentials")
        return attrs


