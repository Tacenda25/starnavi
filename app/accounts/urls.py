from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from .views import (
    UserLoginAPIView,
    UserSignupAPIView,
)


urlpatterns = [
    path('signup/', csrf_exempt(UserSignupAPIView.as_view()), name='Signup'),
    path('login/', csrf_exempt(UserLoginAPIView.as_view()), name='Login')
]
