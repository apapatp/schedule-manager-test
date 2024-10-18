from django.db import transaction
from rest_framework import serializers
from schedule_manager.models import (
    User,
    Schedule
)
from abstract.serializers import AbstractSerializer


class UserSerializer(AbstractSerializer):
    """
    Serializer for User model.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "full_name": {"read_only": True},
            "is_superuser": {"read_only": True},
        }


class ScheduleSerializer(AbstractSerializer):
    """
    Serializer for Schedule model.
    """

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    badge_ids = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    camera_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)

    class Meta:
        model = Schedule
        fields = [
            "day",
            "user",
            "start",
            "stop",
            "badge_ids",
            "camera_ids",
        ]

    def validate(self, validated_data):
        """
        Prevent user from creating a schedule that already exists and restrict badge_ids and camera_ids.
        """
        start = validated_data.get("start")
        stop = validated_data.get("stop")
        day = validated_data.get("day")
        badge_ids = validated_data.get("badge_ids")
        camera_ids = validated_data.get("camera_ids")
        user = self.context["request"].user

        # Ensure that only one of the two fields is provided
        if badge_ids and camera_ids:
            raise serializers.ValidationError("You can provide either 'badge_ids' or 'camera_ids', not both.")

        # Ensure at least one of the fields is provided
        if not badge_ids and not camera_ids:
            raise serializers.ValidationError("You must provide either 'badge_ids' or 'camera_ids'.")

        # Get all schedules that match user, day, start, and stop
        existing_schedules = Schedule.objects.filter(
            user=user,
            day=day,
            start=start,
            stop=stop,
        )

        # If we're updating, get the current instance (if applicable)
        instance = self.instance  # The current instance being updated, if any

        # Prepare a function to check for duplicates
        def has_duplicate(existing_schedule):
            if badge_ids is not None and set(existing_schedule.badge_ids) == set(badge_ids):
                return True
            if camera_ids is not None and set(existing_schedule.camera_ids) == set(camera_ids):
                return True
            return False

        for schedule in existing_schedules:
            # If we're updating, skip the instance being updated
            if instance is None or schedule.id != instance.id:
                if has_duplicate(schedule):
                    raise serializers.ValidationError("Schedule with these IDs already exists.")

        # Additional check when updating
        if instance is not None:
            # Check if we're changing the badge_ids and the existing instance has camera_ids
            if badge_ids is not None and instance.camera_ids:
                raise serializers.ValidationError("Cannot include badge IDs without removing existing camera IDs.")
            # Check if we're changing the camera_ids and the existing instance has badge_ids
            if camera_ids is not None and instance.badge_ids:
                raise serializers.ValidationError("Cannot include camera IDs without removing existing badge IDs.")

        return validated_data

    def create(self, validated_data):
        """Automatically set the user field to the current user."""

        with transaction.atomic():
            return Schedule.objects.create(**validated_data)

    def to_representation(self, instance):
        """
        Modify the representation of the Schedule model to remove the user and day fields.
        """
        representation = super().to_representation(instance)
        representation.pop("user", None)
        representation.pop("day", None)
        return representation
