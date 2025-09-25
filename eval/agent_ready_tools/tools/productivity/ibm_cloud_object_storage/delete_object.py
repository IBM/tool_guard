from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ibm_cos_client import get_ibm_cos_client
from agent_ready_tools.utils.tool_credentials import IBM_COS_CONNECTIONS


@dataclass
class DeleteObjectResponse:
    """Represents the response for deleting an object from IBM Cloud Object Storage."""

    http_code: int
    error_message: Optional[str] = None


@tool(expected_credentials=IBM_COS_CONNECTIONS)
def delete_object(bucket_name: str, object_key: str) -> DeleteObjectResponse:
    """
    Deletes an object from IBM Cloud Object Storage.

    Args:
        bucket_name: The name of the bucket in IBM Cloud Storage, returned by the `list_buckets` tool.
        object_key: The key of the object to delete in IBM Cloud Storage, returned by the `list_objects` tool.

    Returns:
        The status of the delete operation.
    """
    try:
        client = get_ibm_cos_client()

        response = client.delete_object(bucket_name=bucket_name, object_key=object_key)

        if response.get("status") == "error":
            return DeleteObjectResponse(
                http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
                error_message=response.get("message", "Unknown error occurred."),
            )

        return DeleteObjectResponse(http_code=HTTPStatus.NO_CONTENT.value)

    except Exception as e:  # pylint: disable=broad-except
        return DeleteObjectResponse(
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, error_message=str(e)
        )
