import clearbit
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer
)
from starnavi.settings import clearbit_key, hunter_key, hunter_api


clearbit.key = clearbit_key


def get_additional_data_about_user(email):
    """
    Additional data for the user on signup using Clearbit service.
    """

    person = clearbit.Person.find(email=email, stream=True)
    if person != None:
        return person
    else:
        return False


def verify_existence_email(email):
    """
    Verifying email existence on signup.
    """

    data = 'email-verifier?email=%s&api_key=%s' % (email, hunter_key)
    url = hunter_api + data
    resp = requests.get(url=url)
    response = resp.json()
    if 'data' in response or 'meta' in response:
        # Successful response
        # If need additional information about email verifying see response
        return True
    else:
        # Error response
        return False


class UserSignupAPIView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'},
                                status=HTTP_404_NOT_FOUND)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
