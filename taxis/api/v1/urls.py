from django.urls import path

from taxis.api.v1.views import (
    taxi_list,
    taxi_detail,
    taxi_pk_trajectories,
    taxi_plate_trajectories,
)

urlpatterns = [
    path("/taxis", taxi_list, name="taxis_list"),
    path("/taxis/<int:pk>", taxi_detail, name="taxis_detail"),
    path("/taxis/<int:pk>/trajectories", taxi_pk_trajectories, name="taxis_pk_trajectories"),
    path("/taxis/<str:plate>/trajectories", taxi_plate_trajectories, name="taxis_plate_trajectories"),
]
