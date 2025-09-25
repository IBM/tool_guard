from typing import Any
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.ibm_cloud_object_storage.list_object_details import (
    ObjectMetadata,
    list_object_details,
)


def test_list_object_metadata() -> None:
    """Tests that the `list_object_details` tool can successfully retrieve object metadata."""

    # Define test data
    test_data: dict[str, Any] = {
        "object_name": "test-object-key-002",
        "last_modified": "2025-08-14T09:43:08.000Z",
        "etag": "764569e58f53ea8b6404f6fa7fc0247f",
        "size": 12,
        "content_type": "application/json",
    }

    # Patch `get_ibm_cos_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.ibm_cloud_object_storage.list_object_details.get_ibm_cos_client"
    ) as mock_ibm_cos_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_ibm_cos_client.return_value = mock_client
        mock_client.list_object_details.return_value = {
            "key": test_data["object_name"],
            "last_modified": test_data["last_modified"],
            "etag": test_data["etag"],
            "size": test_data["size"],
            "content_type": test_data["content_type"],
        }

        # Call the tool
        response = list_object_details(
            bucket_name="test-bucket-1", object_name="test-object-key-002"
        )

        expected_metadata = ObjectMetadata(
            object_name=test_data["object_name"],
            last_modified=test_data["last_modified"],
            etag=test_data["etag"],
            size=test_data["size"],
            content_type=test_data["content_type"],
            http_code=200,
        )

        print(response)
        print(expected_metadata)
        assert response == expected_metadata
        assert response.http_code == 200

        # Ensure the API call was made with expected parameters
        mock_client.list_object_details.assert_called_once_with(
            "test-bucket-1", "test-object-key-002"
        )
