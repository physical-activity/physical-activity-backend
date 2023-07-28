from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser
from trainings.models import Training

User = get_user_model()


class UserSerializer(UserSerializer):
    """
    User Serializer.
    """
    photo = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email',
                  'first_name', 'last_name', 'phone', 'photo',)


class UserCreateSerializer(UserCreateSerializer):
    """
    New User Create Serializer.
    """

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'first_name', 'password',)

    def validate_username(self, value):
        return self.initial_data.get('email', value)

    def create(self, validated_data):
        # validated_data['username'] = validated_data['email']
        return super().create(validated_data)


class TrainingSerialaizer(serializers.ModelSerializer):
    """
    Training Serialaizer.
    """

    class Meta:
        model = Training
        fields = (
            'id', 'author', 'type', 'started_at', 'finished_at',
            'distance', 'steps_num', 'completed', 'reminder', 'raiting',
        )
