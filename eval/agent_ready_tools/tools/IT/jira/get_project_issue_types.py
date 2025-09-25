from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class ProjectIssueType:
    """Represents the details of the project issue types in Jira."""

    issuetype_id: str
    issuetype: str


@dataclass
class ProjectIssueTypesResponse:
    """Represents the response from getting project issue types in Jira."""

    project_issue_types: List[ProjectIssueType]


@tool(expected_credentials=JIRA_CONNECTIONS)
def get_project_issue_types(project_id: str) -> ProjectIssueTypesResponse:
    """
    Gets a list of project issue types in Jira.

    Args:
        project_id: The id of the project in Jira returned by the `get_projects` tool.

    Returns:
        A list of project issue types.
    """

    client = get_jira_client()
    entity = f"issue/createmeta/{project_id}/issuetypes"
    response = client.get_request(entity=entity)
    project_issue_types: List[ProjectIssueType] = []
    for item in response.get("issueTypes", []):
        project_issue_types.append(
            ProjectIssueType(issuetype_id=item.get("id", ""), issuetype=item.get("name", ""))
        )

    return ProjectIssueTypesResponse(project_issue_types=project_issue_types)
