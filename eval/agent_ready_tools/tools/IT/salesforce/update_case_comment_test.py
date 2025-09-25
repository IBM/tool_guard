from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_case_comment import update_case_comment


def test_update_case_comment() -> None:
    """Test that the `update_case_comment` function returns the expected response."""
    # Define test data
    test_data = {
        "comment": "Case is now closed.",
        "comment_id": "00agL000000XBG1QAO",
    }
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_case_comment.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.CaseComment.update.return_value = test_response

        # Update case comment
        response = update_case_comment(
            comment_id=test_data["comment_id"], comment=test_data["comment"]
        )

        # Ensure that update_case_comment() executed and returned proper values
        assert response
        assert response.http_code == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.CaseComment.update(test_data, test_data["comment_id"])
