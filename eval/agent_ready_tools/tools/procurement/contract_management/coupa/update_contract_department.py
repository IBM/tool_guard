from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.contract_management.coupa.update_contract_details import (
    CoupaUpdateContractResult,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_update_contract_department(
    contract_id: str,
    coupa_department_id: int,
) -> ToolResponse[CoupaUpdateContractResult]:
    """
    Update a Department for a contract.

    Args:
        contract_id: Contract ID.
        coupa_department_id: The Department ID of a contract

    Returns:
        The result of updating a contract's payment details
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    payload = {
        "department": {
            "id": coupa_department_id,
        }
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
        message="The contract was department was successfully updated",
        content=CoupaUpdateContractResult(id=response["id"], status=response["status"]),
    )
