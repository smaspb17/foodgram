from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()

router.register(
    prefix='tags',
    viewset=TagViewSet,
    basename='tags',
)
router.register(
    prefix='ingredients',
    viewset=IngredientViewSet,
    basename='ingredients',
)
router.register(
    prefix='recipes',
    viewset=RecipeViewSet,
    basename='recipes',
)

urlpatterns = [
    path('', include(router.urls)),
]
