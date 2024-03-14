"""
This module contains the API for the search app.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

from .serializers import SearchSerializer, SearchResponseSerializer


class SearchAPIView(APIView):
    """
    API view for searching in elasticsearch.
    """

    def post(self, request):
        """
        Search in elasticsearch.
        """
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Extract the hostname from the query (already validated in the serializer)
        hostname = serializer.validated_data["query"].split(" = ")[1]

        client = connections.create_connection(hosts=["http://elasticsearch:9200"])
        search = Search(using=client, index="hosts").query(
            "wildcard", hostname=hostname
        )

        results = search.execute()
        response_data = SearchResponseSerializer(results, many=True).data

        return Response(response_data)
