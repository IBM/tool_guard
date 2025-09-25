from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.create_custom_object_record import (
    create_custom_object_record,
)


def test_create_custom_object_record() -> None:
    """Tests that the create_custom_object_record tool returns expected response."""

    test_data: Dict[str, Any] = {
        "input_data": {"name": "test record", "external_id": "123", "description": "after changes"},
        "custom_object_key": "asset",
    }

    custom_fields = ["description", "creation_date", "expiration_date", "model", "quantity"]
    custom_objects = ["asset"]

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.create_custom_object_record.get_zendesk_client"
    ) as mock_zendesk_client, patch(
        "agent_ready_tools.tools.IT.zendesk.create_custom_object_record.get_custom_object_fields"
    ) as mock_custom_fields, patch(
        "agent_ready_tools.tools.IT.zendesk.create_custom_object_record.get_all_custom_objects"
    ) as mock_custom_objects:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "custom_object_record": {"name": test_data["input_data"]["name"]}
        }

        # Ensure the mock returns the correct custom object fields
        mock_custom_fields.return_value = custom_fields

        mock_custom_objects.return_value = custom_objects

        response = create_custom_object_record(
            input_data=test_data["input_data"],
            custom_object_key=test_data["custom_object_key"],
        )

    assert response

    mock_client.post_request.assert_called_once_with(
        entity=f"custom_objects/{test_data["custom_object_key"]}/records",
        payload={
            "custom_object_record": {
                "name": "test record",
                "external_id": "123",
                "custom_object_fields": {"description": "after changes"},
            }
        },
    )
