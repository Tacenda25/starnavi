from django.urls import re_path, path
from .views import (
    PostCreationAPIView,
    PostLikeAPIView,
    PostUnlikeAPIView
)


urlpatterns = [
    path('create/', PostCreationAPIView.as_view(), name='Post create'),
    re_path(r'^(?P<id>[0-9]+)/like$', PostLikeAPIView.as_view()),
    re_path(r'^(?P<id>[0-9]+)/unlike$', PostUnlikeAPIView.as_view())
]
