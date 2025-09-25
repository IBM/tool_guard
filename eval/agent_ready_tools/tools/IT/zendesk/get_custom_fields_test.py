from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_custom_fields import get_custom_fields


def test_get_custom_fields() -> None:
    """Verifies that the `get_custom_fields` tool can successfully retrieve the custom fields."""

    # Create the test data
    test_data: Dict[str, Any] = {
        "object_name": "organizations",
        "custom_fields": [
            {"id": "7088875537561", "title": "Emp ID", "key": "emp_id"},
            {"id": "7088875537562", "title": "Position", "key": "position"},
        ],
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_custom_fields.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.return_value = {"organizations_fields": test_data["custom_fields"]}

        # Retrieve custom fields using the get_custom_fields tool
        response = get_custom_fields(object_name=test_data["object_name"])

        # Ensure that get_custom_fields() executed and returned the proper values
        assert response
        assert len(response.custom_fields) == len(test_data["custom_fields"])
        for i, field in enumerate(response.custom_fields):
            assert field.field_id == test_data["custom_fields"][i]["id"]
            assert field.title == test_data["custom_fields"][i]["title"]
            assert field.key == test_data["custom_fields"][i]["key"]

        # Ensure the API call was made with the expected parameters
        mock_client.get_request.assert_called_once_with(entity="organizations_fields")
