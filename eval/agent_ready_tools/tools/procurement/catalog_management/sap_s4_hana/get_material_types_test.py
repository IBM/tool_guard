from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_material_types import (
    SAPS4HANAMaterialType,
    SAPS4HANAMaterialTypeResponse,
    sap_s4_hana_get_material_types,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def test_sap_s4_hana_get_material_types() -> None:
    """Tests that the material types can be retrieved by the `sap_s4_hana_get_material_types` tool
    in SAP S4 HANA."""

    # Define test data
    test_data = {
        "ProductType": "ABF",
        "ProductTypeName": "Waste",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_material_types.get_sap_s4_hana_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "value": [
                    {
                        "ProductType": test_data["ProductType"],
                        "ProductTypeName": test_data["ProductTypeName"],
                    }
                ]
            }
        }

        # Call the function
        response = sap_s4_hana_get_material_types(limit=50, skip=0, material_type_name="Waste")

        # Verify that the material type details match the expected data
        expected_response = ToolResponse(
            success=True,
            message="The data was successfully retrieved.",
            content=SAPS4HANAMaterialTypeResponse(
                material_types=[
                    SAPS4HANAMaterialType(
                        material_type_id=test_data["ProductType"],
                        material_type_name=test_data["ProductTypeName"],
                    )
                ]
            ),
        )

        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="producttype/0001/ProductType",
            filter_expr="ProductTypeName eq 'Waste'",
            params={"$top": 50, "$skip": 0},
        )
