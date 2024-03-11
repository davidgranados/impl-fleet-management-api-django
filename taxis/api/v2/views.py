from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from taxis.models import Taxi
from taxis.api.v2.serializers import TaxiSerializer


@api_view(["GET", "POST"])
def taxi_list(request, format=None):
    if request.method == "GET":
        taxis = Taxi.objects.all()
        serializer = TaxiSerializer(taxis, many=True, context={"request": request})
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TaxiSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "PUT", "DELETE"])
def taxi_detail(request, pk, format=None):
    try:
        taxi = Taxi.objects.get(pk=pk)
    except Taxi.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TaxiSerializer(taxi, context={"request": request})
        return Response(serializer.data)

    elif request.method in ["PATCH", "PUT"]:
        data = JSONParser().parse(request)
        serializer = TaxiSerializer(taxi, data=data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == "DELETE":
        taxi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
