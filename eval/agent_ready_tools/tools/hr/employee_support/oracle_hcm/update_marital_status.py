from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UpdateMaritalStatusResponse:
    """Represents the result of the update action of an employee's marital status."""

    http_code: int


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_marital_status(
    worker_id: str, legislative_id: str, marital_status_id: Optional[str]
) -> UpdateMaritalStatusResponse:
    """
    Updates the marital status of an employee in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.
        legislative_id: The person's legislative_id uniquely identifying them within the Oracle HCM
            returned by the `get_user_legislative_id` tool.
        marital_status_id: The marital_status_id of the marital status of an employee returned by
            the tool `get_martial_statuses`.

    Returns:
        The result from performing the update martial status tool.
    """

    client = get_oracle_hcm_client()

    payload: dict[str, Any] = {"MaritalStatus": marital_status_id}

    # Filter out the blank parameters.
    payload = {key: value for key, value in payload.items() if value}

    entity = f"workers/{worker_id}/child/legislativeInfo/{legislative_id}"

    response = client.update_request(entity=entity, payload=payload)

    http_code = response.get("status_code", "")

    return UpdateMaritalStatusResponse(http_code)
