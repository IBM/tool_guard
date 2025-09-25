from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContractRenewalLengthUnit,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaUpdateContractResult:
    """Represents the result of updating a contract in Coupa."""

    id: int
    status: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_contract_details(
    contract_id: int,
    no_of_renewals: Optional[int] = None,
    renewal_length_unit: Optional[CoupaContractRenewalLengthUnit] = None,
    renewal_length_value: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    reason_insight_events: Optional[str] = None,
) -> ToolResponse[CoupaUpdateContractResult]:
    """
    Update a contract in Coupa.

    Args:
        contract_id: Contract ID.
        no_of_renewals: Number of renewals between 1..100
        renewal_length_unit: Unit of renewal
        renewal_length_value: Value of renewal length
        start_date: Contract start date
        end_date: Contract end date
        reason_insight_events: Reason insight events

    Returns:
        The result of updating a contract.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "no-of-renewals": no_of_renewals,
            "reason-insight-events": reason_insight_events,
            "renewal-length-unit": str(renewal_length_unit),
            "renewal-length-value": renewal_length_value,
            "start-date": start_date,
            "end-date": end_date,
        }.items()
        if value is not None and value != "None"
    }

    response = client.put_request(
        resource_name=f"contracts/{contract_id}",
        params={"fields": '["id","status"]'},
        payload=payload,
    )

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    return ToolResponse(
        success=True,
        message="The contract details ere successfully updated",
        content=CoupaUpdateContractResult(id=response["id"], status=response["status"]),
    )
