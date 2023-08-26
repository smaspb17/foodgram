# from django.http import Http404
# from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
# from rest_framework.mixins import (
#     CreateModelMixin,
#     DestroyModelMixin,
#     ListModelMixin,
#     RetrieveModelMixin,
#     UpdateModelMixin,
# )
from rest_framework.permissions import IsAdminUser  # AllowAny
from rest_framework.viewsets import (
    # GenericViewSet,
    # ModelViewSet,
    ReadOnlyModelViewSet,
)

from .models import Tag
# from .permissions import IsAdminOrReadOnly
from .serializers import (
    TagSerializer,
    # QuestionSerializer,
    # ResultViewSerializer,
    # SurveySerializerAdmin,
    # SurveySerializerPublic,
    # VariantSerializer,
)
# from .validators import validate_user_id


@extend_schema(tags=["Рецепты"])
@extend_schema_view(
    list=extend_schema(
        summary='Список тэгов'
    ),
    retrieve=extend_schema(
        summary='Деталка тэга'
    ),
)
class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminUser,)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('is_active',)
    # http_method_names = ('get',)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # def get_queryset(self):
    #     if self.request.user.is_superuser:
    #         return Survey.objects.all()
    #     return Survey.objects.filter(is_active=True)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    # def get_serializer_class(self):
    #     if self.request.user.is_superuser:
    #         return SurveySerializerAdmin
    #     return SurveySerializerPublic