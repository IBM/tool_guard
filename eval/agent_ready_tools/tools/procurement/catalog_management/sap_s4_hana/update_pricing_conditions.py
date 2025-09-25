from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_s4_hana_client import get_sap_s4_hana_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import SAP_S4_HANA_CONNECTIONS


@dataclass
class S4HanaUpdatePricingConditionResponse:
    """Represents update pricing conditions response in SAP S/4HANA."""

    http_code: Optional[int] = None


@tool(expected_credentials=SAP_S4_HANA_CONNECTIONS)
def sap_s4_hana_update_pir_pricing_conditions(
    pricing_condition_record_id: str,
    condition_rate_value: str,
    condition_to_base_quantity_numerator: Optional[str] = None,
    condition_to_base_quantity_denominator: Optional[str] = None,
    condition_lower_limit: Optional[str] = None,
    condition_upper_limit: Optional[str] = None,
    additional_value_days: Optional[str] = None,
) -> ToolResponse[S4HanaUpdatePricingConditionResponse]:
    """
    Updates pricing conditions for a purchasing info record in SAP S/4 HANA.

    Args:
        pricing_condition_record_id: The ID of the pricing condition record that needs to be updated in SAP S/4 HANA, returned by `get_purchasing_info_records` tool.
        condition_rate_value: New rate value of pricing condition record, this value need to be between condition lower and upper limit.
        condition_to_base_quantity_numerator: New numerator for base quantity conversion of pricing condition record.
        condition_to_base_quantity_denominator: New denominator for base quantity conversion of pricing condition record.
        condition_lower_limit: New lower limit for rate value of pricing condition record.
        condition_upper_limit: New upper limit for rate value of pricing condition record.
        additional_value_days: New additional value days for pricing condition record.

    Returns:
        The http code of the update response.
    """
    try:
        client = get_sap_s4_hana_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    client = get_sap_s4_hana_client()

    payload: Dict[str, Any] = {
        "ConditionRateValue": condition_rate_value,
        "ConditionToBaseQtyNmrtr": condition_to_base_quantity_numerator,
        "ConditionToBaseQtyDnmntr": condition_to_base_quantity_denominator,
        "ConditionLowerLimit": condition_lower_limit,
        "ConditionUpperLimit": condition_upper_limit,
        "AdditionalValueDays": additional_value_days,
    }

    payload = {key: value for key, value in payload.items() if value is not None}

    response = client.patch_request(
        entity=f"100/API_INFORECORD_PROCESS_SRV/A_PurInfoRecdPrcgCndn('{pricing_condition_record_id}')",
        payload={"d": payload},
    )

    if "error" in response:
        content = response.get("error", {}).get("message", {})
        return ToolResponse(success=False, message="Request unsuccessful1", content=content)

    if "fault" in response:
        content = response.get("fault", {}).get("faultstring", "")
        return ToolResponse(success=False, message="Request unsuccessful2", content=content)

    response_status_code = response.get("http_code")

    return ToolResponse(
        success=True,
        message="Record updated successfully.",
        content=S4HanaUpdatePricingConditionResponse(http_code=response_status_code),
    )
