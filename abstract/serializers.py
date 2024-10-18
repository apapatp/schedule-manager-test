from rest_framework import serializers


class AbstractSerializer(serializers.ModelSerializer):
    """
    Abstract serializer class for all serializers.
    """

    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
