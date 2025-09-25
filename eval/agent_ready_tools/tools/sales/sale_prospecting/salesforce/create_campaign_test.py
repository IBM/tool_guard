from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_campaign import (
    create_campaign,
)


def test_create_campaign() -> None:
    """Verifies that the `create_campaign` tool can successfully create a campaign in Salesforce."""

    # Define test input data
    test_data = {
        "campaign_name": "Sri",
        "campaign_type": "Email",
        "campaign_status": "Planned",
        "campaign_description": "hi hello",
        "campaign_start_date": "2025-04-22",
        "campaign_end_date": "2025-09-22",
        "campaign_id": "701gL000005G44pQAC",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.create_campaign.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Campaign.create.return_value = {
            "id": test_data["campaign_id"]
        }

        # Call the function under test
        response = create_campaign(
            campaign_name=test_data["campaign_name"],
            campaign_type=test_data["campaign_type"],
            campaign_status=test_data["campaign_status"],
            campaign_description=test_data["campaign_description"],
            campaign_start_date=test_data["campaign_start_date"],
            campaign_end_date=test_data["campaign_end_date"],
        )

        # Assertions
        assert response is not None
        assert response.campaign_id == test_data["campaign_id"]

        mock_client.salesforce_object.Campaign.create(
            {
                "Name": test_data["campaign_name"],
                "Type": test_data["campaign_type"],
                "Status": test_data["campaign_status"],
                "Description": test_data["campaign_description"],
                "StartDate": test_data["campaign_start_date"],
                "EndDate": test_data["campaign_end_date"],
            }
        )
