from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.jira_client import get_jira_client
from agent_ready_tools.utils.tool_credentials import JIRA_CONNECTIONS


@dataclass
class GetIssuePriorities:
    """Represents a project in Jira."""

    name: str


@dataclass
class GetIssuePrioritiesResponse:
    """Represents the response for retrieving projects in Jira."""

    priorities: List[GetIssuePriorities]


@tool(expected_credentials=JIRA_CONNECTIONS)
def get_issue_priorities() -> GetIssuePrioritiesResponse:
    """
    Retrieves the list of priorities for an issue from Jira.

    Returns:
        Returns the list of issue priorities.
    """
    client = get_jira_client()

    response = client.get_request(entity="priority")
    priorities: List[GetIssuePriorities] = []
    for result in response:
        if isinstance(result, dict):
            priorities.append(
                GetIssuePriorities(
                    name=result.get("name", ""),
                )
            )
    return GetIssuePrioritiesResponse(priorities=priorities)
