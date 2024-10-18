from rest_framework import filters
from rest_framework.viewsets import GenericViewSet


class AbstractView(GenericViewSet):
    """
    Abstract view class for all views.
    """

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
