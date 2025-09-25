from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@dataclass
class SalesforceCreateContactResponse:
    """Represents the result of creating a contact in Salesforce."""

    contact_id: str


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def salesforce_create_contact(
    last_name: str,
    title: str,
    email: str,
    phone_number: str,
    first_name: Optional[str] = None,
    account_id: Optional[str] = None,
) -> SalesforceCreateContactResponse:
    """
    Creates a contact in Salesforce.

    Args:
        last_name: The last name of the contact.
        title: The title of the contact.
        email: The email address of the contact.
        phone_number: The phone number of the contact.
        first_name: The first name of the contact.
        account_id: The id of the account, returned by the tool `list_accounts` in Salesforce.

    Returns:
        The result of creating a contact.
    """

    client = get_salesforce_client()

    payload: dict[str, Any] = {
        "LastName": last_name,
        "Title": title,
        "Email": email,
        "Phone": phone_number,
        "FirstName": first_name,
        "AccountId": account_id,
    }
    # Filter out the parameters that are None/Blank
    payload = {key: value for key, value in payload.items() if value}

    response = client.salesforce_object.Contact.create(data=payload)  # type: ignore[operator]

    return SalesforceCreateContactResponse(contact_id=response.get("id", ""))
