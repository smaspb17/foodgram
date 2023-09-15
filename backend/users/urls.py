from django.urls import path, include

from api.views import (
    SubscribeListViewSet,
    SubscribeViewSet,
)


urlpatterns = [
    path('users/subscriptions/', SubscribeListViewSet.as_view(
        {'get': 'list'})),
    path('users/<int:user_id>/subscribe/', SubscribeViewSet.as_view(
        {'post': 'create', 'delete': 'destroy'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
