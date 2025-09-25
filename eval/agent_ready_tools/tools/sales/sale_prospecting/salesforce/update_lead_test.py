from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_lead import update_lead


def test_update_lead() -> None:
    """Tests that the `update_lead` function returns the expected response."""

    # Define test data:
    test_data = {
        "lead_id": "00QgL000001HqDIUA0",
        "first_name": "Naga",
        "last_name": "N",
        "email": "naga.n@gamil.com",
        "description": "Hi hello",
        "title": "Assistant Manager",
        "industry": "Government",
        "status": "Open - Not Contacted",
    }

    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.update_lead.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Lead.update.return_value = test_response

        # Update lead
        response = update_lead(**test_data)

        # Ensure that update_lead executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Lead.update(test_data, test_data["lead_id"])
