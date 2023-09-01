# from django.urls import path, include
from api.spectacular.urls import urlpatterns as doc_urls
from recipes.urls import urlpatterns as recipes_urls

app_name = 'api'
urlpatterns = []
urlpatterns += doc_urls
urlpatterns += recipes_urls
