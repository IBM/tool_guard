from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.common_classes_sap_s4_hana_catalog_management import (
    S4HANABaseUnit,
    S4HANAIndustrySector,
)
from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.update_material import (
    sap_s4_hana_update_material,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def test_update_material() -> None:
    """Test that the `sap_s4_hana_update_material` tool updates material successfully."""

    # Define test data
    test_data = {
        "material_id": "41",
        "material_type": "CONT",
        "gross_weight": "4.000",
        "weight_unit": "KILOGRAM",
        "net_weight": "4.000",
        "purchase_order_quantity_unit": "KILOGRAM",
        "base_unit": "PIECE",
        "material_group": "01",
        "industry_sector": "MECHANICAL_ENGINEERING",
        "http_code": 204,
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.update_material.get_sap_s4_hana_client"
    ) as mock_sap_s4_hana_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_s4_hana_client.return_value = mock_client
        mock_client.patch_request.return_value = {"status_code": test_data["http_code"]}

        # Call the function under test
        response = sap_s4_hana_update_material(
            material_id=test_data["material_id"],
            material_type=test_data["material_type"],
            gross_weight=test_data["gross_weight"],
            weight_unit=test_data["weight_unit"],
            net_weight=test_data["net_weight"],
            purchase_order_quantity_unit=test_data["purchase_order_quantity_unit"],
            base_unit=test_data["base_unit"],
            material_group=test_data["material_group"],
            industry_sector=test_data["industry_sector"],
        )

        # Ensure that sap_s4_hana_update_material() executed and returned proper values
        assert isinstance(response, ToolResponse)
        assert response.success is True
        assert response.message == "The record was successfully updated."
        assert isinstance(response.content, dict)
        assert response.content["status_code"] == test_data["http_code"]

        mock_client.patch_request.assert_called_once_with(
            entity=f"100/API_PRODUCT_SRV/A_Product('{test_data['material_id']}')",
            payload={
                "d": {
                    "ProductType": test_data["material_type"],
                    "GrossWeight": test_data["gross_weight"],
                    "WeightUnit": S4HANABaseUnit[str(test_data["weight_unit"])].value,
                    "NetWeight": test_data["net_weight"],
                    "PurchaseOrderQuantityUnit": S4HANABaseUnit[
                        str(test_data["purchase_order_quantity_unit"])
                    ].value,
                    "BaseUnit": S4HANABaseUnit[str(test_data["base_unit"])].value,
                    "ProductGroup": test_data["material_group"],
                    "IndustrySector": S4HANAIndustrySector[str(test_data["industry_sector"])].value,
                }
            },
        )
