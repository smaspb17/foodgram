from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from users.models import Subscribe

UserModel = get_user_model()


class UserGetSerializer(ModelSerializer):
    """Получение автора"""
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        current_author = obj
        return Subscribe.objects.filter(
            user=current_user, author=current_author
        ).exists()

    class Meta:
        model = UserModel
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )


class SubscribeListSerializer(UserGetSerializer):
    """"Получение подписок пользователей."""
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = UserModel
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        from api.serializers import RecipeViewSerializer
        request = self.context.get('request')
        recipes_limit = None
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = obj.recipes.all()
        return RecipeViewSerializer(recipes, many=True,
                                    context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class SubscribeSerializer(ModelSerializer):
    """Подписка/отписка от пользователей."""
    class Meta:
        model = Subscribe
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscribe.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if request.user == data['author']:
            raise ValidationError(
                'Нельзя подписываться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscribeListSerializer(
            instance.author, context={'request': request}
        ).data
