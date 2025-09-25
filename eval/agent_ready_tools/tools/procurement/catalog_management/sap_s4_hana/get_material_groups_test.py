from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_material_groups import (
    S4HANAMaterialGroup,
    S4HANAMaterialGroupResponse,
    sap_s4_hana_get_material_groups,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def test_sap_s4_hana_get_material_groups() -> None:
    """Tests that the material groups can be retrieved by the `sap_s4_hana_get_material_groups` tool
    in SAP S4 HANA."""

    # Define test data
    test_data = {
        "ProductGroup": "01",
        "ProductGroupName": "Material group 1",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_material_groups.get_sap_s4_hana_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "value": [
                    {
                        "ProductGroup": test_data["ProductGroup"],
                        "ProductGroupName": test_data["ProductGroupName"],
                    }
                ]
            }
        }

        # Call the function
        response = sap_s4_hana_get_material_groups(
            limit=20, skip=0, material_group_name="Material group 1"
        )

        # Verify that the material group details match the expected data
        expected_response = ToolResponse(
            success=True,
            message="The data was successfully retrieved.",
            content=S4HANAMaterialGroupResponse(
                material_group=[
                    S4HANAMaterialGroup(
                        material_group=test_data["ProductGroup"],
                        material_group_name=test_data["ProductGroupName"],
                    )
                ]
            ),
        )

        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="productgroup/0001/ProductGroup",
            filter_expr="ProductGroupName eq 'Material group 1'",
            params={"$top": 20, "$skip": 0},
        )
