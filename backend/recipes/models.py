from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
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

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


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

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Виды ингредиентов'

    def __str__(self):
        return self.name


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
        validators=[
            MinValueValidator(
                1, 'Время приготовления не должно быть меньше 1 минуты'
            )
        ]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранных'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(
                1, 'Количество ингредиентов должно быть не менее 1'),
            MaxValueValidator(
                10000, 'Количество ингредиентов должно быть не более 10000')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_cart'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
