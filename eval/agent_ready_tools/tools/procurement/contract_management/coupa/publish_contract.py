from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@dataclass
class CoupaPublishContractResult:
    """Represents the result of publishing a contract in Coupa."""

    id: int
    status: str


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_publish_contract(contract_id: int) -> ToolResponse[CoupaPublishContractResult]:
    """
    Publish a contract in Coupa.

    Args:
        contract_id: Contract id.

    Returns:
        The result of publishing a contract.
    """

    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    response = client.put_request(
        resource_name=f"contracts/{contract_id}",
        params={"fields": '["id","status"]'},
        payload={"status": "published"},
    )

    if "errors" in response:
        return ToolResponse(
            success=False, message=coupa_format_error_string(response), content=None
        )

    return ToolResponse(
        success=True,
        message="The contract was successfully published",
        content=CoupaPublishContractResult(id=response["id"], status=response["status"]),
    )
