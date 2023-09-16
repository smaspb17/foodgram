import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()


def validate_username(value):
    existing_user = UserModel.objects.filter(username__iexact=value).exists()
    if existing_user:
        raise ValidationError(
            'Пользователь с таким именем уже существует!'
        )
    if value.lower() == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя!'
        )
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'Некорректные символы в username'
        )
    return value


def validate_email(value):
    existing_email = UserModel.objects.filter(email__iexact=value).exists()
    if existing_email:
        raise ValidationError(
            'Пользователь с таким email уже существует!'
        )
    return value
