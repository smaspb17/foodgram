from django.contrib import admin

from .models import Favorite, Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'name', 'image', 'text', 'cooking_time', 'is_favorited',
        'is_in_shopping_cart', 'tags',
    )
    # readonly_fields = ('start_date',)
    list_display = (
        'id', 'name', 'author', 'is_favorited', 'is_in_shopping_cart',
    )
    list_display_links = ('id', 'name',)
    list_editable = ('is_favorited', 'is_in_shopping_cart',)
    list_filter = ('author', 'name', 'tags')
    # search_fields = ('name',)


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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = ('user', 'recipe')
    list_display = ('id', 'user', 'recipe',)
