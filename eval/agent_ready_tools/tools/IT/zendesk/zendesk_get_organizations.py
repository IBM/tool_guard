from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.zendesk_client import get_zendesk_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import ZENDESK_CONNECTIONS


@dataclass
class Organization:
    """Represents an organization in Zendesk."""

    organization_id: str
    name: str
    created_at: str
    group_id: Optional[str] = None
    domain_names: Optional[List[str]] = None
    notes: Optional[str] = None
    details: Optional[str] = None
    tags: Optional[List[str]] = None
    custom_fields: Optional[Dict[str, Any]] = None


@dataclass
class GetOrganizationsResponse:
    """Represents the response for retrieving organizations in Zendesk."""

    organizations: List[Organization]
    page: Optional[int]
    per_page: Optional[int]
    http_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=ZENDESK_CONNECTIONS)
def zendesk_get_organizations(
    search: Optional[str] = None, per_page: Optional[int] = 10, page: Optional[int] = 1
) -> GetOrganizationsResponse:
    """
    Gets organizations from Zendesk.

    Args:
        search: Optional search query. Users can search for an organization using a keyword (e.g., WO) or the complete organization name (e.g., WO Organization).
        per_page: Number of organizations to retrieve per page. Defaults to 10.
        page: Page number to retrieve. Defaults to 1.

    Returns:
        List of organizations.
    """
    try:
        client = get_zendesk_client()

        query = "type:organization " + search if search else "type:organization"
        params = {
            "query": query,
            "per_page": per_page,
            "page": page,
        }

        params = {key: value for key, value in params.items() if value is not None}

        response = client.get_request(entity="search", params=params)

        organizations: List[Organization] = [
            Organization(
                organization_id=str(org.get("id", "")),
                name=org.get("name", ""),
                created_at=org.get("created_at", ""),
                group_id=str(org.get("group_id", "")),
                domain_names=org.get("domain_names", []),
                notes=org.get("notes", ""),
                details=org.get("details", ""),
                tags=org.get("tags", []),
                custom_fields=org.get("organization_fields", {}),
            )
            for org in response.get("results", [])
        ]

        output_page = None
        output_per_page = None
        next_api_link = response.get("next_page")
        if next_api_link is not None:
            query_params = get_query_param_from_links(next_api_link)
            output_page = int(query_params["page"]) if "page" in query_params else None
            output_per_page = int(query_params["per_page"]) if "per_page" in query_params else None

        return GetOrganizationsResponse(
            organizations=organizations, page=output_page, per_page=output_per_page
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        error_message = (
            error_response.get("error", {}).get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return GetOrganizationsResponse(
            organizations=[],
            page=None,
            per_page=None,
            http_code=e.response.status_code,
            error_message=error_message,
        )
    except Exception as e:  # pylint: disable=broad-except
        return GetOrganizationsResponse(
            organizations=[],
            page=None,
            per_page=None,
            http_code=500,
            error_message=str(e),
        )
