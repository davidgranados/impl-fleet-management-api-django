import json
import re
from datetime import date

from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from taxis.models import Taxi, Trajectory

DEFAULT_PAGE = 1
DEFAULT_LIMIT = 10


def validate_plate(plate):
    return re.match(r"^[A-Z]{3,4}-\d{4}$", plate, flags=re.IGNORECASE)


@csrf_exempt
def taxi_list(request):
    if request.method == "GET":
        page = int(request.GET.get("page", DEFAULT_PAGE))
        limit = int(request.GET.get("limit", DEFAULT_LIMIT))
        with_last_trajectory = request.GET.get("with_last_trajectory") == "true"
        with_last_trajectory_date = request.GET.get("with_last_trajectory_date") == "true"

        if with_last_trajectory and with_last_trajectory_date:
            return JsonResponse(
                {"error": "with_last_trajectory and with_last_trajectory_date cannot be used together"}, status=400
            )

        taxis_queryset = Taxi.objects.all()

        if with_last_trajectory:
            taxis_queryset = taxis_queryset.prefetch_related("trajectory_set").annotate(
                last_trajectory=Trajectory.objects.filter(taxi=models.OuterRef("pk"))
                .order_by("-date")
                .values(
                    data=models.functions.JSONObject(id="id", date="date", latitude="latitude", longitude="longitude")
                )[:1]
            )

        if with_last_trajectory_date:
            taxis_queryset = taxis_queryset.prefetch_related("trajectory_set").annotate(
                last_trajectory_date=models.Max("trajectory__date")
            )

        paginator = Paginator(taxis_queryset, limit)

        if page != DEFAULT_PAGE and page > paginator.num_pages:
            return JsonResponse({"error": "page out of range"}, status=400)

        taxis_serialized = []
        for taxi in paginator.page(page):
            taxi_serialized = {"id": taxi.id, "plate": taxi.plate}
            if with_last_trajectory:
                taxi_serialized["last_trajectory"] = taxi.last_trajectory
            if with_last_trajectory_date:
                taxi_serialized["last_trajectory_date"] = taxi.last_trajectory_date
            taxis_serialized.append(taxi_serialized)

        next_page = paginator.page(page).next_page_number() if paginator.page(page).has_next() else None
        previous_page = paginator.page(page).previous_page_number() if paginator.page(page).has_previous() else None

        response = {
            "results": taxis_serialized,
            "total_results": paginator.count,
            "results_per_page": limit,
            "current_page": page,
            "total_pages": paginator.num_pages,
            "next_page": next_page,
            "previous_page": previous_page,
        }

        return JsonResponse(response)

    if request.method == "POST":
        try:
            body_serialized = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid body"}, status=400)
        if "plate" not in body_serialized:
            return JsonResponse({"error": "plate is required"}, status=400)
        if not validate_plate(body_serialized["plate"]):
            return JsonResponse({"error": "plate must have the format ABCD-1234"}, status=400)

        taxi = Taxi(plate=body_serialized["plate"].upper())
        taxi.save()
        taxi.refresh_from_db()
        taxi_serialized = {"id": taxi.id, "plate": taxi.plate}
        return JsonResponse(taxi_serialized, status=201)
    else:
        return HttpResponse(status=405)


@csrf_exempt
def taxi_detail(request, pk):
    try:
        taxi = Taxi.objects.get(pk=pk)
    except Taxi.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        return JsonResponse({"id": taxi.id, "plate": taxi.plate})

    if request.method == "PATCH":
        try:
            body_serialized = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid body"}, status=400)
        valid_fields = ["plate"]
        for field in body_serialized:
            if field not in valid_fields:
                return JsonResponse({"error": f"{field} is not a valid field"}, status=400)
            value = body_serialized[field]
            if field == "plate":
                if not validate_plate(body_serialized[field]):
                    return JsonResponse({"error": "plate must have the format ABCD-1234"}, status=400)
                value = value.upper()
            setattr(taxi, field, value)
        taxi.save()
        taxi.refresh_from_db()
        taxi_serialized = {"id": taxi.id, "plate": taxi.plate}
        return JsonResponse(taxi_serialized)

    if request.method == "PUT":
        try:
            body_serialized = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "invalid body"}, status=400)
        if "plate" not in body_serialized:
            return JsonResponse({"error": "plate is required"}, status=400)
        if not validate_plate(body_serialized["plate"]):
            return JsonResponse({"error": "plate must have the format ABCD-1234"}, status=400)
        taxi.plate = body_serialized["plate"].upper()
        taxi.save()
        taxi.refresh_from_db()
        taxi_serialized = {"id": taxi.id, "plate": taxi.plate}
        return JsonResponse(taxi_serialized)

    if request.method == "DELETE":
        taxi.delete()
        return HttpResponse(status=204)

    else:
        return HttpResponse(status=405)


def taxi_detail_trajectories_handler(request, taxi):
    if request.method == "GET":
        page = int(request.GET.get("page", DEFAULT_PAGE))
        limit = int(request.GET.get("limit", DEFAULT_LIMIT))
        string_date = request.GET.get("date")

        iso_date = None
        if string_date:
            try:
                iso_date = date.fromisoformat(string_date)
            except ValueError:
                return JsonResponse({"error": "date must be in the format YYYY-MM-DD"}, status=400)

        trajectories_queryset = taxi.trajectory_set.all()

        if iso_date:
            trajectories_queryset = trajectories_queryset.filter(date__date=iso_date)

        paginator = Paginator(trajectories_queryset, limit)

        if page != DEFAULT_PAGE and page > paginator.num_pages:
            return JsonResponse({"error": "page out of range"}, status=400)

        trajectories_serialized = [
            {
                "id": trajectory.id,
                "date": trajectory.date,
                "latitude": trajectory.latitude,
                "longitude": trajectory.longitude,
            }
            for trajectory in paginator.page(page)
        ]

        next_page = paginator.page(page).next_page_number() if paginator.page(page).has_next() else None
        previous_page = paginator.page(page).previous_page_number() if paginator.page(page).has_previous() else None

        response = {
            "results": trajectories_serialized,
            "total_results": paginator.count,
            "results_per_page": limit,
            "current_page": page,
            "total_pages": paginator.num_pages,
            "next_page": next_page,
            "previous_page": previous_page,
        }

        return JsonResponse(response)

    else:
        return HttpResponse(status=405)


@csrf_exempt
def taxi_pk_trajectories(request, pk):
    try:
        taxi = Taxi.objects.get(pk=pk)
    except Taxi.DoesNotExist:
        return HttpResponse(status=404)

    return taxi_detail_trajectories_handler(request, taxi)


@csrf_exempt
def taxi_plate_trajectories(request, plate):
    try:
        taxi = Taxi.objects.get(plate=plate)
    except Taxi.DoesNotExist:
        return HttpResponse(status=404)

    return taxi_detail_trajectories_handler(request, taxi)
