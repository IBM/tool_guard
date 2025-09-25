from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_campaign import (
    delete_campaign,
)


def test_delete_campaign() -> None:
    """Tests that the `delete_a_campaign` function returns the expected response."""

    # Define test data:
    test_data = {
        "campaign_id": "701gL000004duCvQAI",
        "http_code": 204,
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.delete_campaign.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Campaign.delete.return_value = test_data["http_code"]
        # mock_client.delete_a_campaign.return_value = test_data["http_code"]

        # Delete a campaign
        response = delete_campaign(test_data["campaign_id"])

        # Ensure that delete_a_campaign() executed and returned proper values
        assert response

        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Campaign.delete(record_id=test_data["campaign_id"])
