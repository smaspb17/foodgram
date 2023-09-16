from django.db.models import Sum
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import HttpResponse, get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAdminAuthorOrReadOnly
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    ShoppingCart,
)
from .serializers import (
    FavoriteSerializer,
    IngredientViewSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)
from users.models import Subscribe
from users.serializers import (
    SubscribeSerializer,
    SubscribeListSerializer,
)

UserModel = get_user_model()


@extend_schema(tags=["Теги"])
@extend_schema_view(
    list=extend_schema(
        summary='Список тегов'
    ),
    retrieve=extend_schema(
        summary='Получение тега'
    ),
)
class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


@extend_schema(tags=["Ингредиенты"])
@extend_schema_view(
    list=extend_schema(
        summary='Список ингредиентов'
    ),
    retrieve=extend_schema(
        summary='Получение ингредиента'
    ),
)
class IngredientViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Ingredient.objects.all()
    serializer_class = IngredientViewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


@extend_schema(tags=["Рецепты"])
@extend_schema_view(
    list=extend_schema(summary='Список рецептов'),
    retrieve=extend_schema(summary='Получение рецепта'),
    create=extend_schema(summary='Создание рецепта'),
    partial_update=extend_schema(summary='Обновление рецепта'),
    destroy=extend_schema(summary='Удаление рецепта'),
)
class RecipeViewSet(ModelViewSet):
    """Работа с рецептами."""
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminAuthorOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return RecipeGetSerializer
        return RecipePostSerializer

    def add_recipes(self, request, instance, serializer_name):
        """Функция добавления рецепта в избранное/список покупок."""
        serializer = serializer_name(
            data={'user': request.user.id, 'recipe': instance.id, },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipes(self, request, model_name, instance, error_message):
        """Функция удаления рецепта из избранного/списка покупок."""
        if not model_name.objects.filter(user=request.user,
                                         recipe=instance).exists():
            return Response({'errors': error_message},
                            status=status.HTTP_400_BAD_REQUEST)
        model_name.objects.filter(user=request.user, recipe=instance).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Удаление/добавление в список покупок."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_recipes(request, recipe,
                                    ShoppingCartSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет данного рецепта в Списке покупок'
            return self.delete_recipes(request, ShoppingCart,
                                       recipe, error_message)

    @action(detail=True, methods=('post', 'delete'),
            permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        """Удаление/добавление в Избранное."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_recipes(request, recipe, FavoriteSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет данного рецепта в Избранном'
            return self.delete_recipes(request, Favorite,
                                       recipe, error_message)

    @action(detail=False, methods=('get',),
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount} {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response


@extend_schema(tags=["Подписки"])
@extend_schema_view(
    create=extend_schema(summary='Создание подписки'),
    destroy=extend_schema(summary='Удаление подписки'),
)
class SubscribeViewSet(ModelViewSet):
    """Создание/удаление подписки на автора."""
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(UserModel, id=kwargs['user_id'])
        serializer = self.get_serializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(UserModel, id=kwargs['user_id'])
        user = request.user
        instance = Subscribe.objects.filter(
            author=author, user=user
        )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Подписки"])
@extend_schema_view(
    list=extend_schema(summary='Получение подписок'),
)
class SubscribeListViewSet(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """Получение подписок на автора."""
    serializer_class = SubscribeListSerializer

    def get_queryset(self):
        return UserModel.objects.filter(authors__user=self.request.user)
