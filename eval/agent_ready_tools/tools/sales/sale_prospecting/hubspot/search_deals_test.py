from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import HubspotDeal
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.search_deals import hubspot_search_deals
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.utils import (
    hubspot_create_search_filter,
)


def test_hubspot_search_deals() -> None:
    """Test Hubspot search deals tool."""

    test_deal_response = [
        {
            "id": "123",
            "properties": {
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
            },
        },
        {
            "id": "456",
            "properties": {
                "dealname": "The Old Deal",
                "dealtype": "existingbusiness",
                "hs_object_id": "456",
                "description": "An old, beautiful deal",
                "dealstage": "finalizing",
                "amount": 1000.0,
                "pipeline": "Old deals pipeline",
                "closedate": "2025-12-25",
                "lastmodifieddate": "2025-06-01",
                "createdate": "2015-01-01",
                "hubspot_owner_id": "bossman123",
            },
        },
    ]

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.hubspot.search_deals.get_hubspot_client"
    ) as mock_hubspot_client:
        mock_client = MagicMock()
        mock_hubspot_client.return_value = mock_client

        mock_client.post_request.return_value = {"results": test_deal_response}

        response: List[HubspotDeal] = hubspot_search_deals("Deal")

        assert response
        assert response[0].deal_name == "The New Deal"
        assert response[1].deal_type == "existingbusiness"

        filt = hubspot_create_search_filter({"dealname": "Deal"})

        mock_client.post_request.assert_called_once_with(
            service="crm",
            version="v3",
            entity="objects/deals/search",
            payload=filt,
        )
