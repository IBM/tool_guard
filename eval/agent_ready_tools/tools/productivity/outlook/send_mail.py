from typing import Dict, Iterator, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class SendMailResponse:
    """Represents the result of sending an email in Outlook."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def send_mail(
    email_body: str,
    email_address: Union[Iterator[str], str],
    subject: str,
    cc_email_address: Optional[Union[List[str], str]] = None,
    content_type: Optional[str] = "Text",
) -> SendMailResponse:
    """
    Sends a mail from outlook.

    Args:
        email_body: The content being passed in message body.
        email_address: The list of recipient email addresses.
        subject: The subject of the email.
        cc_email_address: The list of cc email addresses.
        content_type: The default value is Text, it can take Text/HTML.

    Returns:
        Confirmation that the email was sent.
    """

    client = get_microsoft_client()

    email_addresses: List[str] = list(
        [email_address] if isinstance(email_address, str) else email_address
    )
    to_recipients: List[Dict[str, Dict[str, str]]] = [
        {"emailAddress": {"address": mail}} for mail in email_addresses
    ]
    cc_email_addresses: List[str] = (
        [cc_email_address] if isinstance(cc_email_address, str) else cc_email_address or []
    )

    to_cc_recipients: Union[List[Dict[str, Dict[str, str]]], None] = (
        [{"emailAddress": {"address": mail}} for mail in cc_email_addresses]
        if cc_email_addresses
        else None
    )

    payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": content_type, "content": email_body},
            "toRecipients": to_recipients,
            "ccRecipients": to_cc_recipients,
        },
    }

    payload["message"] = {key: value for key, value in payload["message"].items() if value}

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/sendMail", data=payload
    )
    return SendMailResponse(http_code=int(response["status_code"]))
