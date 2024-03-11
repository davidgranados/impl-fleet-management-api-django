from django.urls import path

from taxis.api.v2.views import taxi_list, taxi_detail

urlpatterns = [
    path("", taxi_list, name="list"),
    path("<int:pk>", taxi_detail, name="detail"),
]
