from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_custom_object_fields import get_custom_object_fields


def test_get_custom_object_fields() -> None:
    """Verifies that the `get_custom_object_fields` tool can successfully retrieve the custom object
    fields."""

    # Create the test data
    test_data: Dict[str, Any] = {
        "custom_object_key": "asset",
        "custom_object_fields": [
            {
                "field_id": "48532719554585",
                "field_type": "text",
                "title": "Description",
                "key": "description",
            },
            {
                "field_id": "48532730736921",
                "field_type": "date",
                "title": "Creation date",
                "key": "creation_date",
            },
        ],
    }

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_custom_object_fields.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "custom_object_fields": test_data["custom_object_fields"]
        }

        # Retrieve custom fields using the get_custom_object_fields tool
        response = get_custom_object_fields(custom_object_key=test_data["custom_object_key"])

        # Ensure that get_custom_object_fields() executed and returned the proper values
        assert response
        for i, field in enumerate(response.custom_object_fields):
            assert field.field_id == test_data["custom_object_fields"][i].get("id", "")
            assert field.field_type == test_data["custom_object_fields"][i].get("type", "")
            assert field.title == test_data["custom_object_fields"][i].get("title", "")
            assert field.key == test_data["custom_object_fields"][i].get("key", "")

        # Ensure the API call was made with the expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"custom_objects/{test_data['custom_object_key']}/fields"
        )
