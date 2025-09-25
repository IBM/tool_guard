from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaUpdateContractPaymentResult:
    """Represents the result of updating a contract in Coupa."""

    id: int
    status: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_contract_payment_details(
    contract_id: str,
    payment_term: Optional[str] = None,
    currency: Optional[str] = None,
    savings_pct: Optional[float] = None,
    stop_spend_based_on_max_value: Optional[str] = None,
    shipping_term: Optional[str] = None,
    min_commit: Optional[float] = None,
    max_commit: Optional[float] = None,
) -> ToolResponse[CoupaUpdateContractPaymentResult]:
    """
    Update a contract's payment details in Coupa.

    Args:
        contract_id: Contract id
        payment_term: Payment term code
        currency: Currency code
        savings_pct: Savings achieved through contracts pricing
        stop_spend_based_on_max_value: Stop spend based on max value
        shipping_term: Shipping term code on contract
        min_commit: Minimum commit value
        max_commit: Maximum commit value

    Returns:
        The result of updating a contract's payment details
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload: Dict[str, Any] = {
        key: value
        for key, value in {
            "payment-term": {"code": payment_term} if payment_term else None,
            "currency": {"code": currency} if currency else None,
            "savings-pct": savings_pct,
            "stop-spend-based-on-max-value": stop_spend_based_on_max_value,
            "shipping-term": {"code": shipping_term} if shipping_term else None,
            "min-commit": min_commit,
            "max-commit": max_commit,
        }.items()
        if value is not None
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
        message="The contract payment terms were successfully updated",
        content=CoupaUpdateContractPaymentResult(id=response["id"], status=response["status"]),
    )
