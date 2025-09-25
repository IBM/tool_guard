from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.common_classes_contract_management import (
    SAPS4HANAContractTypes,
)
from agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.create_contract import (
    sap_s4_hana_create_contract,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_create_contract() -> None:
    """Test that contract was created successfully by the sap_s4_hana_create_contract tool."""

    test_data = {
        "supplier_id": "10200001",
        "contract_type": "QUANTITY_CONTRACT",
        "company_code": "1010",
        "purchasing_organization": "1010",
        "purchasing_group": "001",
        "validity_end_date": "2025-12-12",
        "material_id": "2000000025",
        "plant": "SE01",
        "quantity": "15",
        "net_price": "150.00",
        "contract_id": "4600000132",
    }

    with patch(
        "agent_ready_tools.tools.procurement.contract_management.sap_s4_hana.create_contract.get_sap_s4_hana_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {
                "PurchaseContract": test_data["contract_id"],
                "Supplier": test_data["supplier_id"],
            }
        }

        response = sap_s4_hana_create_contract(
            supplier_id=test_data["supplier_id"],
            contract_type=test_data["contract_type"],
            company_code=test_data["company_code"],
            purchasing_organization=test_data["purchasing_organization"],
            purchasing_group=test_data["purchasing_group"],
            validity_end_date=test_data["validity_end_date"],
            material_id=test_data["material_id"],
            plant=test_data["plant"],
            quantity=test_data["quantity"],
            net_price=test_data["net_price"],
        )

        assert response.success is True
        assert response.message == "The record was successfully created."
        assert response.content.contract_id == test_data["contract_id"]
        assert response.content.supplier_id == test_data["supplier_id"]

        mock_client.post_request.assert_called_once_with(
            entity="100/API_PURCHASECONTRACT_PROCESS_SRV/A_PurchaseContract",
            payload={
                "PurchaseContractType": SAPS4HANAContractTypes[test_data["contract_type"]].value,
                "Supplier": test_data["supplier_id"],
                "CompanyCode": test_data["company_code"],
                "PurchasingOrganization": test_data["purchasing_organization"],
                "PurchasingGroup": test_data["purchasing_group"],
                "ValidityEndDate": iso_8601_to_sap_date(test_data["validity_end_date"]),
                "to_PurchaseContractItem": {
                    "results": [
                        {
                            "Material": test_data["material_id"],
                            "Plant": test_data["plant"],
                            "TargetQuantity": test_data["quantity"],
                            "ContractNetPriceAmount": test_data["net_price"],
                        }
                    ]
                },
            },
        )
