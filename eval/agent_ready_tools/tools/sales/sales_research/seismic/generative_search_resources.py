from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.seismic_client import get_seismic_client
from agent_ready_tools.utils.tool_credentials import SEISMIC_CONNECTIONS


@dataclass
class ApplicationUrl:
    """Dataclass representing an application URL associated with the content."""

    name: Optional[str] = None
    url: Optional[str] = None


@dataclass
class Document:
    """Dataclass representing a single document in the generative search sources response."""

    id: Optional[str] = None
    version_id: Optional[str] = None  # mapped from "versionId"
    repository: Optional[str] = None
    name: Optional[str] = None
    teamsite_id: Optional[str] = None  # mapped from "teamsiteId"
    type: Optional[str] = None
    format: Optional[str] = None
    properties: Optional[str] = None
    thumbnail_url: Optional[str] = None  # mapped from "thumbnailUrl"
    page_number: Optional[int] = None  # mapped from "page_number"
    download_url: Optional[str] = None  # mapped from "downloadUrl"
    created_date: Optional[str] = None  # mapped from "createdDate"
    publish_date: Optional[str] = None  # mapped from "publishDate"
    modified_date: Optional[str] = None  # mapped from "modifiedDate"
    major_version: Optional[int] = None  # mapped from "majorVersion"
    minor_version: Optional[int] = None  # mapped from "minorVersion"
    source_text: Optional[str] = None  # mapped from "sourceText"
    status: Optional[str] = None
    score: Optional[float] = None  # changed to float to match API response
    application_urls: Optional[List[ApplicationUrl]] = None  # mapped from "applicationUrls"


@dataclass
class GenerativeSearchSourcesResponse:
    """Dataclass representing the generative search sources response from Seismic."""

    query_time_in_ms: int  # mapped from "queryTimeInMs"
    service_time_in_ms: int  # mapped from "serviceTimeInMs"
    total_count: int  # mapped from "totalCount"
    documents: List[Document]


@tool(expected_credentials=SEISMIC_CONNECTIONS)
def get_generative_search_sources(
    term: str,
    size: int = 10,
) -> GenerativeSearchSourcesResponse:
    """
    Retrieves URLs and titles of Seismic-hosted documents related to a specific content query,
    allowing a sales representative to view the original source materials.

    Args:
        term (str): The search term to query against the Seismic content.
        size (int): The number of results to return. Defaults to 10.

    Returns:
        A response object containing the search results.
    """

    # Check Size isn't greater than 20, and if so, set it to 20
    if size > 20:
        size = 20

    # Retrieve the Seismic client using the helper function.
    client = get_seismic_client()

    # Make the POST request with the Seismic Client using the new format.
    response = client.post_request(
        endpoint="generative",  # The command endpoint.
        category="search",  # The API category.
        payload={"term": term, "size": size},  # The dynamic payload with the search term.
        version="v1",  # API version.
        custom_path_suffix="source",  # Custom path suffix.
    )

    # Ensure that the response is a dict (i.e. the parsed JSON).
    if not isinstance(response, dict):
        raise Exception("Invalid response format received from Seismic client.")

    # Check if the response contains an error.
    if "error" in response:
        raise Exception(f"Request failed with error: {response['error']}")

    # Parse the list of documents from the response, mapping JSON keys to snake_case attributes.
    documents = [
        Document(
            id=doc.get("id"),
            version_id=doc.get("versionId"),
            repository=doc.get("repository"),
            name=doc.get("name"),
            teamsite_id=doc.get("teamsiteId"),
            type=doc.get("type"),
            format=doc.get("format"),
            properties=doc.get("properties") or "",
            thumbnail_url=doc.get("thumbnailUrl"),
            page_number=doc.get("page_number", 0),  # using the correct JSON key
            download_url=doc.get("downloadUrl") or "",
            created_date=doc.get("createdDate") or "",
            publish_date=doc.get("publishDate") or "",
            modified_date=doc.get("modifiedDate"),
            major_version=doc.get("majorVersion", 0),
            minor_version=doc.get("minorVersion", 0),
            source_text=doc.get("sourceText"),
            status=doc.get("status"),
            score=doc.get("score", 0.0),
            application_urls=[
                ApplicationUrl(name=app_url.get("name", ""), url=app_url.get("url", ""))
                for app_url in doc.get("applicationUrls", [])
            ],
        )
        for doc in response.get("documents", [])
    ]

    return GenerativeSearchSourcesResponse(
        query_time_in_ms=response.get("queryTimeInMs", 0),
        service_time_in_ms=response.get("serviceTimeInMs", 0),
        total_count=response.get("totalCount", 0),
        documents=documents,
    )
