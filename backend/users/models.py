from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_username, validate_email

UserModel = get_user_model()
UserModel._meta.get_field('username').validators.append(validate_username)
UserModel._meta.get_field('email').validators.append(validate_email)


class Subscribe(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='authors',
        verbose_name='Автор рецепта'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Пользователь {self.user} подписан на автора {self.author}'
