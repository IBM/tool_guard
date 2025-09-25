from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import get_all_custom_objects
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class DeleteCustomObjectRecordResponse:
    """Represents the result of deleting an custom object record in Zendesk."""

    http_code: int
    error_message: Optional[str] = None
    error_description: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def delete_custom_object_record(
    custom_object_key: str, custom_object_record_id: str
) -> DeleteCustomObjectRecordResponse:
    """
    Deletes a custom object record in Zendesk.

    Args:
        custom_object_key: The key of the custom object used to identify the record to delete.
        custom_object_record_id: The ID of the record to be deleted from the custom object.

    Returns:
        The result of the deletion operation, including HTTP status and error details if any.
    """

    custom_objects = get_all_custom_objects()

    # checks if the provided custom object key is configured or not.

    if custom_object_key not in custom_objects:
        return DeleteCustomObjectRecordResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=f"An exception occurred during the API call: custom object {custom_object_key} is not valid",
        )

    client = get_zendesk_client()

    try:
        response = client.delete_request(
            entity=f"custom_objects/{custom_object_key}/records/{custom_object_record_id}"
        )
        return DeleteCustomObjectRecordResponse(
            http_code=response.get("status_code", HTTPStatus.OK.value)
        )
    except HTTPError as e:
        error_response = e.response.json()
        error_message = error_response.get("error", HTTPStatus.INTERNAL_SERVER_ERROR.value)
        error_description = error_response.get("description", "")
        return DeleteCustomObjectRecordResponse(
            http_code=e.response.status_code,
            error_message=error_message,
            error_description=error_description,
        )
    except Exception as e:  # pylint: disable=broad-except
        error_message = str(e)
        return DeleteCustomObjectRecordResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=error_message,
            error_description="An unexpected error occurred.",
        )
