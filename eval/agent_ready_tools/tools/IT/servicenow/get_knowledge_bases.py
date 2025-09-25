from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class KnowledgeBase:
    """Represents the details of knowledge bases in ServiceNow."""

    knowledge_base: str
    system_id: str


@dataclass
class KnowledgeBaseResponse:
    """Represents the response from getting a list of knowledge bases."""

    knowledge_bases: list[KnowledgeBase]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_knowledge_bases(system_id: Optional[str] = None) -> KnowledgeBaseResponse:
    """
    Gets the list of knowledge bases in ServiceNow.

    Args:
        system_id: The system_id of the knowledge bases.

    Returns:
        The list of knowledge bases.
    """
    params = {}
    if system_id:
        params["sys_id"] = system_id

    client = get_servicenow_client()
    response = client.get_request(entity="kb_knowledge_base", params=params)

    knowledge_bases_list = [
        KnowledgeBase(
            knowledge_base=item.get("title"),
            system_id=item.get("sys_id"),
        )
        for item in response.get("result", [])
    ]

    return KnowledgeBaseResponse(knowledge_bases=knowledge_bases_list)
