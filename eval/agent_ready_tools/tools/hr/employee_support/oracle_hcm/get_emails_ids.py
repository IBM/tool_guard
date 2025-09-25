from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class EmailId:
    """Represents an email id in Oracle HCM."""

    email_id: int
    email_address: str


@dataclass
class EmailsIdsResponse:
    """Represents the response from getting all user's emails ids from Oracle HCM."""

    emails_ids: List[EmailId]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_emails_ids(worker_id: str) -> EmailsIdsResponse:
    """
    Gets all user's emails ids from Oracle HCM.

    Args:
        worker_id: The user's worker_id uniquely identifying them within the Oracle HCM API, as
            specified by the get_user_oracle_ids tool.

    Returns:
        The all user's emails ids.
    """
    client = get_oracle_hcm_client()

    entity = f"workers/{worker_id}/child/emails"
    response = client.get_request(entity=entity)

    emails_ids: List[EmailId] = []
    for result in response.get("items", []):
        emails_ids.append(
            EmailId(
                email_id=result.get("EmailAddressId", ""),
                email_address=result.get("EmailAddress", ""),
            )
        )
    return EmailsIdsResponse(emails_ids=emails_ids)
