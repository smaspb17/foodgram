from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import HttpResponse, get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from .helpers import add_recipes, delete_recipes
from .filters import RecipeFilter
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    ShoppingCart,
)
# from .permissions import IsAdminOrReadOnly
from .serializers import (
    FavoriteSerializer,
    IngredientViewSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


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
    permission_classes = (IsAdminUser,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientViewSerializer


@extend_schema(tags=["Рецепты"])
@extend_schema_view(
    list=extend_schema(summary='Список рецептов'),
    retrieve=extend_schema(summary='Получение рецепта'),
    create=extend_schema(summary='Создание рецепта'),
    partial_update=extend_schema(summary='Обновление рецепта'),
    destroy=extend_schema(summary='Удаление рецепта'),
)
class RecipeViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return RecipeGetSerializer
        return RecipePostSerializer

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Удаление/добавление в список покупок."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return add_recipes(request, recipe,
                               ShoppingCartSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в списке покупок'
            return delete_recipes(request, ShoppingCart,
                                  recipe, error_message)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Удаление/добавление в Избранное."""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return add_recipes(request, recipe, FavoriteSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет данного рецепта в Избранном'
            return delete_recipes(request, Favorite,
                                  recipe, error_message)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
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
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = \
            'attachment; filename="shopping_cart.txt"'
        return response
