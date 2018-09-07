from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from rest_framework.views import APIView
from .serializers import (
    PostCreationSerializer,
    PostLikeSerializer
)
from .models import Post


@method_decorator(csrf_exempt, name='dispatch')
class PostCreationAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostCreationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PostCreationSerializer(data=data,
                                            context={'request': request})
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PostLikeAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostLikeSerializer

    def get_object(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

    def get(self, request, id):
        post = self.get_object(int(id))
        if not post:
            return Response({'error': 'There is no such post.'}, status=HTTP_404_NOT_FOUND)
        post.like += 1
        post.save()
        return Response({'success': True, 'likes': post.like}, status=HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PostUnlikeAPIView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostLikeSerializer

    def get_object(self, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None

    def get(self, request, id):
        post = self.get_object(int(id))
        if not post:
            return Response({'error': 'There is no such post.'}, status=HTTP_404_NOT_FOUND)
        if post.like == 0 or post.like <= 0:
            return Response({'error': 'You can not reduce the value.'}, status=HTTP_200_OK)
        post.like -= 1
        post.save()
        return Response({'likes': post.like}, status=HTTP_200_OK)
