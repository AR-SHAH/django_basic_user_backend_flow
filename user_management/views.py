from user_management.models import User
from user_management.serializers import UserSignUpSerializer, UserLoginSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.db.models import Q


class UserSignUp(APIView):
    """
    List all users, or create a new user.
    """

    # Fixme Confirm is it required or not?
    # def get(self, request, format=None):
    #     snippets = User.objects.all()
    #     serializer = UserSerializer(snippets, many=True)
    #     return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UserSignUpSerializer,
        responses={status.HTTP_201_CREATED: UserSignUpSerializer()},
    )
    def post(self, request, format=None):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogIn(APIView):
    authentication_classes = (TokenAuthentication,)

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={status.HTTP_201_CREATED: UserLoginSerializer()},
    )
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(
                Q(username=serializer.validated_data.get('username')) | Q(email=serializer.validated_data.get('email'))
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
