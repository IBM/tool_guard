from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ibm_cos_client import get_ibm_cos_client
from agent_ready_tools.utils.tool_credentials import IBM_COS_CONNECTIONS


@dataclass
class ObjectMetadata:
    """Represents metadata of an object in IBM Cloud Object Storage."""

    object_name: str
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    size: Optional[int] = 0
    content_type: Optional[str] = None
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=IBM_COS_CONNECTIONS)
def list_object_details(bucket_name: str, object_name: str) -> ObjectMetadata:
    """
    Retrieves metadata of a specific object from IBM Cloud Object Storage.

    Args:
        bucket_name: The name of the bucket, as returned by `list_buckets` tool.
        object_name: The key of the object, as returned by `list_objects` tool.

    Returns:
        Object metadata in IBM Cloud Object Storage.
    """
    try:
        client = get_ibm_cos_client()
        response = client.list_object_details(bucket_name, object_name)

        if response.get("status") == "error":
            return ObjectMetadata(
                object_name=object_name,
                http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                error_message=f"Failed to retrieve object metadata: {response.get('message')}",
            )

        return ObjectMetadata(
            object_name=response.get("key", ""),
            last_modified=response.get("last_modified", ""),
            etag=response.get("etag", ""),
            size=response.get("size", 0),
            content_type=response.get("content_type", ""),
            http_code=HTTPStatus.OK.value,
        )

    except Exception as e:  # pylint: disable=broad-except
        return ObjectMetadata(
            object_name=object_name,
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=str(e),
        )
