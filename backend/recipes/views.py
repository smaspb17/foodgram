# from django.http import Http404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
# from rest_framework.mixins import (
#     CreateModelMixin,
#     DestroyModelMixin,
#     ListModelMixin,
#     RetrieveModelMixin,
#     UpdateModelMixin,
# )
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import (
    # GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)

from .models import Ingredient, Recipe, Tag
# from .permissions import IsAdminOrReadOnly
from .serializers import (
    IngredientGetSerializer,
    IngredientPostSerializer,
    RecipeGetSerializer,
    RecipePostSerializer,
    TagSerializer,
)
# from .validators import validate_user_id


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
    serializer_class = IngredientPostSerializer


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

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return RecipeGetSerializer
        return RecipePostSerializer
