from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class UpdateEmailAddressResponse:
    """Represents the result of email update operation in Oracle HCM."""

    email_address: str
    email_type: str


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def update_email_address(
    worker_id: str, email_id: int, email_address: str, email_type: str
) -> UpdateEmailAddressResponse:
    """
    Updates a user's email address in Oracle HCM.

    Args:
        worker_id: The user's worker_id uniquely identifying them within the Oracle HCM API, as
            specified by the `get_user_oracle_ids` tool.
        email_id: "The user's email_id uniquely identifying them within the Oracle HCM API, as
            specified by the `get_emails_ids` tool"
        email_address: "The user's email_address"
        email_type: "The user's email_type, as specified by the `get_email_types_oracle` tool"

    Returns:
        The user's email details.
    """
    client = get_oracle_hcm_client()

    payload = {
        "EmailAddress": email_address,
        "EmailType": email_type,
    }

    entity = f"workers/{worker_id}/child/emails/{email_id}"
    response = client.update_request(payload=payload, entity=entity)

    return UpdateEmailAddressResponse(
        email_address=response.get("EmailAddress", ""),
        email_type=response.get("EmailType", ""),
    )
