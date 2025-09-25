from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.update_pricing_conditions import (
    S4HanaUpdatePricingConditionResponse,
    sap_s4_hana_update_pir_pricing_conditions,
)
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse


def test_sap_s4_hana_update_pir_pricing_conditions() -> None:
    """Test that pricing condition update returns expected ToolResponse on success."""

    # Define test input
    test_data = {
        "pricing_condition_record_id": "PC123456",
        "condition_rate_value": "150.00",
        "condition_to_base_quantity_numerator": "1",
        "condition_to_base_quantity_denominator": "1",
        "condition_lower_limit": "100.00",
        "condition_upper_limit": "200.00",
        "additional_value_days": "5",
    }

    expected_response = ToolResponse(
        success=True,
        message="Record updated successfully.",
        content=S4HanaUpdatePricingConditionResponse(http_code=204),
    )

    # Patch `get_sap_s4_hana_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.catalog_management.sap_s4_hana.update_pricing_conditions.get_sap_s4_hana_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.patch_request.return_value = {"http_code": 204}

        # Call the function
        response = sap_s4_hana_update_pir_pricing_conditions(**test_data)

        # Verify that the details match the expected data
        assert isinstance(response, ToolResponse)
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.patch_request.assert_called_once_with(
            entity="100/API_INFORECORD_PROCESS_SRV/A_PurInfoRecdPrcgCndn('PC123456')",
            payload={
                "d": {
                    "ConditionRateValue": "150.00",
                    "ConditionToBaseQtyNmrtr": "1",
                    "ConditionToBaseQtyDnmntr": "1",
                    "ConditionLowerLimit": "100.00",
                    "ConditionUpperLimit": "200.00",
                    "AdditionalValueDays": "5",
                }
            },
        )
