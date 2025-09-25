import base64
from email.message import EmailMessage
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class SendEmailResponse:
    """Represents the response of the send an email in Gmail."""

    label: str


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def send_an_email(
    email_address: str,
    body: str,
    subject: str,
    cc_email_address: Optional[str] = None,
    bcc_email_address: Optional[str] = None,
) -> SendEmailResponse:
    """
    Sends a email using Gmail API.

    Args:
        email_address: The email address of the recipient.
        body: The body content of the email.
        subject: The subject of the email.
        cc_email_address: The carbon copy(cc) email address of the recipient.
        bcc_email_address: The blind carbon copy(bcc) email address of the recipient.

    Returns:
        SendEmailResponse with message status.
    """

    client = get_google_client()
    content = EmailMessage()
    content.set_content(body)

    content["To"] = email_address
    content["Subject"] = subject
    if cc_email_address:
        content["Cc"] = cc_email_address
    if bcc_email_address:
        content["Bcc"] = bcc_email_address

    # encoded message
    encoded_message = base64.urlsafe_b64encode(content.as_bytes()).decode()

    payload = {"raw": encoded_message}

    response = client.post_request(
        entity="users/me/messages/send", service="gmail", version="v1", payload=payload
    )

    return SendEmailResponse(
        label=(
            response.get("labelIds", [])[0]
            if response.get("labelIds")
            else "Email could not be sent."
        )
    )
