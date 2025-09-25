from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_purchasing_info_records import (
    sap_s4_hana_get_purchasing_info_records,
)


def test_sap_s4_hana_get_purchasing_info_records() -> None:
    """Test that the purchasing info record retrieval works as expected with ToolResponse."""

    test_data = {
        "purchasing_info_record_id": "5300000597",
        "material_id": "FG251",
        "supplier_id": "1070",
        "supplier_phone_number": "9876543210",
        "plant": "1010",
        "currency": "USD",
        "net_amount": "45.61",
        "quantity_per_net_amount": "1",
        "standard_quantity": "100.000",
        "planned_delivery_time": "30",
        "minimum_quantity": "10.000",
        "supply_available_from": "/Date(1752192000000)/",
        "supply_available_to": "/Date(1815265000000)/",
        "tolerance_limit_over_delivery": "15.0",
        "tolerance_limit_under_delivery": "15.0",
        "unlimited_delivery_allowed": False,
        "condition_record_id": "0000007894",
        "condition_rate_value": "45.61",
        "condition_currency": "USD",
        "condition_quantity": "1",
    }

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.get_purchasing_info_records.get_sap_s4_hana_client"
    ) as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "response": {
                "d": {
                    "results": [
                        {
                            "PurchasingInfoRecord": test_data["purchasing_info_record_id"],
                            "Material": test_data["material_id"],
                            "Supplier": test_data["supplier_id"],
                            "SupplierPhoneNumber": test_data["supplier_phone_number"],
                            "AvailabilityStartDate": test_data["supply_available_from"],
                            "AvailabilityEndDate": test_data["supply_available_to"],
                            "to_PurgInfoRecdOrgPlantData": {
                                "results": [
                                    {
                                        "Plant": test_data["plant"],
                                        "Currency": test_data["currency"],
                                        "MinimumPurchaseOrderQuantity": test_data[
                                            "minimum_quantity"
                                        ],
                                        "StandardPurchaseOrderQuantity": test_data[
                                            "standard_quantity"
                                        ],
                                        "MaterialPlannedDeliveryDurn": test_data[
                                            "planned_delivery_time"
                                        ],
                                        "OverdelivTolrtdLmtRatioInPct": test_data[
                                            "tolerance_limit_over_delivery"
                                        ],
                                        "UnderdelivTolrtdLmtRatioInPct": test_data[
                                            "tolerance_limit_under_delivery"
                                        ],
                                        "UnlimitedOverdeliveryIsAllowed": test_data[
                                            "unlimited_delivery_allowed"
                                        ],
                                        "NetPriceAmount": test_data["net_amount"],
                                        "MaterialPriceUnitQty": test_data[
                                            "quantity_per_net_amount"
                                        ],
                                        "to_PurInfoRecdPrcgCndnValidity": {
                                            "results": [
                                                {
                                                    "ConditionRecord": test_data[
                                                        "condition_record_id"
                                                    ],
                                                    "to_PurInfoRecdPrcgCndn": {
                                                        "ConditionRateValue": test_data[
                                                            "condition_rate_value"
                                                        ],
                                                        "ConditionCurrency": test_data[
                                                            "condition_currency"
                                                        ],
                                                        "ConditionQuantity": test_data[
                                                            "condition_quantity"
                                                        ],
                                                    },
                                                }
                                            ]
                                        },
                                    }
                                ]
                            },
                        }
                    ]
                }
            }
        }

        response = sap_s4_hana_get_purchasing_info_records(material_id="FG251", supplier_id="1070")

        assert response.success is True
        assert response.message == "The data was successfully retrieved."
        assert response.content is not None  # MyPy-safe check
        assert (
            response.content.purchase_info[0].purchasing_info_record_id
            == test_data["purchasing_info_record_id"]
        )
        assert (
            response.content.purchase_info[0].pricing_conditions[0].condition_record_id
            == test_data["condition_record_id"]
        )

        mock_client.get_request.assert_called_once_with(
            entity="100/API_INFORECORD_PROCESS_SRV/A_PurchasingInfoRecord",
            filter_expr="Supplier eq '1070' and Material eq 'FG251'",
            expand_expr="to_PurgInfoRecdOrgPlantData/to_PurInfoRecdPrcgCndnValidity/to_PurInfoRecdPrcgCndn",
            params={"$top": 10, "$skip": 0},
        )
