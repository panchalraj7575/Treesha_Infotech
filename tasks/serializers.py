from rest_framework import serializers
from .models import Task
from datetime import date


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for validating and handling Task data."""

    class Meta:
        model = Task
        fields = "__all__"

    def validate_priority(self, value):
        allowed = ["LOW", "MEDIUM", "HIGH"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Invalid priority. Allowed values: {allowed}"
            )
        return value

    def validate_status(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Status must be true or false")
        return value

    def validate_due_date(self, value):
        if value is not None and value <= date.today():
            raise serializers.ValidationError(
                "Due date must be greater than today's date"
            )
        return value
