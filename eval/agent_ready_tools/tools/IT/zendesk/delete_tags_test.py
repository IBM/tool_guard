from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.zendesk.delete_tags import RemainingTagResponse, delete_tags


def test_delete_tags() -> None:
    """Tests that tags can be deleted successfully by the `delete_tags` tool."""
    # Define test data:
    test_data = {"module": "tickets", "module_record_id": "184943", "tag_names": "123,newtag"}

    # Patch `get_zendesk_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.zendesk.delete_tags.get_zendesk_client"
    ) as mock_zendesk_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_zendesk_client.return_value = mock_client
        mock_client.delete_request.return_value = {
            "tags": [
                "is_valid_tag",
                "newtestuser",
                "prnew",
                "randomtag",
                "test-ea",
                "test-ea1",
                "warranties",
            ],
            "status_code": 200,
        }

        # Call the function
        response = delete_tags(
            module=test_data["module"],
            module_record_id=test_data["module_record_id"],
            tag_names=test_data["tag_names"],
        )

        expected_response = RemainingTagResponse(
            tags=[
                "is_valid_tag",
                "newtestuser",
                "prnew",
                "randomtag",
                "test-ea",
                "test-ea1",
                "warranties",
            ],
            http_code=200,
        )

        # Ensure that the delete_tag() has been executed and returned the expected response
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(
            entity=f"{test_data['module']}/{test_data['module_record_id']}/tags",
            payload={"tags": test_data["tag_names"].split(",")},  # Split the tag names by comma
        )
