from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.get_contract_status import (
    get_contract_status,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import Status


def test_get_contract_status() -> None:
    """Test that the `get_contract_status` function returns the expected response."""

    expected = [
        Status(value="Draft", label="Draft", active=True),
        Status(value="InApproval", label="In Approval Process", active=True),
        Status(value="Activated", label="Activated", active=True),
        Status(value="Terminated", label="Terminated", active=True),
        Status(value="Expired", label="Expired", active=True),
        Status(value="Rejected", label="Rejected", active=True),
        Status(value="Negotiating", label="Negotiating", active=True),
        Status(value="AwaitingSignature", label="Awaiting Signature", active=True),
        Status(value="SignatureDeclined", label="Signature Declined", active=True),
        Status(value="Signed", label="Signed", active=True),
        Status(value="Cancelled", label="Canceled", active=True),
        Status(value="Expired2", label="Contract Expired", active=True),
        Status(value="Terminated2", label="Contract Terminated", active=True),
    ]

    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.get_contract_status.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Contract.describe.return_value = {
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
                            "label": "In Approval Process",
                            "validFor": None,
                            "value": "InApproval",
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
                            "label": "Terminated",
                            "validFor": None,
                            "value": "Terminated",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Expired",
                            "validFor": None,
                            "value": "Expired",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Rejected",
                            "validFor": None,
                            "value": "Rejected",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Negotiating",
                            "validFor": None,
                            "value": "Negotiating",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Awaiting Signature",
                            "validFor": None,
                            "value": "AwaitingSignature",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Signature Declined",
                            "validFor": None,
                            "value": "SignatureDeclined",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Signed",
                            "validFor": None,
                            "value": "Signed",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Canceled",
                            "validFor": None,
                            "value": "Cancelled",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Contract Expired",
                            "validFor": None,
                            "value": "Expired2",
                        },
                        {
                            "active": True,
                            "defaultValue": False,
                            "label": "Contract Terminated",
                            "validFor": None,
                            "value": "Terminated2",
                        },
                    ],
                }
            ]
        }
        response = get_contract_status()
        assert response == expected
