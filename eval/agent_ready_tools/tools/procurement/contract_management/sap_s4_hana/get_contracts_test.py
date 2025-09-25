from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.get_contracts import (
    S4HANAContractsResponse,
    sap_s4_hana_get_contracts,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_sap_s4_hana_get_contracts() -> None:
    """Test that the `sap_s4_hana_get_contracts` function returns the expected response."""
    test_data = {
        "contract_id": "4600000105",
        "company_code": "1010",
        "creation_date": "/Date(1747872000000)/",
        "created_by_user": "MANEPALLIM",
        "supplier": "10200001",
        "purchasing_processing_status_name": "Active",
        "created_after": "2025-05-22",
        "created_before": "2025-05-23",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.get_contracts.get_sap_s4_hana_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "PurchaseContract": test_data["contract_id"],
                            "CompanyCode": test_data["company_code"],
                            "CreationDate": test_data["creation_date"],
                            "CreatedByUser": test_data["created_by_user"],
                            "Supplier": test_data["supplier"],
                            "PurchasingProcessingStatusName": test_data[
                                "purchasing_processing_status_name"
                            ],
                        },
                    ]
                }
            }
        }

        response = sap_s4_hana_get_contracts(
            created_after=test_data["created_after"], created_before=test_data["created_before"]
        )

        assert isinstance(response, ToolResponse)
        assert response.success is True
        assert isinstance(response.content, S4HANAContractsResponse)

        contract = response.content.contracts[0]
        assert contract.contract_id == test_data["contract_id"]
        assert contract.company_code == test_data["company_code"]
        assert contract.creation_date == sap_date_to_iso_8601(test_data["creation_date"])
        assert contract.created_by_user == test_data["created_by_user"]
        assert contract.supplier == test_data["supplier"]
        assert (
            contract.purchasing_processing_status_name
            == test_data["purchasing_processing_status_name"]
        )

        mock_client.get_request.assert_called_once_with(
            entity="100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract",
            filter_expr=f"CreationDate ge datetime'{test_data['created_after']}T00:00:00' and CreationDate le datetime'{test_data['created_before']}T00:00:00'",
            params={"$top": 20, "$skip": 0},
        )
