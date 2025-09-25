from typing import List
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.hubspot.dataclasses import HubspotContact
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.search_contacts import (
    hubspot_search_contacts,
)
from agent_ready_tools.tools.sales.sale_prospecting.hubspot.utils import (
    hubspot_create_search_filter,
)


def test_hubspot_search_contacts() -> None:
    """Test Hubspot search contacts tool."""

    test_contact_response = [
        {
            "properties": {
                "createdate": "2025-08-05T17:56:41.453Z",
                "email": "lorelai@thedragonfly.com",
                "firstname": "Lorelai",
                "hs_object_id": "197093183168",
                "lastmodifieddate": "2025-08-05T20:55:06.398Z",
                "lastname": "Gilmore",
            },
        },
        {
            "properties": {
                "createdate": "2025-08-05T17:56:41.451Z",
                "email": "luke@lukesdiner.com",
                "firstname": "Luke",
                "hs_object_id": "196851302084",
                "lastmodifieddate": "2025-08-05T20:55:13.912Z",
                "lastname": "Danes",
            },
        },
    ]

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.hubspot.search_contacts.get_hubspot_client"
    ) as mock_hubspot_client:
        mock_client = MagicMock()
        mock_hubspot_client.return_value = mock_client

        mock_client.post_request.return_value = {"results": test_contact_response}

        response: List[HubspotContact] = hubspot_search_contacts(first_name="L")

        assert response
        assert response[0].first_name == "Lorelai"
        assert response[1].last_name == "Danes"

        filt = hubspot_create_search_filter({"firstname": "L"})

        mock_client.post_request.assert_called_once_with(
            service="crm",
            version="v3",
            entity="objects/contacts/search",
            payload=filt,
        )
