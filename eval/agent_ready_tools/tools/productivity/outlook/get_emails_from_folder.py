from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Emails:
    """Represents the details of an email in Microsoft Outlook."""

    message_id: str
    recipient_email_address: str
    subject: str
    body: str
    sender_email_address: str
    sender_name: str


@dataclass
class EmailsResponse:
    """Represents a list of emails within a folder of a Microsoft Outlook."""

    emails: List[Emails]
    limit: Optional[int]
    skip: Optional[int]


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_emails_from_folder(
    folder_id: str,
    sender_name: Optional[str] = None,
    sender_email_address: Optional[str] = None,
    limit: Optional[int] = 20,
    skip: Optional[int] = 0,
) -> EmailsResponse:
    """
    Retrieves a list of Emails in Microsoft Outlook.

    Args:
        folder_id: The folder id returned by the `get_mail_folders` tool.
        sender_name: The name of the sender.
        sender_email_address: The email address of the sender.
        limit: The maximum number of emails in a folder to retrieve in a single API call. Defaults
            to 100. Use this to control the size of the result set.
        skip: The number of emails in a folder to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of all the emails from folder, along with pagination parameters (limit and skip).
    """

    client = get_microsoft_client()
    params = {
        "$filter": (
            f"sender/emailAddress/address eq '{sender_email_address}'"
            if sender_email_address
            else (None or f"sender/emailAddress/name eq '{sender_name}'" if sender_name else None)
        ),
        "$top": limit,
        "$skip": skip,
    }
    # Filters out the parameters that are None/Blank.
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(
        endpoint=f"{client.get_user_resource_path()}/mailFolders/{folder_id}/messages",
        params=params,
    )

    emails: List[Emails] = []

    for email in response.get("value", []):
        recipient = email.get("toRecipients", [])
        recipient_email_address = (
            recipient[0].get("emailAddress", {}).get("address", "") if recipient else ""
        )

        emails.append(
            Emails(
                message_id=email.get("id", ""),
                recipient_email_address=recipient_email_address,
                subject=email.get("subject", ""),
                body=email.get("bodyPreview", ""),
                sender_email_address=email.get("sender", {})
                .get("emailAddress", {})
                .get("address", ""),
                sender_name=email.get("sender", {}).get("emailAddress", {}).get("name", ""),
            )
        )
    # Extract limit and skip from @odata.nextLink if it exists
    output_limit = None
    output_skip = None
    next_api_link = response.get("@odata.nextLink", "")
    if next_api_link:
        query_params = get_query_param_from_links(next_api_link)
        output_limit = int(query_params["$top"])
        output_skip = int(query_params["$skip"])

    return EmailsResponse(
        emails=emails,
        limit=output_limit,
        skip=output_skip,
    )
