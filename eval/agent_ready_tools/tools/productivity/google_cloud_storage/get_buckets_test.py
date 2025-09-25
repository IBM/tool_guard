from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.google_cloud_storage.constants import SERVICE, VERSION
from agent_ready_tools.tools.productivity.google_cloud_storage.get_buckets import (
    GoogleCloudStorageBucket,
    get_buckets,
)


def test_get_buckets() -> None:
    """Tests that the buckets can be retrieved by the `get_buckets` tool in Google Cloud Storage."""

    # Define test data
    test_data = {
        "project_id": "solid-transport-456516-u9",
        "bucket_id": "ibm-watson-orchestrate",
        "bucket_name": "ibm-watson-orchestrate",
        "location": "US",
        "creation_date": "2023-01-01T00:00:00Z",
        "bucket_name_prefix": "ibm-watson-orchestrate",
        "limit": 50,
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_cloud_storage.get_buckets.get_google_client"
    ) as mock_get_client:
        # Create a mock client and mock its get_request method
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "id": test_data["bucket_id"],
                    "name": test_data["bucket_name"],
                    "location": test_data["location"],
                    "timeCreated": test_data["creation_date"],
                }
            ],
        }

        # Call the get_buckets function
        response = get_buckets(
            project_id=test_data["project_id"],
            limit=test_data["limit"],
            bucket_name_prefix=test_data["bucket_name_prefix"],
        )

        # Ensure that the response is not None and contains data
        expected_bucket = GoogleCloudStorageBucket(
            bucket_id=str(test_data["bucket_id"]),
            bucket_name=str(test_data["bucket_name"]),
            location=str(test_data["location"]),
            creation_date=str(test_data["creation_date"]),
        )
        assert response
        assert response.buckets[0] == expected_bucket

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            service="storage",
            version="v1",
            entity="b",
            params={
                "project": test_data["project_id"],
                "maxResults": test_data["limit"],
                "prefix": test_data["bucket_name_prefix"],
            },
        )


def test_get_buckets_without_filter() -> None:
    """Tests that the buckets can be retrieved by the `get_buckets` tool in Google Cloud Storage."""

    # Define test data
    test_data = {
        "project_id": "solid-transport-456516-u9",
        "bucket_id": "ibm-watson-agent",
        "bucket_name": "ibm-watson-agent",
        "location": "UK",
        "creation_date": "2023-01-01T00:00:00Z",
        "next_page_token": "ibm-watson-agent",
        "limit": 1,
    }

    # Patch `get_google_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.google_cloud_storage.get_buckets.get_google_client"
    ) as mock_get_client:
        # Create a mock client and mock its get_request method
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "nextPageToken": test_data["next_page_token"],
            "items": [
                {
                    "id": test_data["bucket_id"],
                    "name": test_data["bucket_name"],
                    "location": test_data["location"],
                    "timeCreated": test_data["creation_date"],
                }
            ],
        }

        # Call the get_buckets function
        response = get_buckets(
            project_id=test_data["project_id"],
            limit=test_data["limit"],
            next_page_token=test_data["next_page_token"],
        )

        # Ensure that the response is not None and contains data
        expected_bucket = GoogleCloudStorageBucket(
            bucket_id=str(test_data["bucket_id"]),
            bucket_name=str(test_data["bucket_name"]),
            location=str(test_data["location"]),
            creation_date=str(test_data["creation_date"]),
        )
        assert response
        assert response.buckets[0] == expected_bucket
        assert response.next_page_token == test_data["next_page_token"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            service=SERVICE,
            version=VERSION,
            entity="b",
            params={
                "project": test_data["project_id"],
                "maxResults": test_data["limit"],
                "pageToken": test_data["next_page_token"],
            },
        )
