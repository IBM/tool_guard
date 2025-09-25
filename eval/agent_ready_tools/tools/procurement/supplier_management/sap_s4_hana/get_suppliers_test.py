from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_suppliers import (
    S4HANASupplier,
    S4HANASuppliersResponse,
    sap_s4_hana_get_suppliers,
)
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_get_suppliers() -> None:
    """Tests that the suppliers can be retrieved by the `get_suppliers` tool in SAP S4 HANA."""

    # Define test data
    test_data: dict[str, str] = {
        "supplier_id": "1042",
        "supplier_name": "RG Professional Services lTD Mumbai",
        "supplier_company_name": "Company RG Professional Services lTDMumbaiMH 400002/400001 MUMBAI",
        "creation_date": "/Date(1703548800000)/",
        "created_by": "GRASIK",
        "currency": "INR",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.get_suppliers.get_sap_s4_hana_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "Supplier": test_data["supplier_id"],
                            "SupplierName": test_data["supplier_name"],
                            "SupplierFullName": test_data["supplier_company_name"],
                            "CreationDate": test_data["creation_date"],
                            "CreatedByUser": test_data["created_by"],
                            "to_SupplierPurchasingOrg": {
                                "results": [
                                    {
                                        "PurchaseOrderCurrency": test_data["currency"],
                                    }
                                ]
                            },
                        }
                    ]
                }
            }
        }

        # Call the function
        response = sap_s4_hana_get_suppliers(supplier_name=test_data["supplier_name"]).content
        # Verify that the supplier details matches the expected data
        expected_response = S4HANASuppliersResponse(
            suppliers=[
                S4HANASupplier(
                    supplier_name=test_data["supplier_name"],
                    supplier_id=test_data["supplier_id"],
                    supplier_company_name=test_data["supplier_company_name"],
                    creation_date=sap_date_to_iso_8601(test_data["creation_date"]),
                    created_by=test_data["created_by"],
                    currency=test_data["currency"],
                )
            ]
        )

        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_BUSINESS_PARTNER/A_Supplier",
            filter_expr=f"SupplierName eq '{test_data['supplier_name']}'",
            expand_expr="to_SupplierPurchasingOrg",
            params={"$top": 20, "$skip": 0},
        )
