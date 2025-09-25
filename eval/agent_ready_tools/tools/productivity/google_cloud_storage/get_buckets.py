from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.google_client import get_google_client
from agent_ready_tools.tools.productivity.google_cloud_storage.constants import SERVICE, VERSION
from agent_ready_tools.utils.tool_credentials import GOOGLE_CONNECTIONS


@dataclass
class GoogleCloudStorageBucket:
    """Represents a bucket in Google Cloud Storage."""

    bucket_id: str
    bucket_name: str
    location: str
    creation_date: str


@dataclass
class GoogleCloudStorageBucketsResponse:
    """Represents a list of buckets in Google Cloud Storage."""

    buckets: list[GoogleCloudStorageBucket]
    next_page_token: Optional[str]


@tool(expected_credentials=GOOGLE_CONNECTIONS)
def get_buckets(
    project_id: str,
    bucket_name_prefix: Optional[str] = None,
    limit: Optional[int] = 50,
    next_page_token: Optional[str] = None,
) -> GoogleCloudStorageBucketsResponse:
    """
    Retrieves a list of buckets in Google Cloud Storage.

    Args:
        project_id: The ID of the Google Cloud Storage project.
        bucket_name_prefix: Filters buckets whose names start with the specified string.
        limit: The maximum number of buckets retrieved in a single API call. Defaults to 50. Use
            this to control the result size.
        next_page_token: Token for retrieving the results for pagination.

    Returns:
        List of buckets in Google Cloud Storage.
    """

    client = get_google_client()

    params = {
        "project": project_id,
        "prefix": bucket_name_prefix,
        "maxResults": limit,
        "pageToken": next_page_token,
    }
    # Filter out the parameters which are blank/None
    params = {key: value for key, value in params.items() if value}

    response = client.get_request(service=SERVICE, version=VERSION, entity="b", params=params)

    buckets_list: list[GoogleCloudStorageBucket] = []

    for bucket in response.get("items", []):
        buckets_list.append(
            GoogleCloudStorageBucket(
                bucket_id=bucket.get("id", ""),
                bucket_name=bucket.get("name", ""),
                location=bucket.get("location", ""),
                creation_date=bucket.get("timeCreated", ""),
            )
        )

    next_token = response.get("nextPageToken") if response.get("nextPageToken") else None

    return GoogleCloudStorageBucketsResponse(
        buckets=buckets_list,
        next_page_token=next_token,
    )
