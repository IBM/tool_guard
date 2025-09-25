from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.common_classes_supplier_management import (
    S4HanaBusinessPartner,
)
from agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.update_supplier import (
    sap_s4_hana_update_supplier,
)


def test_update_supplier() -> None:
    """Test that the sap_s4_hana_update_supplier tool updates supplier successfully."""

    # Define test data
    test_data = {
        "supplier_id": "1042",
        "business_partner_id": "1042",
        "supplier_name": "Test for aqheel 1",
        "supplier_name2": "aqheel 2",
        "supplier_name3": "aqheel 3",
        "supplier_name4": "aqheel 4",
        "search_term": "test1",
        "http_code": 204,
    }
    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.update_supplier.get_business_partner_id_of_supplier"
    ) as mock_business_partner, patch(
        "agent_ready_tools.tools.procurement.supplier_management.sap_s4_hana.update_supplier.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": test_data["http_code"]}
        mock_client.get_request.return_value = {
            "response": {"d": {"results": [{"BusinessPartner": test_data["business_partner_id"]}]}}
        }
        # Ensure the mock returns the correct business partner ID
        mock_business_partner.return_value = ToolResponse(
            success=True,
            message="Success",
            content=S4HanaBusinessPartner(
                business_partner_id=str(test_data["business_partner_id"])
            ),
        )

        # Call the function under test
        response = sap_s4_hana_update_supplier(
            supplier_id=test_data["supplier_id"],
            supplier_name=test_data["supplier_name"],
            supplier_name2=test_data["supplier_name2"],
            supplier_name3=test_data["supplier_name3"],
            supplier_name4=test_data["supplier_name4"],
            search_term=test_data["search_term"],
        )

        # Ensure that update_supplier() executed and returned proper values
        assert response
        assert response.content.http_code == test_data["http_code"]

        mock_client.patch_request.assert_called_once_with(
            entity=f"API_BUSINESS_PARTNER/A_BusinessPartner('{test_data["business_partner_id"]}')",
            payload={
                "OrganizationBPName1": test_data["supplier_name"],
                "OrganizationBPName2": test_data["supplier_name2"],
                "OrganizationBPName3": test_data["supplier_name3"],
                "OrganizationBPName4": test_data["supplier_name4"],
                "SearchTerm1": test_data["search_term"],
            },
        )
