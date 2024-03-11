from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "v1": reverse("api/v1/taxis:list", request=request, format=format),
        "v2": reverse("api/v2/taxis:list", request=request, format=format),
    })
