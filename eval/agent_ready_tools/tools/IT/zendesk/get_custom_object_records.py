import logging
from typing import Any, Dict, List, Optional, Union

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic import BaseModel
from requests.exceptions import RequestException

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.tools.IT.zendesk.zendesk_utility import get_all_custom_objects
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


class CustomObjectRecords(BaseModel):
    """Represents a record in Zendesk."""

    record_id: str
    record_name: str
    created_by_user_id: str
    created_at: str
    creation_date: Optional[str] = None
    description: Optional[str] = None
    expiry_date: Optional[str] = None
    quantity: Optional[int] = None
    after_cursor: Optional[Union[str, bool, None]] = None
    before_cursor: Optional[str] = None
    has_more_val: Optional[bool] = None


class CustomObjectRecordsResponse(BaseModel):
    """Represents the response of all asset records."""

    custom_object_details: List[Dict[str, Any]] = []
    pagination: Optional[Dict[str, Union[str, bool, None]]] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def get_custom_object_records(
    custom_object_key: str,
    query_field: Optional[str] = None,
    after_cursor: Optional[str] = None,
    before_cursor: Optional[str] = None,
    page_size: Optional[int] = 10,
) -> CustomObjectRecordsResponse:
    """
    Gets the custom object records.

    Args:
        custom_object_key: The custom object key which identifies the asset type.
        query_field: The query field of the record in the asset.
        after_cursor: Cursor to move to the next page.
        before_cursor: Cursor to move to the previous page.
        page_size: Number of recoreds to retrieve per page. Defaults to 10.


    Returns:
        All the custom object records from the Zendesk.
    """
    try:
        client = get_zendesk_client()
        query = query_field
        params = {
            "query": query,
            "page[after]": after_cursor,
            "page[before]": before_cursor,
            "page[size]": page_size,
        }

        custom_objects = get_all_custom_objects()
        if custom_object_key not in custom_objects:
            error_message = f"No entries for key: '{custom_object_key}'."
            return CustomObjectRecordsResponse(error_message=error_message)

        params = {key: value for key, value in params.items() if value}
        response = client.get_request(
            entity=f"custom_objects/{custom_object_key}/records/search", params=params
        )
        meta_response = response.get("meta", {})
        records = response.get("custom_object_records", [])
        custom_object_details: List[Dict[str, Any]] = [
            CustomObjectRecords(
                record_id=record.get("id", ""),
                record_name=record.get("name", ""),
                creation_date=record.get("custom_object_fields", {}).get("creation_date", ""),
                description=record.get("custom_object_fields", {}).get("description", ""),
                expiry_date=record.get("custom_object_fields", {}).get("expiry_date", ""),
                quantity=record.get("custom_object_fields", {}).get("quantity", 0),
                created_by_user_id=record.get("created_by_user_id", ""),
                created_at=record.get("created_at", ""),
            ).dict()
            for record in records
        ]
        # Extract page[after], page[before] and page[size] if they exist
        after_cursor = meta_response.get("after_cursor", "")
        before_cursor = meta_response.get("before_cursor", "")
        has_more_val = meta_response.get("has_more", "")

        return CustomObjectRecordsResponse(
            custom_object_details=custom_object_details,
            pagination=(
                {
                    "after_cursor": after_cursor,
                    "before_cursor": before_cursor,
                    "has_more": has_more_val,
                }
                if meta_response
                else None
            ),
        )
    except RequestException as e:
        response = e.response.json() if e.response is not None else {}
        message = response.get("error", "")
        error_message = f"An exception occurred during the API call: {message}"
        logging.error(error_message, exc_info=True)
        return CustomObjectRecordsResponse(error_message=error_message)

    except Exception as e:  # pylint: disable=broad-except
        return CustomObjectRecordsResponse(
            custom_object_details=[],
            pagination={"after_cursor": None, "before_cursor": None, "has_more": False},
            error_message=str(e),
        )
