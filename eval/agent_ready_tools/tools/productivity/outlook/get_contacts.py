from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Contacts:
    """Represents a contact record in Microsoft Outlook."""

    email_address: str
    contact_name: Optional[str] = None
    phone_number: Optional[str] = None
    folder_name: Optional[str] = None


@dataclass
class ContactsResponse:
    """Represents the list of contacts in Microsoft Outlook."""

    contacts_list: List[Contacts]
    limit: Optional[int]
    skip: Optional[int]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_contacts(
    contact_name: Optional[str] = None,
    email_address: Optional[str] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> ContactsResponse:
    """
    Retrieves the list of contacts in Microsoft Outlook.

    Args:
        contact_name: The name of the contact in Microsoft Outlook.
        email_address: The email address of the contact in Microsoft Outlook.
        limit: The maximum number of contacts to retrieve.
        skip: The number of contacts to skip for pagination.

    Returns:
        A list of contacts in Microsoft Outlook.
    """

    client = get_microsoft_client()

    query = None
    if contact_name and email_address:
        query = f"displayName eq '{contact_name}' and emailAddresses/any(a:a/address eq '{email_address}')"
    elif contact_name:
        query = f"displayName eq '{contact_name}'"
    elif email_address:
        query = f"emailAddresses/any(a:a/address eq '{email_address}')"

    params = {"$top": limit, "$skip": skip, "$filter": query}

    # Filters out the parameters that are None/blank.
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(
        endpoint=f"{client.get_user_resource_path()}/contacts", params=params
    )

    contacts_list: list[Contacts] = []

    contacts_list = [
        Contacts(
            contact_name=item.get("displayName", ""),
            email_address=(
                ", ".join([email.get("address", "") for email in item.get("emailAddresses", [])])
                if item.get("emailAddresses")
                else ""
            ),
            folder_name=(
                ", ".join(item.get("categories", []))
                if isinstance(item.get("categories"), list)
                else ""
            ),
            phone_number=item.get("mobilePhone", ""),
        )
        for item in response.get("value", [])
    ]

    # Extract limit and skip from @odata.nextLink if it exists
    output_limit = None
    output_skip = None
    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(next_api_link)
        output_limit = int(query_params["$top"])
        output_skip = int(query_params["$skip"])

    return ContactsResponse(
        contacts_list=contacts_list,
        limit=output_limit,
        skip=output_skip,
    )
