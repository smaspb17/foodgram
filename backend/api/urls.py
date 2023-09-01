from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from api.spectacular.urls import urlpatterns as doc_urls

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
urlpatterns += doc_urls
urlpatterns += [path('', include(router.urls))]
