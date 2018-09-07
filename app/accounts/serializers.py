import time
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    ValidationError
)
from rest_framework.status import HTTP_201_CREATED


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password'
        )
        extra_kwargs = {
            'password':
                {'write_only': True}
        }

    def create(self, validated_data, verify=None, person_info=None):
        """
        If need to verify email address pass verify parameter as True.
        """
        # Avoid circular dependencies
        from accounts.views import (
            get_additional_data_about_user,
            verify_existence_email
        )

        username = validated_data['username']
        email = validated_data['email']

        if verify:
            if verify_existence_email(email):
                pass
            else:
                raise ValidationError('Email address not verifying.')

        if person_info:
            user_information = get_additional_data_about_user(email)
            if user_information is False:
                pass
            else:
                # TODO
                # Save additional information abou user
                pass

        # Checkin
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        token = Token.objects.create(user=user_obj)
        return validated_data


class UserLoginSerializer(ModelSerializer):
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )
        extra_kwargs = {
            'password':
                {'write_only': True}
        }

    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        password = data['password']
        if not username:
            raise ValidationError("A username and email is required to login.")
        user = User.objects.filter(Q(username=username)).distinct()
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This user or email is not valid.")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials, please try again.")
        user_id = user_obj.id
        return data
