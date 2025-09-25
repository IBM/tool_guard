from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class CreateKnowledgeArticleResponse:
    """Represents the result of creating a knowledge article in ServiceNow."""

    system_id: str
    short_description: str
    knowledge_article_number: int
    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def create_a_knowledge_article(
    short_description: str,
    knowledge_base: str,
    article_type: Optional[str] = None,
    text: Optional[str] = None,
    wiki: Optional[str] = None,
    description: Optional[str] = None,
    knowledge_category: Optional[str] = None,
    workflow_state: Optional[str] = None,
    topic: Optional[str] = None,
) -> CreateKnowledgeArticleResponse:
    """
    Creates a knowledge article in ServiceNow.

    Args:
        short_description: The short description for creating a knowledge article.
        knowledge_base: The knowledge_base of the knowledge article returned by the
            `get_knowledge_bases` tool.
        article_type: The article_type of the knowledge article, returned by the `get_article_types`
            tool.
        text: The input text data for the knowledge article.
        wiki: The content of the article.This is used to update the content when the article_type is
            selected as wiki.
        description: The description for the knowledge article.
        knowledge_category: The category of the knowledge article, returned by the
            `get_knowledge_categories` tool.
        workflow_state: The work_flow_state of the knowledge article returned by the
            `get_workflow_states` tool.
        topic: The topic of the knowledge article returned by the `get_knowledge_topics` tool.

    Returns:
        The result from performing the creation of a knowledge article.
    """
    client = get_servicenow_client()

    payload = {
        "short_description": short_description,
        "kb_knowledge_base": knowledge_base,
        "article_type": article_type,
        "text": text,
        "wiki": wiki,
        "description": description,
        "kb_category": knowledge_category,
        "workflow_state": workflow_state,
        "topic": topic,
    }
    payload = {key: value for key, value in payload.items() if value}

    response = client.post_request(entity="kb_knowledge", payload=payload)
    result = response.get("result", {})
    return CreateKnowledgeArticleResponse(
        system_id=result.get("sys_id", ""),
        knowledge_article_number=result.get("number", ""),
        short_description=result.get("short_description", ""),
        http_code=response.get("status_code", ""),
    )
