from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS

EMAIL_TYPE = "H1"  # Default email type set as 'H1' for home email address


@dataclass
class CreateWorkerHomeEmailResponse:
    """Represents the results of creating worker home email address in Oracle HCM."""

    http_code: int


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_worker_home_email(worker_id: str, email_address: str) -> CreateWorkerHomeEmailResponse:
    """
    Creates a worker home email address.

    Args:
        worker_id: The worker_id uniquely identifies workers within the Oracle HCM, returned by the
            `get_user_oracle_ids` tool.
        email_address: The home email address of the worker.

    Returns:
        The status of the create worker email address operation.
    """

    client = get_oracle_hcm_client()

    payload = {"EmailAddress": email_address, "EmailType": EMAIL_TYPE}

    entity = f"workers/{worker_id}/child/emails"
    response = client.post_request(entity=entity, payload=payload)

    http_code = response.get("status_code", "")

    return CreateWorkerHomeEmailResponse(http_code)
