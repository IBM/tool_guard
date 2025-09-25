from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class CustomFields:
    """Represents a single custom field."""

    field_id: str
    title: str
    key: Optional[str] = None


@dataclass
class CustomFieldsResponse:
    """Represents the result of retrieving all custom fields from Zendesk."""

    custom_fields: List[CustomFields]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_custom_fields(object_name: str) -> CustomFieldsResponse:
    """
    Get all the custom fields from Zendesk.

    Args:
        object_name: The name of the object (e.g., organization, ticket).

    Returns:
        The list of custom fields.
    """
    try:
        client = get_zendesk_client()
        field_name = f"{object_name.lower()}_fields"
        response = client.get_request(entity=field_name)
        custom_fields: List[CustomFields] = [
            CustomFields(field_id=str(item["id"]), title=item["title"], key=item.get("key"))
            for item in response[field_name]
        ]
        return CustomFieldsResponse(custom_fields=custom_fields)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return CustomFieldsResponse(
            custom_fields=[],
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return CustomFieldsResponse(
            custom_fields=[],
            http_code=500,
            error_message=str(e),
        )
