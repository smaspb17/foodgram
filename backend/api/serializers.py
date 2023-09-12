import base64
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ImageField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    ValidationError,
)

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import Subscribe

User = get_user_model()


class Base64ImageField(ImageField):
    """Декодирование изображений из формата base64."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(ModelSerializer):
    """Работа с тегами"""
    class Meta:
        model = Tag
        fields = '__all__'


class UserGetSerializer(ModelSerializer):
    """Получение автора"""
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user
        if isinstance(current_user, User):
            current_author = obj
            if Subscribe.objects.filter(
                user=current_user, author=current_author
            ).exists():
                return True
        return False

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',)


class IngredientViewSerializer(ModelSerializer):
    """Просмотр списка ингредиентов (ингредиента)."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientGetSerializer(ModelSerializer):
    """Получение данных об ингредиентах в рецептах."""
    id = IntegerField(source='ingredient.id', read_only=True)
    name = CharField(source='ingredient.name', read_only=True)
    measurement_unit = CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientPostSerializer(ModelSerializer):
    """Добавление ингредиентов при создании рецепта."""
    id = IntegerField()
    amount = IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeGetSerializer(ModelSerializer):
    """Просмотр рецептов(а)."""
    image = Base64ImageField(required=False)
    author = UserGetSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientGetSerializer(many=True, read_only=True,
                                          source='recipe_ingredients')
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time',)
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Favorite.objects.filter(
                    user=request.user, recipe=obj
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and ShoppingCart.objects.filter(
                    user=request.user, recipe=obj
                ).exists())


class RecipePostSerializer(ModelSerializer):
    """Создание/обновление/удаление рецепта"""
    image = Base64ImageField()
    ingredients = IngredientPostSerializer(
        many=True,
        source='recipe_ingredients'
    )
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                  many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        ingredients_list = []
        for ingredient in data.get('recipe_ingredients'):
            if ingredient.get('amount') > 10000 or \
                    ingredient.get('amount') < 1:
                raise ValidationError(
                    'Количество ингредиента должно быть от 1 до 10000'
                )
            ingredients_list.append(ingredient.get('id'))
        if len(set(ingredients_list)) != len(ingredients_list):
            raise ValidationError(
                'Нельзя добавить в рецепт два одинаковых ингредиента'
            )
        return data

    def create_ingredients(self, recipe, ingredients):
        """Создание ингредиентов рецепта"""
        ingredient_arr = []
        for ingredient in ingredients:
            current_ingredient = get_object_or_404(
                Ingredient, id=ingredient.get('id'))
            amount = ingredient.get('amount')
            ingredient_arr.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=amount
                    )
                )
        RecipeIngredient.objects.bulk_create(ingredient_arr)

    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('recipe_ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        super().update(instance, validated_data)
        self.create_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeGetSerializer(
            instance,
            context={'request': request}
        ).data


class RecipeViewSerializer(ModelSerializer):
    """Получение краткой информации о рецепте."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(ModelSerializer):
    """Избранные рецепты."""
    class Meta:
        model = Favorite
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в Избранном'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeViewSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class ShoppingCartSerializer(ModelSerializer):
    """Список покупок."""
    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже в Списке покупок'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeViewSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class UserSignUpSerializer(UserCreateSerializer):
    """Регистрация пользователя."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class SubscribeListSerializer(UserGetSerializer):
    """"Получение подписок пользователей."""
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        print(request)
        recipes_limit = None
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = obj.recipes.all()
        return RecipeViewSerializer(recipes, many=True,
                                    context={'request': request}).data

    def get_recipes_count(self, obj):
        print(f'кол-во: {obj.recipes.count()}')
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
