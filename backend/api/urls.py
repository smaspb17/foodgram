from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet
)
from users.urls import urlpatterns as user_urls

app_name = 'api'
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

urlpatterns = []
urlpatterns += [
    path('', include(router.urls)),
]
urlpatterns += user_urls
