from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.get_id_from_links import get_query_param_from_links
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class GetProject:
    """Represents a project in Jira."""

    project_id: str
    project_type: str
    project_name: str
    project_key: str
    project_lead: str


@dataclass
class GetProjectsResponse:
    """Represents the response for retrieving projects in Jira."""

    projects: List[GetProject]
    limit: Optional[int]
    skip: Optional[int]


@tool(expected_credentials=JIRA_CONNECTIONS)
def get_projects(
    project_name: Optional[str] = None,
    expand_expr: Optional[str] = "lead",
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> GetProjectsResponse:
    """
    Gets a list of projects from Jira.

    Args:
        project_name: The field is used to filter out projects by their names.
        expand_expr: The field is used to expand the project details. Defaults to "lead". Use this
            to include additional information about the projects.
        limit: The maximum number of projectss to retrieve in a single API call. Defaults to 50. Use
            this to control the size of the result set.
        skip: The number of projects to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        List of projects.
    """
    client = get_jira_client()

    params: Dict[str, Any] = {}
    if project_name:
        params["query"] = project_name
    if expand_expr:
        params["expand"] = expand_expr
    if limit:
        params["maxResults"] = limit
    if skip is not None:
        params["startAt"] = skip

    response = client.get_request(entity="project/search", params=params)

    projects: List[GetProject] = [
        GetProject(
            project_id=result.get("id", ""),
            project_type=result.get("projectTypeKey", ""),
            project_name=result.get("name", ""),
            project_key=result.get("key", ""),
            project_lead=result.get("lead", {}).get("displayName", ""),
        )
        for result in response.get("values", [])
    ]

    # Extract limit and skip from nextPage if it exists
    output_limit = None
    output_skip = None
    next_api_link = response.get("nextPage", "")
    if next_api_link:
        query_params = get_query_param_from_links(next_api_link)
        output_limit = int(query_params["maxResults"])
        output_skip = int(query_params["startAt"])

    return GetProjectsResponse(
        projects=projects,
        limit=output_limit,
        skip=output_skip,
    )
