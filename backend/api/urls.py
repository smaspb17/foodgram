# from django.urls import path, include
from api.spectacular.urls import urlpatterns as doc_urls
from recipes.urls import urlpatterns as recipes_urls

app_name = 'api'
urlpatterns = []
urlpatterns += doc_urls
urlpatterns += recipes_urls

# urlpatterns = [
#     path('auth/', include('djoser.urls.jwt')),
# ]

# from api.spectacular.urls import urlpatterns as doc_urls
# from users.urls import urlpatterns as user_urls
# from organisations.urls import urlpatterns as organisation_urls
# from breaks.urls import urlpatterns as breaks_urls



# urlpatterns += doc_urls
# urlpatterns += organisation_urls
# urlpatterns += user_urls
