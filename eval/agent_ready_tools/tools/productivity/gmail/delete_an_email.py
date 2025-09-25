from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import RequestException

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class DeleteEmailResponse:
    """Represents the response of the send an email in Gmail."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def delete_an_email(message_id: str) -> DeleteEmailResponse:
    """
    Deletes an email using Gmail API.

    Args:
        message_id: The unique identifier of email message in gmail, as specified by the `list_emails` tool.

    Returns:
        DeleteEmailResponse with status code.
    """
    try:
        client = get_google_client()

        response = client.delete_request(
            entity=f"users/me/messages/{message_id}", service="gmail", version="v1"
        )
        return DeleteEmailResponse(http_code=response, message="Deleted the email successfully.")

    except RequestException as e:
        message = f"An unexpected error occurred: {e}"

        return DeleteEmailResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, message=message
        )
