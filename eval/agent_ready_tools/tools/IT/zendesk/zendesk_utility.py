from enum import StrEnum
from typing import Any, Dict, List, Optional, Type

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_schemas import ZendeskRole


def get_custom_object_fields(custom_object_key: str) -> List:
    """
    Gets the configured fields for a custom object in Zendesk.

    Args:
        custom_object_key: The Key of the custom object for updating a record in Zendesk.

    Returns:
        The result from performing the retreiving of fields.
    """

    client = get_zendesk_client()

    response = client.get_request(entity=f"custom_objects/{custom_object_key}/fields")

    custom_object_fields: List[str] = []
    for fields in response["custom_object_fields"]:
        field = fields.get("key", "")
        custom_object_fields.append(field)

    return custom_object_fields


def get_all_custom_objects() -> List:
    """
    Gets the available custom objects configured in Zendesk.

    Returns:
        The result from performing the retreiving of custom objects.
    """

    client = get_zendesk_client()

    response = client.get_request(entity=f"custom_objects")

    custom_objects: List[str] = []
    for objects in response["custom_objects"]:
        custom_object = objects.get("key", "")
        custom_objects.append(custom_object)

    return custom_objects


def get_name_by_id(data: List[dict], target_id: str) -> Optional[str]:
    """
    Fetch the 'name' field from a collection in the data dict by matching 'id'.

    Args:
        data (list[dict]): The data list containing collections like 'users' or 'organizations'.
        target_id (str): The ID to search for.

    Returns:
        Optional[str]: The name if found, otherwise None.
    """
    for item in data:
        if item.get("id") == target_id:
            return item.get("name")
    return None


def get_custom_field_key_id(
    custom_fields: List[Dict[str, Any]], custom_field_name: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Maps custom field IDs to their titles and values.

    Args:
        custom_fields (List[Dict[str, Any]]): The custom fields from the API response.
        custom_field_name (List[Dict[str, Any]]): The list of custom fields with their IDs and titles.

    Returns:
        Dict[str, Any]: A dictionary mapping custom field titles to their values.
    """
    custom_field_mapping = {field["id"]: field["title"] for field in custom_field_name}
    mapped_fields = {
        custom_field_mapping.get(field["id"], ""): field["value"] for field in custom_fields
    }
    return mapped_fields


def validate_enum_value(
    value: Optional[str], enum_class: Type[StrEnum], field_name: str
) -> Optional[str]:
    """
    Validates the enum values in Zendesk.

    Args:
        value: The field to be passed for validation.
        enum_class: The enum class to be used for validation.
        field_name: The name of the field to be displayed as an output.
    Returns:
       The value of the enum class.
    """
    if value:
        valid_values = [item.name for item in enum_class]
        value_upper = value.upper()
        if value_upper not in valid_values:
            raise ValueError(
                f"{field_name} '{value}' is not a valid value. Accepted values are {valid_values}."
            )
        return enum_class[value_upper].value
    return None


def validate_role_enum_value(role: Optional[str]) -> Optional[str]:
    """
    Validates the role value against ZendeskRole enum.

    Args:
        role: The role string to validate.

    Returns:
        The validated role value from ZendeskRole.

    Raises:
        ValueError: If the role is not a valid ZendeskRole.
    """
    if role:
        valid_values = [item.name for item in ZendeskRole]
        role_upper = role.upper().replace("-", "_").replace(" ", "_")
        if role_upper not in valid_values:
            raise ValueError(
                f"Role '{role}' is not a valid value. Accepted values are {valid_values}."
            )
        return ZendeskRole[role_upper].value
    return None
