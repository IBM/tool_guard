import logging
from typing import Any, Dict

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from requests.exceptions import RequestException

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import CustomObjectDefaultFields
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import (
    get_all_custom_objects,
    get_custom_object_fields,
)
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def create_custom_object_record(input_data: Dict[str, Any], custom_object_key: str) -> str:
    """
    Creates a custom object record in Zendesk.

    Args:
        input_data: The input data used for creating a record in Zendesk.
        custom_object_key: The Key of the custom object for creating a record in Zendesk.

    Returns:
        The result from performing the creation of a record.
    """

    # calling utility function to retrieve the configured custom objects.
    custom_objects = get_all_custom_objects()

    # checks if the provided custom object key is configured or not.
    if custom_object_key not in custom_objects:
        return f"An exception occurred during the API call: custom object {custom_object_key} is not valid"

    # calling utility function to retrieve the configured custom fields for an object.
    custom_object_fields = get_custom_object_fields(custom_object_key)

    payload: Dict[str, Any] = {
        CustomObjectDefaultFields.CUSTOM_OBJECT_RECORD: {
            CustomObjectDefaultFields.NAME: input_data[CustomObjectDefaultFields.NAME],
            CustomObjectDefaultFields.CUSTOM_OBJECT_FIELDS: {},
        }
    }

    if CustomObjectDefaultFields.EXTERNAL_ID in input_data:
        payload[CustomObjectDefaultFields.CUSTOM_OBJECT_RECORD][
            CustomObjectDefaultFields.EXTERNAL_ID
        ] = input_data[CustomObjectDefaultFields.EXTERNAL_ID]

    for key, value in input_data.items():
        if key in [CustomObjectDefaultFields.NAME, CustomObjectDefaultFields.EXTERNAL_ID]:
            continue
        if key in custom_object_fields:
            payload[CustomObjectDefaultFields.CUSTOM_OBJECT_RECORD][
                CustomObjectDefaultFields.CUSTOM_OBJECT_FIELDS
            ][key] = value
        else:
            return f"Custom field '{key}' is not valid. '{key}' is not configured for this custom object '{custom_object_key}'."

    if (
        payload[CustomObjectDefaultFields.CUSTOM_OBJECT_RECORD][
            CustomObjectDefaultFields.CUSTOM_OBJECT_FIELDS
        ]
        == {}
    ):
        del payload[CustomObjectDefaultFields.CUSTOM_OBJECT_RECORD][
            CustomObjectDefaultFields.CUSTOM_OBJECT_FIELDS
        ]

    client = get_zendesk_client()

    try:
        response = client.post_request(
            entity=f"custom_objects/{custom_object_key}/records", payload=payload
        )
        return response.get(CustomObjectDefaultFields.CUSTOM_OBJECT_RECORD, {}).get(
            CustomObjectDefaultFields.NAME, ""
        )
    except RequestException as e:
        response = e.response.json() if e.response is not None else {}
        message = response.get("details", {}).get(CustomObjectDefaultFields.EXTERNAL_ID, [])
        error_message = (
            f"An exception occurred during the API call: {message[0].get("description","")}"
        )
        logging.error(
            error_message,
            exc_info=True,
        )
        return error_message
