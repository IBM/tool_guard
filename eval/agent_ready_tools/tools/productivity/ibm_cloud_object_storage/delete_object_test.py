from http import HTTPStatus
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.ibm_cloud_object_storage.delete_object import (
    delete_object,
)


def test_delete_object() -> None:
    """Tests that an object can be deleted successfully by the `delete_object` tool."""

    # Define test data
    test_data = {
        "bucket_name": "test-bucket-1",
        "object_key": "test-object-key-002",
        "http_code": HTTPStatus.NO_CONTENT.value,
    }

    # Patch `get_ibm_cos_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.ibm_cloud_object_storage.delete_object.get_ibm_cos_client"
    ) as mock_get_ibm_cos_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_ibm_cos_client.return_value = mock_client
        # Simulate the response from the delete_object method
        mock_client.delete_object.return_value = {
            "status_code": test_data["http_code"],
        }

        # Call the function
        response = delete_object(
            bucket_name=test_data["bucket_name"], object_key=test_data["object_key"]
        )

        # Assertions
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_object.assert_called_once_with(
            bucket_name=test_data["bucket_name"], object_key=test_data["object_key"]
        )
