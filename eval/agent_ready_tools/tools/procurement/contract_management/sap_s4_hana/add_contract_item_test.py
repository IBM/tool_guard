from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.add_contract_item import (
    sap_s4_hana_add_contract_item,
)


def test_add_contract_item() -> None:
    """Test that item was added to a contract successfully by the sap_s4_hana_add_contract_item
    tool."""

    test_data = {
        "material_id": "2000000025",
        "plant": "SE01",
        "quantity": "15",
        "net_price": "150.00",
        "contract_id": "4600000132",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.add_contract_item.get_sap_s4_hana_client"
    ) as mock_get_client:

        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        mock_client.post_request.return_value = {
            "d": {
                "PurchaseContract": test_data["contract_id"],
                "Material": test_data["material_id"],
                "Plant": test_data["plant"],
                "TargetQuantity": test_data["quantity"],
                "ContractNetPriceAmount": test_data["net_price"],
            }
        }

        response = sap_s4_hana_add_contract_item(
            contract_id=test_data["contract_id"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            quantity=test_data["quantity"],
            net_price=test_data["net_price"],
        )

        assert response.success is True
        assert response.message == "The record was successfully created."
        assert response.content.contract_id == test_data["contract_id"]

        mock_client.post_request.assert_called_once_with(
            entity=f"100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract('{test_data['contract_id']}')/to_PurchaseContractItem",
            payload={
                "PurchaseContract": test_data["contract_id"],
                "Material": test_data["material_id"],
                "Plant": test_data["plant"],
                "TargetQuantity": test_data["quantity"],
                "ContractNetPriceAmount": test_data["net_price"],
            },
        )
