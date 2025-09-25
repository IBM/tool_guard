from http import HTTPStatus
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.ibm_cloud_object_storage.delete_bucket import (
    delete_bucket,
)


def test_delete_bucket() -> None:
    """Tests that a bucket can be deleted successfully by the `delete_bucket` tool."""

    # Define test data
    test_data = {
        "bucket_name": "test-bucket-1",
        "http_code": HTTPStatus.OK.value,
        "status": "success",
    }

    # Patch `get_ibm_cos_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.ibm_cloud_object_storage.delete_bucket.get_ibm_cos_client"
    ) as mock_get_ibm_cos_client:

        # Create mock bucket and resource
        mock_bucket = MagicMock()
        mock_cos_resource = MagicMock()
        mock_cos_resource.Bucket.return_value = mock_bucket

        # Create mock client and assign resource
        mock_client = MagicMock()
        mock_client.cos_resource = mock_cos_resource
        mock_get_ibm_cos_client.return_value = mock_client

        # Call the function
        response = delete_bucket(bucket_name=test_data["bucket_name"])

        # Assertions
        assert response
        assert response.http_code == test_data["http_code"]
        assert response.client_response["status"] == test_data["status"]
        assert response.error_message is None

        # Ensure the API call was made with expected parameters
        mock_cos_resource.Bucket.assert_called_once_with(test_data["bucket_name"])
