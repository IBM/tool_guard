from typing import Dict, Iterator, List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class ReplyEmailResponse:
    """Represents the result of replying to an email in Microsoft Outlook."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def reply_to_email(
    message_id: str, sender_email_address: Iterator[str] | str, comment: str
) -> ReplyEmailResponse:
    """
    Replies to an email in Microsoft Outlook.

    Args:
        message_id: The unique identifier of the email to which the user has to reply, returned from
            `get_emails_from_folder` tool.
        sender_email_address: The email address of the sender.
        comment: The actual content of the reply message.

    Returns:
        The result from replying to the email.
    """
    client = get_microsoft_client()

    sender_email_addresses: List[str] = list(
        [sender_email_address] if isinstance(sender_email_address, str) else sender_email_address
    )

    to_recipients: List[Dict[str, Dict[str, str]]] = [
        {"emailAddress": {"address": email_address}} for email_address in sender_email_addresses
    ]

    payload = {
        "message": {"toRecipients": to_recipients},
        "comment": comment,
    }

    response = client.post_request(
        endpoint=f"{client.get_user_resource_path()}/messages/{message_id}/reply", data=payload
    )
    return ReplyEmailResponse(http_code=response["status_code"])
