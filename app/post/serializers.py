from django.contrib.auth.models import User
from post.models import Post
from rest_framework.serializers import (
    CharField,
    Field,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    IntegerField
)


class PostCreationSerializer(ModelSerializer):
    text = CharField(required=True, allow_blank=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
        )

    def validate(self, data):
        user = self.context['request'].user
        text = data.get('text', None)
        if not text:
            raise ValidationError('Text field is required.')
        post = Post.objects.create(owner=user, text=text)
        data.update({'id': post.id})
        return data


class PostLikeSerializer(ModelSerializer):
    like = IntegerField()

    class Meta:
        model = Post
        fields = {
            'like'
        }
    def validate(self, data):
        pass

class PostUnlikeSerializer(ModelSerializer):
    pass
