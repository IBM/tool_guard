from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.get_contract_owner_expiration_notice import (
    get_contract_owner_expiration_notice,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    OwnerExpirationNotice,
)


def test_get_contract_owner_expiration_notice() -> None:
    """Test that the `get_contract_owner_expiration_notice` function returns the expected
    response."""

    expected = [
        OwnerExpirationNotice(value="15", label="15 Days", active=True),
        OwnerExpirationNotice(value="30", label="30 Days", active=True),
        OwnerExpirationNotice(value="45", label="45 Days", active=True),
        OwnerExpirationNotice(value="60", label="60 Days", active=True),
        OwnerExpirationNotice(value="90", label="90 Days", active=True),
        OwnerExpirationNotice(value="120", label="120 Days", active=True),
    ]

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.get_contract_owner_expiration_notice.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Contract.describe.return_value = {
            "fields": [
                {
                    "aggregatable": True,
                    "name": "OwnerExpirationNotice",
                    "picklistValues": [
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "15 Days",
                            "validFor": None,
                            "value": "15",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "30 Days",
                            "validFor": None,
                            "value": "30",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "45 Days",
                            "validFor": None,
                            "value": "45",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "60 Days",
                            "validFor": None,
                            "value": "60",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "90 Days",
                            "validFor": None,
                            "value": "90",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "120 Days",
                            "validFor": None,
                            "value": "120",
                        },
                    ],
                }
            ]
        }
        response = get_contract_owner_expiration_notice()
        assert response == expected
