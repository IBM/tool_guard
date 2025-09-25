from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class KnowledgeCategory:
    """Represents the details of a knowledge categories in ServiceNow."""

    category: str
    system_id: str


@dataclass
class KnowledgeCategoryResponse:
    """Represents the response from getting a list of knowledge categories."""

    categories: list[KnowledgeCategory]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_knowledge_categories(system_id: Optional[str] = None) -> KnowledgeCategoryResponse:
    """
    Retrieves a list of knowledge categories in Servicenow.

    Args:
        system_id: The system_id of the knowledge category.

    Returns:
        A list of all the knowledge categories.
    """
    params = {}
    if system_id:
        params["sys_id"] = system_id

    client = get_servicenow_client()
    response = client.get_request(entity="kb_category", params=params)

    categories_list = [
        KnowledgeCategory(
            category=item.get("label"),
            system_id=item.get("sys_id"),
        )
        for item in response.get("result", [])
    ]

    return KnowledgeCategoryResponse(categories=categories_list)
