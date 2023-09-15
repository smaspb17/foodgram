from django.contrib import admin

from .models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'name', 'image', 'text', 'cooking_time', 'is_favorited',
        'is_in_shopping_cart', 'tags', 'author',
    )
    list_display = (
        'id', 'name', 'author',
    )
    list_display_links = ('id', 'name',)
    list_filter = ('author', 'name', 'tags')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = (
        'name', 'measurement_unit',
    )
    list_display = (
        'id', 'name', 'measurement_unit',
    )
    list_display_links = ('id', 'name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name', 'color', 'slug',
    )
    list_display = (
        'id', 'name', 'color', 'slug',
    )
    list_display_links = ('id', 'name',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    fields = (
        'recipe', 'ingredient', 'amount',
    )
    list_display = (
        'recipe', 'ingredient', 'amount',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe')
    list_display = ('id', 'user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe')
    list_display = ('id', 'user', 'recipe',)
