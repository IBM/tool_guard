from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class CreateContactResponse:
    """Represents the result of creating a contact in Microsoft Outlook."""

    email_address: str
    first_name: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def create_a_contact(
    email_address: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone_number: Optional[str] = None,
) -> CreateContactResponse:
    """
    Creates a contact in Microsoft Outlook.

    Args:
        email_address: The email address of the contact.
        first_name: The first name of the contact.
        last_name: The last name of the contact.
        phone_number: The mobile phone number of the contact.

    Returns:
        The result after creating the contact.
    """
    client = get_microsoft_client()

    payload = {
        "givenName": first_name,
        "surname": last_name,
        "emailAddresses": [{"address": email_address}],
        "mobilePhone": phone_number,
    }
    # Filter out the parameters that are None.
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/contacts", data=payload
    )
    return CreateContactResponse(
        first_name=response.get("givenName", ""),
        email_address=response.get("emailAddresses", [{}])[0].get("address"),
    )
