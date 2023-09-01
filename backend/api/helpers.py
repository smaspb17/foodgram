from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from recipes.models import Ingredient, RecipeIngredient


def create_ingredients(self, recipe, ingredients):
    """Функция создания ингредиентов рецепта"""
    ingredient_arr = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(
            Ingredient, id=ingredient.get('id'))
        amount = ingredient.get('amount')
        ingredient_arr.append(RecipeIngredient(
            recipe=recipe,
            ingredient=current_ingredient,
            amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(ingredient_arr)


def add_recipes(request, instance, serializer_name):
    """Функция добавления рецепта в избранное/список покупок."""
    serializer = serializer_name(
        data={'user': request.user.id, 'recipe': instance.id, },
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_recipes(request, model_name, instance, error_message):
    """Функция удаления рецепта из избранного/списка покупок."""
    if not model_name.objects.filter(user=request.user,
                                     recipe=instance).exists():
        return Response({'errors': error_message},
                        status=status.HTTP_400_BAD_REQUEST)
    model_name.objects.filter(user=request.user, recipe=instance).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)