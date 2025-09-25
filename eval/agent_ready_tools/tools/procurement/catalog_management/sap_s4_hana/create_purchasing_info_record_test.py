from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.create_purchasing_info_record import (
    sap_s4_hana_create_purchasing_info_record,
)
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date


def test_create_purchasing_info_record_success() -> None:
    """Test successful creation of a purchasing info record."""

    test_data = {
        "supplier_id": "1070",
        "material_id": "TU_TW",
        "purchasing_organization": "WXO1",
        "planned_delivery_time": "30",
        "purchasing_group": "001",
        "standard_quantity": "75",
        "net_amount": "11.24",
        "quantity_per_net_amount": "1",
        "supply_available_from": "2025-07-11",
        "supply_available_to": "2027-07-11",
        "minimum_quantity": "10",
        "tolerance_limit_under_delivery": "10",
        "tolerance_limit_over_delivery": "10",
        "unlimited_delivery_allowed": True,
        "purchasing_info_record": "5300000597",
    }

    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.create_purchasing_info_record.get_sap_s4_hana_client"
    ) as mock_s4hana_client:
        mock_client = MagicMock()
        mock_s4hana_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "d": {"PurchasingInfoRecord": test_data["purchasing_info_record"]}
        }

        response = sap_s4_hana_create_purchasing_info_record(
            supplier_id=test_data["supplier_id"],
            material_id=test_data["material_id"],
            purchasing_organization=test_data["purchasing_organization"],
            planned_delivery_time=test_data["planned_delivery_time"],
            purchasing_group=str(test_data["purchasing_group"]),
            standard_quantity=test_data["standard_quantity"],
            net_amount=test_data["net_amount"],
            quantity_per_net_amount=test_data["quantity_per_net_amount"],
            supply_available_from=test_data["supply_available_from"],
            supply_available_to=test_data["supply_available_to"],
            minimum_quantity=test_data["minimum_quantity"],
            tolerance_limit_under_delivery=test_data["tolerance_limit_under_delivery"],
            tolerance_limit_over_delivery=test_data["tolerance_limit_over_delivery"],
            unlimited_delivery_allowed=test_data["unlimited_delivery_allowed"],
        ).content

        assert response
        assert response.purchasing_info_record_id == test_data["purchasing_info_record"]

        expected_payload = {
            "Supplier": test_data["supplier_id"],
            "Material": test_data["material_id"],
            "AvailabilityStartDate": iso_8601_to_sap_date(str(test_data["supply_available_from"])),
            "AvailabilityEndDate": iso_8601_to_sap_date(str(test_data["supply_available_to"])),
            "to_PurgInfoRecdOrgPlantData": {
                "results": [
                    {
                        "PurchasingOrganization": test_data["purchasing_organization"],
                        "MaterialPlannedDeliveryDurn": test_data["planned_delivery_time"],
                        "PurchasingGroup": str(test_data["purchasing_group"]),
                        "StandardPurchaseOrderQuantity": test_data["standard_quantity"],
                        "MinimumPurchaseOrderQuantity": test_data["minimum_quantity"],
                        "OverdelivTolrtdLmtRatioInPct": test_data["tolerance_limit_under_delivery"],
                        "UnderdelivTolrtdLmtRatioInPct": test_data["tolerance_limit_over_delivery"],
                        "UnlimitedOverdeliveryIsAllowed": test_data["unlimited_delivery_allowed"],
                        "NetPriceAmount": test_data["net_amount"],
                        "MaterialPriceUnitQty": test_data["quantity_per_net_amount"],
                    }
                ]
            },
        }

        mock_client.post_request.assert_called_once_with(
            entity="100/API_INFORECORD_PROCESS_SRV/A_PurchasingInfoRecord",
            payload=expected_payload,
        )
