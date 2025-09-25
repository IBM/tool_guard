from unittest.mock import MagicMock, patch

from requests import HTTPError
from requests.models import Response

from agent_ready_tools.tools.IT.zendesk.get_all_custom_objects import get_all_custom_objects


def test_get_all_custom_objects() -> None:
    """Verifies that the `get_all_custom_objects` tool can successfully retrieve the custom
    objects."""

    # Create the test data
    test_data = {
        "custom_objects": [
            {"key": "asset"},
            {"key": "equipment"},
        ],
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_all_custom_objects.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Retrieve custom objects using the get_all_custom_objects tool
        response = get_all_custom_objects()

        # Ensure that get_all_custom_objects() executed and returned the proper values
        assert response
        assert len(response.custom_objects) == len(test_data["custom_objects"])
        for i, obj in enumerate(response.custom_objects):
            assert obj.custom_object_key == test_data["custom_objects"][i]["key"]

        # Ensure the API call was made with the expected parameters
        mock_client.get_request.assert_called_once_with(entity="custom_objects")


def test_get_all_custom_objects_exception() -> None:
    """Tests that the `get_all_custom_objects` tool handles exceptions properly."""

    # Define test data for the error
    test_data = {"message": "Something went wrong.", "http_code": 500}

    # Create a mock response object
    mock_response = MagicMock(spec=Response)
    mock_response.status_code = test_data["http_code"]
    mock_response.json.return_value = {"error": {"message": test_data["message"]}}

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_all_custom_objects.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.side_effect = HTTPError(response=mock_response)

        # Call the function
        response = get_all_custom_objects()

        # Ensure that the function handled the exception and returned the correct error info
        assert response
        assert response.custom_objects == []
        assert response.http_code == test_data["http_code"]
        assert response.error_message == test_data["message"]

        # Ensure the API call was made
        mock_client.get_request.assert_called_once_with(entity="custom_objects")
