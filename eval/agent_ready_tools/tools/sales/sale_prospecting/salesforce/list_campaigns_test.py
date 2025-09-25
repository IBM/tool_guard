from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_campaigns import list_campaigns
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Campaign


def test_list_campaigns() -> None:
    """Tests that the `list_campaigns` function returns the expected response."""

    # Define test data:
    test_data = {
        "campaign_id": "701gL000003fj1xQAA",
        "campaign_name": "GC Product Webinar - Jan 7, 2002",
        "campaign_status": "Completed",
        "campaign_type": "Webinar",
        "campaign_created_date": "2025-04-11",
        "campaign_start_date": "2024-09-20",
        "campaign_end_date": "2024-09-20",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_campaigns.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": "701gL000003fj1xQAA",
                "Name": "GC Product Webinar - Jan 7, 2002",
                "StartDate": "2024-09-20",
                "EndDate": "2024-09-20",
                "Type": "Webinar",
                "Status": "Completed",
                "CreatedDate": "2025-04-11T03:36:12.000+0000",
            }
        ]

        response = list_campaigns(
            "Name = 'GC Product Webinar - Jan 7, 2002' AND Type = 'Webinar' AND Status = 'Completed'"
        )

        expected = Campaign(**test_data)

        # Ensure that list_campaigns() executed and returned proper values
        assert response
        assert len(response)
        assert response[0] == expected

        # Ensure the correct query was made with limit and offset
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, Name, Status, Type, CreatedDate, StartDate, EndDate FROM Campaign WHERE Name = 'GC Product Webinar - Jan 7, 2002' AND Type = 'Webinar' AND Status = 'Completed'"
        )
