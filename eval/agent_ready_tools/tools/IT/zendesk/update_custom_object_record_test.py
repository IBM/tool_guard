from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.update_custom_object_record import (
    update_custom_object_record,
)


def test_update_custom_object_record() -> None:
    """Tests that the zendesk_update_custom_object_record tool returns expected response."""

    test_data = {
        "input_data": {"name": "test record", "description": "after changes"},
        "custom_object_key": "asset",
        "custom_object_record_id": "99U988878FRF",
    }
    custom_fields = ["description", "creation_date", "expiration_date", "model", "quantity"]

    custom_objects = ["asset"]

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.update_custom_object_record.get_zendesk_client"
    ) as mock_zendesk_client, patch(
        "agent_ready_tools.tools.IT.zendesk.update_custom_object_record.get_custom_object_fields"
    ) as mock_custom_fields, patch(
        "agent_ready_tools.tools.IT.zendesk.update_custom_object_record.get_all_custom_objects"
    ) as mock_custom_objects:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.patch_request.return_value = {
            "custom_object_record": {"id": test_data["custom_object_record_id"]}
        }

        # Ensure the mock returns the correct custom object fields
        mock_custom_fields.return_value = custom_fields

        mock_custom_objects.return_value = custom_objects

        response = update_custom_object_record(
            input_data=test_data["input_data"],
            custom_object_key=test_data["custom_object_key"],
            custom_object_record_id=test_data["custom_object_record_id"],
        )

    assert response
    assert response.custom_object_record_id == test_data["custom_object_record_id"]

    mock_client.patch_request.assert_called_once_with(
        entity=f"custom_objects/{test_data["custom_object_key"]}/records/{test_data["custom_object_record_id"]}",
        payload={
            "custom_object_record": {
                "name": "test record",
                "custom_object_fields": {"description": "after changes"},
            }
        },
    )
