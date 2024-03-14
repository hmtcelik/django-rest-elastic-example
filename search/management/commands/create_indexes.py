from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections


class Command(BaseCommand):
    help = "Create an Elasticsearch index and populate it with sample data"

    def handle(self, *args, **options):
        # Sample data
        data = [
            {"hostname": "octoxlabs01", "ip_addresses": ["0.0.0.0"]},
            {"hostname": "octoxlabs02", "ip_addresses": ["127.0.0.1"]},
        ]

        # Connect to Elasticsearch
        client = connections.create_connection(hosts=["http://elasticsearch:9200"])
        client.indices.create(index="hosts", ignore=400)

        # Populate the index with sample data
        for item in data:
            client.index(index="hosts", body=item)

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created an Elasticsearch index and populated it with sample data"
            )
        )
