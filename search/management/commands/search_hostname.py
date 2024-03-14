from django.core.management.base import BaseCommand
from elasticsearch_dsl.connections import connections
from django.urls import reverse
import requests


class Command(BaseCommand):
    help = "Search for a hostname with the api"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            type=str,
            help="The username to authenticate with",
        )
        parser.add_argument(
            "password",
            type=str,
            help="The password to authenticate with",
        )
        parser.add_argument("hostname", type=str, help="The hostname to search for")

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        hostname = options["hostname"]

        base_url = "http://localhost:8000/"  # NOTE: should be changed to the actual url

        # Authenticate with the API
        auth_url = base_url + reverse("token_obtain_pair")
        auth_response = requests.post(
            auth_url, json={"username": username, "password": password}
        )
        if "access" not in auth_response.json():
            return self.stdout.write(
                self.style.ERROR(
                    "Failed the Authentication, No active account found with the given credentials"
                )
            )
        token = auth_response.json()["access"]

        # Search for the hostname
        url = base_url + reverse("search")
        headers = {"Authorization": f"Octoxlabs {token}"}
        search_response = requests.post(
            url, json={"query": f"Hostname = {hostname}"}, headers=headers
        )

        if search_response.status_code != 200:
            return self.stdout.write(
                self.style.ERROR(
                    "Failed to search for the hostname, maybe you should create the index first, check the readme for more information."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(f"Search results: {search_response.json()}")
        )
