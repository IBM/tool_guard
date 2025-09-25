from typing import Any, Dict, Iterator, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class ForwardAnEmailResponse:
    """Represents the result of forwarding an email in Microsoft Outlook."""

    http_code: int


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def forward_an_email(
    message_id: str,
    recipient_email_address: Union[Iterator[str] | str],
    comment: Optional[str] = None,
) -> ForwardAnEmailResponse:
    """
    Forwards the email to the intended recipient in Microsoft Outlook.

    Args:
        message_id: The message id uniquely identifying the email, returned by the tool
            `get_emails_from_folder`.
        recipient_email_address: The email address of the recipients.
        comment: The content to be given inside the email.

    Returns:
        The result from performing forward an email.
    """

    client = get_microsoft_client()

    recipient_email_addresses: List[str] = list(
        [recipient_email_address]
        if isinstance(recipient_email_address, str)
        else recipient_email_address
    )

    to_recipients: List[Dict[str, Dict[str, str]]] = [
        {"emailAddress": {"address": mail}} for mail in recipient_email_addresses
    ]

    data: dict[str, Any] = {"toRecipients": to_recipients}
    if comment is not None:
        data["comment"] = comment

    endpoint_expr = f"{client.get_user_resource_path()}/messages/{message_id}/forward"

    response = client.post_request(endpoint=endpoint_expr, data=data)

    return ForwardAnEmailResponse(http_code=response["status_code"])
