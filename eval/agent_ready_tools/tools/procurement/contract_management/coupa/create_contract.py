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
class CoupaCreateContractResult:
    """Represents the result of creating a contract in Coupa."""

    id: int
    status: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_create_contract(
    name: str,
    number: str,
    start_date: str,
    supplier_id: str,
    reason_insight_events: Optional[list[Any]] = None,
    no_of_renewals: int = 0,
    renewal_length_unit: CoupaContractRenewalLengthUnit = CoupaContractRenewalLengthUnit.NULL,
    renewal_length_value: int = 0,
    status: str = "draft",
) -> ToolResponse[CoupaCreateContractResult]:
    """
    Create a contract in Coupa.

    Args:
        name: Contract name.
        number: Contract's number.
        start_date: Start date of the contract.
        supplier_id: Supplier id (int).
        reason_insight_events: Reason insight events.
        no_of_renewals: Amount of renewals between 1..100.
        renewal_length_unit: The contract's renewal length unit.
        renewal_length_value: Value of renewal length.
        status: Status of the contract.

    Returns:
        The result of creating a contract.
    """

    # Handle the "None" case inside the function
    if reason_insight_events is None:
        reason_insight_events = []

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "name": name,
            "no-of-renewals": no_of_renewals,
            "number": number,
            "reason-insight-events": reason_insight_events,
            "renewal-length-unit": str(renewal_length_unit),
            "renewal-length-value": renewal_length_value,
            "status": status,
            "start-date": start_date,
            "supplier": {"id": supplier_id},
        }.items()
        if value is not None and value != "None"
    }

    response = client.post_request(
        resource_name="contracts", params={"fields": '["id","status"]'}, payload=payload
    )

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    return ToolResponse(
        success=True,
        message="The contract was successfully created",
        content=CoupaCreateContractResult(id=response["id"], status=response["status"]),
    )
