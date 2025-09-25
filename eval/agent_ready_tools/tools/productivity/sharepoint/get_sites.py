from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class Site:
    """Represents the details of a site in Microsoft SharePoint."""

    site_name: str
    site_url: str
    site_id: str
    site_description: Optional[str] = None


@dataclass
class SitesResponse:
    """Represents a list of sites in Microsoft SharePoint."""

    sites: List[Site]
    limit: Optional[int] = 0
    skip_token: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def get_sites(
    site_name: str = "*", limit: Optional[int] = 25, skip_token: Optional[str] = None
) -> SitesResponse:
    """
    Retrieves a list of sites in Microsoft SharePoint.

    Args:
        site_name: The site_name is used to filter results in Microsoft SharePoint based upon the
            display name of the site.
        limit: The maximum number of sites retrieved in a single API call. Defaults to 100. Use this
            to control the size of the result set.
        skip_token: The number of sites to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of all the sites in Microsoft SharePoint, along with pagination parameters (limit and
        skip).
    """

    client = get_microsoft_client()

    params = {"$top": limit, "$skiptoken": skip_token, "search": site_name}

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(endpoint="sites", params=params)

    sites: List[Site] = []

    # Extract limit and skip from @odata.nextLink if it exists
    next_api_link = response.get("@odata.nextLink", "")
    output_limit = None
    output_skip_token = None

    if next_api_link:
        query_params = get_query_param_from_links(href=next_api_link)
        output_limit = int(query_params.get("$top", ""))
        output_skip_token = query_params.get("$skiptoken", "")

    for site in response["value"]:
        sites.append(
            Site(
                site_name=site.get("displayName", ""),
                site_url=site.get("webUrl", ""),
                site_id=site.get("id", ""),
                site_description=site.get("description", ""),
            )
        )

    return SitesResponse(sites=sites, limit=output_limit, skip_token=output_skip_token)
