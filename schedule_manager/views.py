from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from schedule_manager.models import Schedule
from rest_framework.permissions import IsAuthenticated
from schedule_manager.serializers import ScheduleSerializer

class ScheduleViews(viewsets.ModelViewSet):
    """
    A Schedule viewset for CRUD operations.
    """

    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]  # No need for custom permission since isn't required
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        """Fetch all schedules."""
        return Schedule.objects.all()

    def perform_create(self, serializer):
        """Automatically set the user field to the current user."""
        serializer.save(user=self.request.user)

    # Custom action for retrieving schedules grouped by day
    @action(detail=False, methods=['get'])
    def grouped(self, request):
        schedule_data = {}

        for day, _ in Schedule.DaysChoices.choices:
            day_schedules = Schedule.objects.filter(day=day).order_by('start')  # Fixed ordering to 'start'
            serializer = ScheduleSerializer(day_schedules, many=True)
            unique_entries = []
            seen = set()

            for entry in serializer.data:
                # Remove empty badge_ids and camera_ids
                if not entry.get("badge_ids"):
                    entry.pop("badge_ids", None)
                if not entry.get("camera_ids"):
                    entry.pop("camera_ids", None)

                # Create a unique identifier based on the fields you want to consider
                unique_key = (entry["start"], entry["stop"], tuple(entry.get("badge_ids", [])), tuple(entry.get("camera_ids", [])))

                if unique_key not in seen:
                    seen.add(unique_key)
                    unique_entries.append(entry)

            schedule_data[day] = unique_entries

        return Response({"schedule": schedule_data})
