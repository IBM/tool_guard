from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.common_classes_sap_s4_hana_catalog_management import (
    S4HANABaseUnit,
    S4HANAIndustrySector,
)
from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.create_material import (
    sap_s4_hana_create_material,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def test_sap_s4_hana_create_material_success() -> None:
    """Verify that the `sap_s4_hana_create_material` tool can successfully create a new material in
    SAP S4 HANA."""

    test_data = {
        "material_type": "FERT",
        "base_unit": "PIECE",
        "industry_sector": "MECHANICAL_ENGINEERING",
        "material_description": "create item test",
        "material_id": "321",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.create_material.get_sap_s4_hana_client"
    ) as mock_get_client:
        # create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"d": {"Product": test_data["material_id"]}}

        # Create a material
        response = sap_s4_hana_create_material(
            material_type=test_data["material_type"],
            base_unit=test_data["base_unit"],
            industry_sector=test_data["industry_sector"],
            material_description=test_data["material_description"],
        )

        # Ensure that sap_s4_hana_create_material() executed and returned proper values
        assert isinstance(response, ToolResponse)
        assert response.success is True
        assert response.message == "The record was successfully created."
        assert response.content is not None
        assert response.content.material_id == test_data["material_id"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="API_PRODUCT_SRV/A_Product",
            payload={
                "ProductType": test_data["material_type"].upper(),
                "BaseUnit": S4HANABaseUnit[test_data["base_unit"].upper()].value,
                "IndustrySector": S4HANAIndustrySector[test_data["industry_sector"].upper()].value,
                "to_Description": {
                    "results": [
                        {"Language": "EN", "ProductDescription": test_data["material_description"]}
                    ]
                },
            },
        )
