from http import HTTPStatus
from typing import Optional

from ibm_botocore.exceptions import ClientError
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.ibm_cos_client import get_ibm_cos_client
from agent_ready_tools.utils.tool_credentials import IBM_COS_CONNECTIONS


@dataclass
class DeleteBucketResponse:
    """Represents the response for deleting a bucket."""

    http_code: Optional[int] = None
    client_response: Optional[dict] = None
    error_message: Optional[str] = None


@tool(expected_credentials=IBM_COS_CONNECTIONS)
def delete_bucket(bucket_name: str) -> DeleteBucketResponse:
    """
    Deletes a bucket from IBM Cloud Object Storage.

    Args:
        bucket_name: The name of the bucket in IBM Cloud Object Storage, returned by the `list_buckets` tool.

    Returns:
        The status of the delete operation.
    """
    try:
        client = get_ibm_cos_client()

        # Directly use the cos_resource to delete the bucket
        client.cos_resource.Bucket(bucket_name).delete()

        return DeleteBucketResponse(
            client_response={
                "status": "success",
                "message": f"Bucket '{bucket_name}' deleted successfully.",
            },
            http_code=HTTPStatus.OK.value,
        )

    except ClientError as e:
        return DeleteBucketResponse(
            client_response={"status": "error"},
            http_code=HTTPStatus.BAD_REQUEST.value,
            error_message=e.response["Error"]["Message"],
        )

    except Exception as e:  # pylint: disable=broad-except
        return DeleteBucketResponse(
            client_response={"status": "error"},
            http_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            error_message=str(e),
        )
