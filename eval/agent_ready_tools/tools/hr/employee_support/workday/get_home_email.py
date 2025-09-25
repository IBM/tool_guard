from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class HomeEmailAddress:
    """Represents a home email in Workday."""

    email_id: str
    email_address: str


@dataclass
class GetHomeEmailResponse:
    """Represents the response from getting a user's home email addresses in Workday."""

    email_addresses: list[HomeEmailAddress]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_home_email(person_id: str) -> GetHomeEmailResponse:
    """
    Gets a user's home email in Workday.

    Args:
        person_id: The user's person_id uniquely identifying them within the Workday API.

    Returns:
        The user's home email addresses.
    """
    client = get_workday_client()

    url = f"api/person/v4/{client.tenant_name}/people/{person_id}/homeEmails"
    response = client.get_request(url=url)

    email_addresses: list[HomeEmailAddress] = []
    for email in response["data"]:
        email_addresses.append(
            HomeEmailAddress(
                email_id=email.get("id"),
                email_address=email.get("emailAddress"),
            )
        )
    return GetHomeEmailResponse(email_addresses=email_addresses)
