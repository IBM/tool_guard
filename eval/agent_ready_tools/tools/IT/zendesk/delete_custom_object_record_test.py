from unittest.mock import MagicMock, patch

from requests import HTTPError
from requests.models import Response

from agent_ready_tools.tools.IT.zendesk.delete_custom_object_record import (
    delete_custom_object_record,
)


def test_delete_custom_object_record() -> None:
    """Tests that a custom object can be successfully deleted by the `delete_custom_object_record`
    tool."""

    # Define test data:
    test_data = {
        "custom_object_key": "asset1",
        "custom_object_record_id": "01JZHJ83R38MPNMYPA1Z6SWWHW",
        "http_code": 204,
    }
    custom_objects = ["asset1"]

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_custom_object_record.get_zendesk_client"
    ) as mock_zendesk_client, patch(
        "agent_ready_tools.tools.IT.zendesk.delete_custom_object_record.get_all_custom_objects"
    ) as mock_custom_objects:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client

        mock_client.delete_request.return_value = {"status_code": test_data["http_code"]}
        mock_custom_objects.return_value = custom_objects

        # Delete custom object
        response = delete_custom_object_record(
            test_data["custom_object_key"], test_data["custom_object_record_id"]
        )

        # Ensure that delete_custom_object_record() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"custom_objects/{test_data['custom_object_key']}/records/{test_data['custom_object_record_id']}"
        )


def test_delete_custom_object_record_invalid_key() -> None:
    """Tests that an invalid custom object key is handled properly by the
    `delete_custom_object_record` tool."""

    # Define test data:
    test_data = {
        "custom_object_key": "invalid_key",
        "custom_object_record_id": "01JZHJ83R38MPNMYPA1Z6SWWHW",
    }
    custom_objects = ["asset1"]

    # Patch `get_all_custom_objects` to return a mock list of custom objects
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_custom_object_record.get_all_custom_objects"
    ) as mock_custom_objects:
        mock_custom_objects.return_value = custom_objects
        # Delete custom object
        response = delete_custom_object_record(
            test_data["custom_object_key"], test_data["custom_object_record_id"]
        )

        # Ensure that delete_custom_object_record() executed and returned proper values
        assert (
            response.error_message
            == f"An exception occurred during the API call: custom object {test_data['custom_object_key']} is not valid"
        )


def test_delete_custom_object_record_exception() -> None:
    """Tests that custom object deletion handles exceptions properly by the
    `delete_custom_object_record` tool."""

    # Define test data:
    test_data = {
        "custom_object_key": "asset1",
        "custom_object_record_id": "01JZHJ83R38MPNMYPA1Z6SWWHW",
        "error": "RecordNotFound",
        "description": "Not found",
        "http_code": 404,
    }

    # Create a mock response object
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = test_data["http_code"]
    mock_response.json.return_value = {
        "error": test_data["error"],
        "description": test_data["description"],
    }

    custom_objects = ["asset1"]

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_custom_object_record.get_zendesk_client"
    ) as mock_zendesk_client, patch(
        "agent_ready_tools.tools.IT.zendesk.delete_custom_object_record.get_all_custom_objects"
    ) as mock_custom_objects:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.delete_request.side_effect = HTTPError(response=mock_response)
        mock_custom_objects.return_value = custom_objects

        # Delete custom object
        response = delete_custom_object_record(
            test_data["custom_object_key"], test_data["custom_object_record_id"]
        )

        # Ensure that delete_custom_object_record() executed and returned proper values
        assert response
        assert response.error_message == test_data["error"]
        assert response.error_description == test_data["description"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"custom_objects/{test_data['custom_object_key']}/records/{test_data['custom_object_record_id']}"
        )
