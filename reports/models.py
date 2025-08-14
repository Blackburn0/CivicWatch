from django.conf import settings
from django.db import models


class Incident(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_REVIEW = "in_review", "In Review"
        RESOLVED = "resolved", "Resolved"
        REJECTED = "rejected", "Rejected"

    class Category(models.TextChoices):
        ROAD = "road", "Road / Potholes"
        ELECTRICITY = "electricity", "Electricity / Streetlights"
        WATER = "water", "Water / Drainage"
        SANITATION = "sanitation", "Sanitation / Waste"
        SAFETY = "safety", "Public Safety"
        OTHER = "other", "Other"

    title = models.CharField(max_length=180)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=Category.choices, default=Category.OTHER)

    city = models.CharField(max_length=120, blank=True, default="")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    image_url = models.URLField(blank=True, default="")

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="incidents"
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.status})"


class StatusHistory(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="history")
    old_status = models.CharField(max_length=20, choices=Incident.Status.choices)
    new_status = models.CharField(max_length=20, choices=Incident.Status.choices)
    comment = models.TextField(blank=True, default="")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return f"{self.incident} {self.old_status} → {self.new_status}"
