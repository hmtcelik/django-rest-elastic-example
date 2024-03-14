"""
This file contains the serializers for the search app.
"""

from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    """
    Serializer for the search API.
    """

    # The query to search for
    query = serializers.CharField(max_length=100)

    def validate_query(self, value):
        """
        Validate the query.
        """
        if "Hostname = " not in value:
            raise serializers.ValidationError(
                "Invalid query, must start with 'Hostname = '"
            )

        return value


class SearchResponseSerializer(serializers.Serializer):
    """
    Serializer for the search API response.
    """

    hostname = serializers.CharField(max_length=100)
    ip_addresses = serializers.ListField(child=serializers.IPAddressField())
