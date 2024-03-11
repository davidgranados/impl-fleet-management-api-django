from django.urls import path, include

from taxis.api.v1.urls import urlpatterns as taxi_urls
from config.views import api_root

urlpatterns = [
    path("", api_root, name="root"),
    path("v1", include((taxi_urls, "v1"), namespace="api/v1")),
]
