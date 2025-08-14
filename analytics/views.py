from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.permissions import IsAdminRole
from reports.models import Incident

@api_view(["GET"])
@permission_classes([IsAdminRole])
def dashboard_stats(request):
    """
    Provides summary statistics for all incidents. Admin-only.
    """
    # Total count of all incidents
    total_incidents = Incident.objects.count()

    # Counts grouped by status
    status_counts_query = Incident.objects.values("status").annotate(count=Count("id"))
    status_counts = {item["status"]: item["count"] for item in status_counts_query}

    # Counts grouped by category
    category_counts_query = Incident.objects.values("category").annotate(count=Count("id"))
    category_counts = {item["category"]: item["count"] for item in category_counts_query}
    
    # Counts grouped by city (excluding empty/null city names)
    city_counts_query = (
        Incident.objects.exclude(city__exact="")
        .values("city")
        .annotate(count=Count("id"))
        .order_by("-count") # Order by most reports per city
    )
    city_counts = {item["city"]: item["count"] for item in city_counts_query}


    # Construct the final response payload
    payload = {
        "total_incidents": total_incidents,
        "by_status": status_counts,
        "by_category": category_counts,
        "by_city": city_counts,
    }

    return Response(payload)