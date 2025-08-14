from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from .models import Incident
from .serializers import (
    IncidentCreateSerializer,
    IncidentReadSerializer,
    IncidentStatusUpdateSerializer,
    StatusHistorySerializer,
)
from users.permissions import IsAdminRole


class IncidentViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentReadSerializer

    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            return [AllowAny()]
        if self.action in ["update_status"]:
            return [IsAdminRole()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == "create":
            return IncidentCreateSerializer
        if self.action == "update_status":
            return IncidentStatusUpdateSerializer
        if self.action == "history":
            return StatusHistorySerializer
        return IncidentReadSerializer

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        status_q = request.query_params.get("status")
        category = request.query_params.get("category")
        city = request.query_params.get("city")
        date_from = request.query_params.get("from")
        date_to = request.query_params.get("to")
        ordering = request.query_params.get("ordering")

        if status_q:
            qs = qs.filter(status=status_q)
        if category:
            qs = qs.filter(category=category)
        if city:
            qs = qs.filter(city__iexact=city)
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        if ordering in ("created_at", "-created_at"):
            qs = qs.order_by(ordering)

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(qs, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["put"], url_path="status")
    def update_status(self, request, pk=None):
        """Admin-only: update incident status & log history"""
        incident = self.get_object()
        ser = self.get_serializer(data=request.data, context={"request": request, "incident": incident})
        ser.is_valid(raise_exception=True)
        updated_incident = ser.save()
        return Response(IncidentReadSerializer(updated_incident).data)

    @action(detail=True, methods=["get"], url_path="history", permission_classes=[IsAdminRole])
    def history(self, request, pk=None):
        """Admin-only: get status history of an incident"""
        incident = self.get_object()
        history = incident.history.all()
        ser = self.get_serializer(history, many=True)
        return Response(ser.data)
