import logging
from typing import Any, Dict, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import RequestException

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import (
    get_all_custom_objects,
    get_custom_object_fields,
)
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class UpdateCustomRecordResponse:
    """Represents the result of updating an custom object record in Zendesk."""

    custom_object_record_id: Optional[str] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def update_custom_object_record(
    input_data: Dict[str, Any], custom_object_key: str, custom_object_record_id: str
) -> UpdateCustomRecordResponse:
    """
    Updates a custom object record in Zendesk.

    Args:
        input_data: The input data used for updating a record.
        custom_object_key: The Key of the custom object for updating a record in Zendesk.
        custom_object_record_id: The record id of the existing record returned from get_custom_object_records tool in zendesk.

    Returns:
        The result from performing the updation of a record.
    """

    # calling utility function to retrieve the configured custom objects.
    custom_objects = get_all_custom_objects()

    # checks if the provided custom object key is configured or not.
    if custom_object_key not in custom_objects:
        error_message = f"An exception occurred during the API call: custom object {custom_object_key} is not valid"
        return UpdateCustomRecordResponse(error_message=error_message)

    # calling utility function to retrieve the configured custom fields for an object.
    custom_object_fields = get_custom_object_fields(custom_object_key)

    payload: Dict[str, Any] = {"custom_object_record": {"custom_object_fields": {}}}

    # Handling custom fields for updating the records.
    for key, value in input_data.items():
        if key == "name":
            payload["custom_object_record"][key] = value
        # checks if the keys passed as input are configured or not for current custom object.
        elif key in custom_object_fields:
            payload["custom_object_record"]["custom_object_fields"][key] = value
        else:
            error_message = f"custom field '{key}' is not valid.{key} is not configured for this custom object {custom_object_key}."
            return UpdateCustomRecordResponse(error_message=error_message)

    if payload["custom_object_record"]["custom_object_fields"] == {}:
        del payload["custom_object_record"]["custom_object_fields"]

    client = get_zendesk_client()

    try:
        response = client.patch_request(
            entity=f"custom_objects/{custom_object_key}/records/{custom_object_record_id}",
            payload=payload,
        )
        record_id = response.get("custom_object_record", {}).get("id", "")
        return UpdateCustomRecordResponse(custom_object_record_id=record_id)
    except RequestException as e:
        response = e.response.json() if e.response is not None else {}
        message = response.get("error", {}).get("message", "")
        error_message = f"An exception occurred during the API call: {message}"
        logging.error(
            error_message,
            exc_info=True,
        )
        return UpdateCustomRecordResponse(error_message=error_message)
