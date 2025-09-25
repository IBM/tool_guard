from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.get_custom_object_records import get_custom_object_records


# Mock Client test for getting all asset records
def test_get_custom_object_records() -> None:
    """Tests that the custom object record details are correctly returned."""

    # Define test data
    test_data = {
        "record_id": "01JZHYXQGH7Y5M89JF9TP0YB72",
        "record_name": "headphones  agent",
        "custom_object_key": "asset1",
        "creation_date": "2025-07-03T00:00:00+00:00",
        "description": "This is the headphones user requires",
        "expiry_date": "2026-07-03T00:00:00+00:00",
        "quantity": 1,
        "created_by_user_id": "382203429554",
        "created_at": "2025-07-07T08:09:31Z",
        "after_cursor": "eyJvIjoiLV9zY29yZSwtaWQiLCJ2IjoiYVFFQUFBQUFBQUFBY3hvQUFBQXdNVXBhU0ZsWVVVZElOMWsxVFRnNVNrWTVWRkF3V1VJM01nIn0",
        "before_cursor": None,
        "has_more_val": True,
        "error_message": "An exception occurred during the API call",
    }

    page_size = 1
    custom_objects = ["asset1"]

    with patch(
        "agent_ready_tools.tools.IT.zendesk.get_custom_object_records.get_zendesk_client"
    ) as mock_zendesk_client, patch(
        "agent_ready_tools.tools.IT.zendesk.get_custom_object_records.get_all_custom_objects"
    ) as mock_custom_objects:
        # Setup mock client and response
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "custom_object_records": [
                {
                    "id": test_data["record_id"],
                    "name": test_data["record_name"],
                    "custom_object_fields": {
                        "creation_date": test_data["creation_date"],
                        "description": test_data["description"],
                        "expiry_date": test_data["expiry_date"],
                        "quantity": test_data["quantity"],
                    },
                    "created_by_user_id": test_data["created_by_user_id"],
                    "created_at": test_data["created_at"],
                }
            ],
            "pagination": {
                "after_cursor": test_data["after_cursor"],
                "before_cursor": None,
                "has_more": test_data["has_more_val"],
            },
        }

        mock_custom_objects.return_value = custom_objects
        # Call the function
        response = get_custom_object_records(
            custom_object_key="asset1", query_field="headphones  agent", page_size=1
        )
        # Expected response
        expected_response = {
            "custom_object_details": [
                {
                    "record_id": test_data["record_id"],
                    "record_name": test_data["record_name"],
                    "created_by_user_id": test_data["created_by_user_id"],
                    "created_at": test_data["created_at"],
                    "creation_date": test_data["creation_date"],
                    "description": test_data["description"],
                    "expiry_date": test_data["expiry_date"],
                    "quantity": test_data["quantity"],
                    "after_cursor": None,
                    "before_cursor": None,
                    "has_more_val": None,
                }
            ],
        }
        assert response.dict(exclude_none=True) == expected_response

        # Assert correct API call
        mock_client.get_request.assert_called_once_with(
            entity=f"custom_objects/{test_data['custom_object_key']}/records/search",
            params={"query": test_data["record_name"], "page[size]": page_size},
        )
