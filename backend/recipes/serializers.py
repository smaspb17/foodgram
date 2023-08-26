# from datetime import date
# # from django.utils import timezone
# from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import (
    # CharField,
    # DateField,
    ModelSerializer,
    # SlugRelatedField,
    # ValidationError,
)

# from .validators import validate_user_id

from .models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
