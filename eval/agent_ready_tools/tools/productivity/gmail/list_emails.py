from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class Email:
    """Represents a email message from Gmail."""

    id: str
    body: str
    subject: str
    from_address: str
    to_address: str
    date: str


@dataclass
class EmailsResponse:
    """Represents a list of email messages."""

    emails: List[Email]
    limit: Optional[int] = 0
    next_page_token: Optional[str] = None


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def list_emails(
    to_address: Optional[str] = None,
    subject: Optional[str] = None,
    limit: Optional[int] = 5,
    next_page_token: Optional[str] = None,
) -> EmailsResponse:
    """
    Retrieves a list of email messages from Gmail.

    Args:
        to_address: Filter email messages sent to this address.
        subject: The subject of the email.
        limit: The maximum number of emails retrieved in a single API call. Defaults to 5.
        next_page_token: A token used for pagination to retrieve the next set of results.

    Returns:
        List of email messages from Gmail, along with pagination parameters (limit and next_page_token).
    """

    client = get_google_client()

    # Build search query
    query = ""
    if to_address:
        query = f"to:{to_address} "
    if subject:
        query += f"subject:{subject}"

    # Step 1: List emails
    params = {"maxResults": limit, "pageToken": next_page_token, "q": query}

    response = client.get_request(
        entity="users/me/messages", service="gmail", version="v1", params=params
    )
    messages = response.get("messages", [])

    # Step 2: Get details for each email
    detailed_emails = []

    for msg in messages:
        email_message_id = msg.get("id")

        detail = client.get_request(
            entity=f"users/me/messages/{email_message_id}", service="gmail", version="v1"
        )
        payload = detail.get("payload", {})
        headers = payload.get("headers", [])

        subject_value = next(
            (header["value"] for header in headers if header["name"].lower() == "subject"), None
        )
        from_address_value = next(
            (header["value"] for header in headers if header["name"].lower() == "from"), None
        )
        to_address_value = next(
            (header["value"] for header in headers if header["name"].lower() == "to"), None
        )
        date_value = next(
            (header["value"] for header in headers if header["name"].lower() == "date"), None
        )

        detailed_emails.append(
            Email(
                id=detail.get("id", ""),
                body=detail.get("snippet", ""),
                subject=subject_value or "",
                from_address=from_address_value or "",
                to_address=to_address_value or "",
                date=date_value or "",
            )
        )

    return EmailsResponse(
        emails=detailed_emails, limit=limit, next_page_token=response.get("nextPageToken", "")
    )
