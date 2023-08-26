from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=64,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
    )


class Ingredient(models.Model):
    CHOICES = [
        ('г', 'г'),
        ('мл', 'мл'),
        ('шт.', 'шт.'),
        ('ст. л.', 'ст. л.'),
        ('ч. л.', 'ч. л.'),
        ('батон', 'батон'),
        ('банка', 'банка'),
        ('бутылка', 'бутылка'),
        ('веточка', 'веточка'),
        ('горсть', 'горсть'),
        ('долька', 'долька'),
        ('звездочка', 'звездочка'),
        ('зубчик', 'зубчик'),
        ('капля', 'капля'),
        ('кусок', 'кусок'),
        ('лист', 'лист'),
        ('пакет', 'пакет'),
        ('пакетик', 'пакетик'),
        ('пачка', 'пачка'),
        ('пласт', 'пласт'),
        ('по вкусу', 'по вкусу'),
        ('пучок', 'пучок'),
        ('стакан', 'стакан'),
        ('стебель', 'стебель'),
        ('стручок', 'стручок'),
        ('тушка', 'тушка'),
        ('упаковка', 'упаковка'),
        ('щепотка', 'щепотка'),
    ]
    name = models.CharField(
        verbose_name='Название',
        max_length=255,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=255,
        choices=CHOICES,
    )


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=64,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/images/',
        help_text='Загрузите картинку'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Опишите рецепт',
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления в минутах',
        help_text='Введите количество минут',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранных'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тэги')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество ингредиента'
    )


# class Favorite(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='users',
#         verbose_name='Пользователь'
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipes',
#         verbose_name='Рецепт'
#     )
