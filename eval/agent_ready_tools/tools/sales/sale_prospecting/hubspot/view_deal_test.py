from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import HubspotDeal
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.view_deal import hubspot_view_deal


def test_hubspot_view_deal() -> None:
    """Test Hubspot view deal tool."""

    test_id = "123"

    test_deal_response = {
        "dealname": "The New Deal",
        "dealtype": "newbusiness",
        "hs_object_id": "123",
        "description": "A brand new, beautiful deal",
        "dealstage": "initiated",
        "amount": 250.5,
        "pipeline": "New deals pipeline",
        "closedate": "2025-12-25",
        "lastmodifieddate": "2025-06-01",
        "createdate": "2025-01-01",
        "hubspot_owner_id": "bossman123",
    }

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.hubspot.view_deal.get_hubspot_client"
    ) as mock_hubspot_client:
        mock_client = MagicMock()
        mock_hubspot_client.return_value = mock_client

        mock_client.get_request.return_value = {"properties": test_deal_response}

        response: HubspotDeal = hubspot_view_deal(test_id)

        assert response
        assert response.deal_name == "The New Deal"
        assert response.deal_type == "newbusiness"

        mock_client.get_request.assert_called_once_with(
            service="crm",
            version="v3",
            entity=f"objects/deals/{test_id}",
        )
