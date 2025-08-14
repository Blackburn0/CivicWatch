from rest_framework import serializers
from django.conf import settings
from .models import Incident, StatusHistory

CLOUDINARY_ENABLED = bool(getattr(settings, "CLOUDINARY_URL", ""))

if CLOUDINARY_ENABLED:
    try:
        import cloudinary.uploader 
    except Exception:
        CLOUDINARY_ENABLED = False

class IncidentBaseSerializer(serializers.ModelSerializer):
    reporter_username = serializers.SerializerMethodField()

    class Meta:
        model = Incident
        fields = [
            "id", "title", "description", "category",
            "city", "latitude", "longitude",
            "image_url",
            "status", "reporter", "reporter_username",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status", "reporter", "reporter_username", "created_at", "updated_at"]

    def get_reporter_username(self, obj):
        return getattr(obj.reporter, "username", None)


class IncidentCreateSerializer(serializers.ModelSerializer):
    # Allow either uploading a file or passing an existing URL
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = Incident
        fields = [
            "title", "description", "category",
            "city", "latitude", "longitude",
            "image", "image_url",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        image_file = validated_data.pop("image", None)

        # Attach reporter if authenticated; else anonymous (None)
        reporter = request.user if (request and request.user and request.user.is_authenticated) else None

        # Handle image upload (Cloudinary if configured and file provided)
        img_url = validated_data.get("image_url", "")
        if image_file is not None:
            if CLOUDINARY_ENABLED:
                uploaded = cloudinary.uploader.upload(image_file)  # noqa
                img_url = uploaded.get("secure_url") or uploaded.get("url") or img_url
            else:
                # If not using Cloudinary, you could alternatively save to MEDIA_ROOT with a FileField.
                # For now, we just ignore file saving and keep URL blank unless provided.
                pass

        incident = Incident.objects.create(
            reporter=reporter,
            image_url=img_url,
            **validated_data,
        )
        return incident


class IncidentReadSerializer(IncidentBaseSerializer):
    pass





class StatusHistorySerializer(serializers.ModelSerializer):
    changed_by_username = serializers.SerializerMethodField()

    class Meta:
        model = StatusHistory
        fields = ["id", "old_status", "new_status", "comment", "changed_by_username", "changed_at"]

    def get_changed_by_username(self, obj):
        return getattr(obj.changed_by, "username", None)


class IncidentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Incident.Status.choices)
    comment = serializers.CharField(required=False, allow_blank=True)

    def validate_status(self, value):
        # Could add rules here (e.g., no reverting to pending from resolved)
        return value

    def save(self, **kwargs):
        request = self.context.get("request")
        incident = self.context.get("incident")
        old_status = incident.status
        new_status = self.validated_data["status"]
        comment = self.validated_data.get("comment", "")

        incident.status = new_status
        incident.save()

        StatusHistory.objects.create(
            incident=incident,
            old_status=old_status,
            new_status=new_status,
            comment=comment,
            changed_by=request.user if request and request.user.is_authenticated else None,
        )
        return incident
