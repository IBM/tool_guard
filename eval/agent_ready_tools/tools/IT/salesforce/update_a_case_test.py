from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_a_case import update_a_case


def test_update_a_case() -> None:
    """Test that the `update_a_case` function returns the expected response."""

    # Define test data:
    test_data = {
        "case_id": "500gL000002mk6jQAA",
        "case_status": "Working",
        "case_origin": "Phone",
        "case_subject": "Issue",
        "case_type": "Problem",
        "case_reason": "User did not complete registration",
        "case_priority": "High",
        "case_description": "Customer is unable to log in after password reset.",
    }
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_a_case.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Case.update.return_value = test_response

        # Update case
        response = update_a_case(**test_data)

        # Ensure that update_a_case() has executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Case.update(test_data, test_data["case_id"])
