from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.coupa.contract_dataclasses import (
    CoupaContract,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_contract_details(
    contract_id: int,
) -> ToolResponse[List[CoupaContract]]:
    """
    Get all details from a single contract from Coupa.

    Args:
        contract_id: The contract ID provides details from the resource.

    Returns:
        A list with one CoupaContract object containing the contract's details.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    # Construct the endpoint for the specific contract
    resource_name = f"contracts/{contract_id}"

    # Use the correct client method for a single resource
    contract_detail = client.get_request(
        resource_name=resource_name,
    )

    if len(contract_detail) == 1 and "errors" in contract_detail:
        return ToolResponse(
            success=False, message=coupa_format_error_string(contract_detail), content=None
        )

    found_contract_details = []
    found_contract_details.append(
        CoupaContract.from_fields(
            contract_id=contract_detail.get("id", 0),
            name=contract_detail.get("name", ""),
            no_of_renewals=contract_detail.get("no-of-renewals", 0),
            number=contract_detail.get("number", ""),
            reason_insight_events=contract_detail.get("reason-insight-events", []),
            renewal_length_unit=contract_detail.get("renewal-length-unit", ""),
            renewal_length_value=contract_detail.get("renewal-length-value", 0),
            status=contract_detail.get("status", ""),
            start_date=contract_detail.get("start-date", ""),
            end_date=contract_detail.get("end-date", ""),
            supplier_name=(contract_detail.get("supplier") or {}).get("name", ""),
            supplier_number=(contract_detail.get("supplier") or {}).get("number", ""),
            supplier_id=(contract_detail.get("supplier") or {}).get("id"),
            supplier_status=(contract_detail.get("supplier") or {}).get("status", ""),
            supplier_contact_email=(contract_detail.get("supplier") or {})
            .get("primary-contact", {})
            .get("email", ""),
            payment_term_id=(contract_detail.get("payment-term") or {}).get("id"),
            payment_term_code=(contract_detail.get("payment-term") or {}).get("code", ""),
            coupa_contract_department_id=(contract_detail.get("department") or {}).get("id"),
            coupa_contract_department_name=(contract_detail.get("department") or {}).get(
                "name", ""
            ),
            coupa_contract_department_status=(contract_detail.get("department") or {}).get(
                "active", False
            ),
        )
    )

    # Parse the response into a CoupaContract object
    return ToolResponse(
        success=True,
        message="The contract details were successfully gathered ",
        content=found_contract_details,
    )
