from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_all_purchase_requisitions import (
    oracle_fusion_get_all_purchase_requisitions,
)


def test_oracle_fusion_get_all_purchase_requisitions() -> None:
    """Test the getting of all purchase requisitions from Oracle Fusion using a mock client."""
    requisition_list = {
        "items": [
            {
                "RequisitionHeaderId": 300000025241141,
                "Requisition": "204221",
                "Preparer": "sri",
                "PreparerEmail": "sri@gmail.com",
                "Description": "Test001DemoJDE",
                "DocumentStatus": "Approved",
                "CreationDate": "2025-07-24T11:51:20.274+00:00",
                "FundsStatus": "Not applicable",
                "Justification": "Testing APi",
            }
        ]
    }

    with patch(
        "agent_ready_tools.tools.procurement.purchase_support.oracle_fusion.get_all_purchase_requisitions.get_oracle_fusion_client"
    ) as mock_oracle_fusion_client:
        mock_client = MagicMock()
        mock_oracle_fusion_client.return_value = mock_client
        mock_client.get_request.return_value = requisition_list

        response = oracle_fusion_get_all_purchase_requisitions()

        assert response

        mock_client.get_request.assert_called_once_with(
            resource_name="purchaseRequisitions",
            params={"limit": 10, "offset": 0},
        )
