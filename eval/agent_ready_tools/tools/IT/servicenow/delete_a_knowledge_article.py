from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class DeleteKnowledgeArticleResponse:
    """Represents the result of an knowledge article delete operation in Service Now."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def delete_a_knowledge_article(
    knowledge_article_number_system_id: str,
) -> DeleteKnowledgeArticleResponse:
    """
    Deletes the knowledge article in ServiceNow.

    Args:
        knowledge_article_number_system_id: The system_id of the knowledge article number returned
            by the `get_knowledge_articles` tool..

    Returns:
        The result from performing the delete a knowledge article.
    """

    client = get_servicenow_client()

    response = client.delete_request(
        entity="kb_knowledge", entity_id=knowledge_article_number_system_id
    )
    return DeleteKnowledgeArticleResponse(http_code=response)
