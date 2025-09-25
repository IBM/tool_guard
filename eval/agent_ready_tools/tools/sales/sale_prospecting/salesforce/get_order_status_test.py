from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.get_order_status import (
    get_order_status,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Status


def test_get_order_status() -> None:
    """Test that the `get_order_status` function returns the expected response."""

    expected = [
        Status(value="Draft", label="Draft", active=True),
        Status(value="Activated", label="Activated", active=True),
        Status(value="Canceled", label="Cancelled", active=True),
        Status(value="Expired", label="Expired", active=True),
    ]

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.get_order_status.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Order.describe.return_value = {
            "fields": [
                {
                    "aggregatable": True,
                    "name": "StatusCode",
                    "picklistValues": [
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Draft",
                            "validFor": None,
                            "value": "Draft",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Activated",
                            "validFor": None,
                            "value": "Activated",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Cancelled",
                            "validFor": None,
                            "value": "Canceled",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Expired",
                            "validFor": None,
                            "value": "Expired",
                        },
                    ],
                }
            ]
        }
        response = get_order_status()
        assert response == expected
