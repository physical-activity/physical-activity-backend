from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from trainings.models import Training, TrainingType
from users.models import CustomUser

User = get_user_model()


class UserSerializer(UserSerializer):
    """User Serializer."""

    photo = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email',
                  'first_name', 'last_name', 'phone', 'photo',)


class UserCreateSerializer(UserCreateSerializer):
    """New User Create Serializer."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'first_name', 'password',)

    def validate_username(self, value):
        return self.initial_data.get('email', value)

    def create(self, validated_data):
        return super().create(validated_data)


class TrainingSerialaizer(serializers.ModelSerializer):
    """Training Serialaizer."""
    author = serializers.ReadOnlyField(source='author.email')
    training_type = serializers.ReadOnlyField(source='type.name')

    class Meta:
        model = Training
        fields = (
            'id', 'author', 'training_type', 'started_at', 'finished_at',
            'distance', 'steps_num', 'completed', 'reminder', 'raiting',
        )

    def validate(self, data):
        if self.context.get('request').stream.method == 'PATCH':
            if not self.initial_data.get('training_type'):
                self.initial_data['training_type'] = self.instance.type.name
            if not self.initial_data.get('started_at'):
                self.initial_data[
                    'started_at'] = self.instance.started_at.isoformat()
        if not (training_type_name := self.initial_data.get('training_type')):
            raise serializers.ValidationError(
                'Тип тренировки должен быть указан.'
            )
        if not (started_at := self.initial_data.get('started_at')):
            raise serializers.ValidationError(
                'Время начала тренировки должно быть указано.'
            )
        if not self.instance and not self.initial_data.get('finished_at'):
            data['finished_at'] = started_at
        if (
            (finished_at := self.initial_data.get('finished_at'))
            and finished_at < started_at
        ):
            raise serializers.ValidationError(
                'Конец тренировки не может быть раньше её начала.'
            )
        data['author'] = self.context.get('request').user
        try:
            data['type'] = TrainingType.objects.get(name=training_type_name)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Такого типа тренировки не существует.'
            )
        return super().validate(data)


class TrainingTypeSerializer(serializers.ModelSerializer):
    """Training Type Serializer."""

    class Meta:
        model = TrainingType
        fields = ('name', )
