from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.seismic_client import get_seismic_client
from agent_ready_tools.tools.sales.sales_research.seismic.generative_search_resources import (
    ApplicationUrl,
    Document,
)
from agent_ready_tools.utils.tool_credentials import SEISMIC_CONNECTIONS


@dataclass
class GenerativeSearchResponse:
    """
    Dataclass representing the generative search response from Seismic.

    This matches the API response structure exactly, which includes:
      - answer: str
      - totalCount: int (mapped to total_count)
      - documents: list of Document objects
    """

    answer: Optional[str] = None
    total_count: Optional[int] = None  # mapped from "totalCount"
    documents: Optional[List[Document]] = None


@tool(expected_credentials=SEISMIC_CONNECTIONS)
def get_generative_search(term: str) -> GenerativeSearchResponse:
    """
    Retrieves either buyer persona insights or sales messaging for a sales representative from
    Seismic based on a given natural language search term.

    Args:
        term: The natural language search term.

    Returns:
        The generative search results for the given term from Seismic. The search results
        could be:
            - Buyer persona insights: a structured table where each persona has its own row and includes
            the following columns: Job Title, Role/Description, Responsibilities, Goals, Challenges, and Values.
            - Sales messaging: high-level sales outline with key value propositions and differentiators.
    """
    # Retrieve the Seismic client using the helper function.
    client = get_seismic_client()

    # Make the POST request using the provided configuration.
    # Note: The endpoint is updated to "generative/query" to match the curl example.
    response = client.post_request(
        endpoint="generative/query",  # matches the curl URL path
        category="search",  # API category remains the same
        payload={"term": term},  # dynamic payload with the search term
        version="v1",  # API version as used in the curl request
        # No custom_path_suffix is used to align with the exact endpoint layout.
    )

    # Ensure that the response is a dict (parsed JSON).
    if not isinstance(response, dict):
        raise Exception("Invalid response format received from Seismic client.")

    # Check if the response contains an error.
    if "error" in response:
        raise Exception(f"Request failed with error: {response['error']}")

    # Parse the list of documents from the response, mapping JSON keys to our snake_case attributes.
    documents = []
    for doc in response.get("documents", []):
        document = Document(
            id=doc.get("id"),
            version_id=doc.get("versionId"),
            repository=doc.get("repository"),
            name=doc.get("name"),
            teamsite_id=doc.get("teamsiteId"),
            type=doc.get("type"),
            format=doc.get("format"),
            properties=doc.get("properties", ""),
            thumbnail_url=doc.get("thumbnailUrl"),
            page_number=doc.get("pageNumber", 0),
            download_url=doc.get("downloadUrl", ""),
            created_date=doc.get("createdDate", ""),
            publish_date=doc.get("publishDate", ""),
            modified_date=doc.get("modifiedDate", ""),
            major_version=doc.get("majorVersion", 0),
            minor_version=doc.get("minorVersion", 0),
            source_text=doc.get("sourceText", ""),
            status=doc.get("status"),
            score=doc.get("score", 0.0),
            application_urls=[
                ApplicationUrl(name=app_url.get("name", ""), url=app_url.get("url", ""))
                for app_url in doc.get("applicationUrls", [])
            ],
        )
        documents.append(document)

    # Construct and return the GenerativeSearchResponse object matching the API structure.
    return GenerativeSearchResponse(
        answer=response.get("answer", ""),
        total_count=response.get("totalCount", 0),
        documents=documents,
    )
