from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import ToolPermission, tool

from agent_ready_tools.clients.salesforce_client import get_salesforce_client
from agent_ready_tools.utils.tool_credentials import SALESFORCE_CONNECTIONS


@tool(
    permission=ToolPermission.WRITE_ONLY,
    expected_credentials=SALESFORCE_CONNECTIONS,
)
def update_contact(
    contact_id: str,
    last_name: Optional[str] = None,
    first_name: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    title: Optional[str] = None,
    account_id: Optional[str] = None,
    mailing_country: Optional[str] = None,
    mailing_state: Optional[str] = None,
    mailing_city: Optional[str] = None,
    mailing_street: Optional[str] = None,
    mailing_postal_code: Optional[str] = None,
) -> int:
    """
    Updates an existing contact in Salesforce.

    Args:
        contact_id: The contact id used to update the contact in Salesforce.It is returned by
            'list_contacts' tool.
        last_name: The last name of the contact to be updated in Salesforce.
        first_name: The first name of the contact to be updated in Salesforce.
        email: The email of the contact to be updated in Salesforce.
        phone_number: The phone number of the contact to be updated in Salesforce.
        title: The title to be updated in Salesforce.
        account_id: The id of the account in Salesforce.It is returned by 'list_accounts' tool.
        mailing_country: The mailing country of the contact.It is returned by 'list_countries' tool.
        mailing_state: The mailing state of the contact.It is returned by 'list_states' tool.
        mailing_city: The mailing city of the contact.
        mailing_street: The mailing street of the contact.
        mailing_postal_code: The mailing postal code  of the contact.

    Returns:
        The status of the update operation performed on the contact.
    """
    client = get_salesforce_client()
    data = {
        "LastName": last_name,
        "FirstName": first_name,
        "Email": email,
        "Phone": phone_number,
        "Title": title,
        "AccountId": account_id,
        "MailingCountry": mailing_country,
        "MailingState": mailing_state,
        "MailingCity": mailing_city,
        "MailingStreet": mailing_street,
        "MailingPostalCode": mailing_postal_code,
    }

    # Filter out the blank parameters.
    data = {key: value for key, value in data.items() if value}
    status = client.salesforce_object.Contact.update(contact_id, data)  # type: ignore[operator]

    return status
