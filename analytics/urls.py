from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ping(request):
    return Response({"ok": True, "service": "analytics"})

urlpatterns = [
    path("ping/", ping, name="analytics-ping"),
]
