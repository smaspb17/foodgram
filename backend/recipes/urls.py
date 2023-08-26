from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()

router.register(
    prefix='tags',
    viewset=TagViewSet,
    basename='tags',
)
# router.register(r'dicts/statuses/breaks', dicts.BreakStatusView, 'breaks-statuses')
# router.register(r'dicts/statuses/replacements', dicts.ReplacementStatusView, 'replacement-statuses')

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('breaks/replacements/<int:pk>/member/', replacements.MeReplacementMemberView.as_view(), name='replacement-member'),
#     path('breaks/replacements/<int:pk>/break/', breaks.BreakMeView.as_view(), name='break-me'),

#     path('breaks/', include(router.urls)),
# ]
