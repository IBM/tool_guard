from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_materials import (
    S4HANAMaterial,
    S4HANAMaterialResponse,
    sap_s4_hana_get_materials,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.date_conversion import sap_date_to_iso_8601


def test_sap_s4_hana_get_materials() -> None:
    """Tests that the materials can be retrieved by the `sap_s4_hana_get_materials` tool in SAP S4
    HANA."""

    # Define test data
    test_data: dict[str, str] = {
        "material_id": "34",
        "material_type": "FERT",
        "created_by": "MRAMISETTY",
        "creation_date": "2018-12-18",
        "material_group": "",
        "base_unit": "PC",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_materials.get_sap_s4_hana_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "Product": test_data["material_id"],
                            "ProductType": test_data["material_type"],
                            "CreatedByUser": test_data["created_by"],
                            "CreationDate": test_data["creation_date"],
                            "ProductGroup": test_data["material_group"],
                            "BaseUnit": test_data["base_unit"],
                        }
                    ]
                }
            }
        }

        # Call the function
        response = sap_s4_hana_get_materials(material_id=test_data["material_id"])

        # Verify that the material details match the expected data
        expected_response = ToolResponse(
            success=True,
            message="The data was successfully retrieved.",
            content=S4HANAMaterialResponse(
                materials=[
                    S4HANAMaterial(
                        material_id=test_data["material_id"],
                        material_type=test_data["material_type"],
                        created_by=test_data["created_by"],
                        creation_date=sap_date_to_iso_8601(test_data["creation_date"]),
                        material_group=test_data["material_group"],
                        base_unit=test_data["base_unit"],
                    )
                ]
            ),
        )
        assert response == expected_response
        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="API_PRODUCT_SRV/A_Product",
            filter_expr="Product eq '34'",
            params={"$top": 10, "$skip": 0},
        )
