from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Organization:
    """Represents the result of Organization object in Outlook."""

    id: str
    name: str


@dataclass
class GetOrganizationsResponse:
    """Represents the result of an event delete operation in Outlook."""

    organizations: list[Organization]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_organizations() -> GetOrganizationsResponse:
    """
    Get list of organizations from Outlook.

    Returns:
        List of organizations.
    """
    client = get_microsoft_client()

    endpoint = "organization"
    response = client.get_request(endpoint)
    organizations: list[Organization] = []

    for organization in response["value"]:
        organizations.append(
            Organization(id=organization.get("id", ""), name=organization.get("displayName", ""))
        )

    return GetOrganizationsResponse(organizations=organizations)
