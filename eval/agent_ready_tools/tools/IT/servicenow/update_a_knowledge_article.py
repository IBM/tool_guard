from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class UpdateKnowledgeArticleResponse:
    """Represents the result of updating a knowledge article in ServiceNow."""

    http_code: int


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def update_a_knowledge_article(
    knowledge_article_number_system_id: str,
    short_description: Optional[str] = None,
    knowledge_base: Optional[str] = None,
    article_type: Optional[str] = None,
    description: Optional[str] = None,
    knowledge_category: Optional[str] = None,
    text: Optional[str] = None,
    wiki: Optional[str] = None,
    topic: Optional[str] = None,
    validity_end_date: Optional[str] = None,
    published_date: Optional[str] = None,
    display_attachments_flag: Optional[bool] = None,
    disable_commenting: Optional[bool] = None,
    active: Optional[bool] = None,
) -> UpdateKnowledgeArticleResponse:
    """
    Update a knowledge article in ServiceNow.

    Args:
        knowledge_article_number_system_id: The system_id of the knowledge_article_number returned
            by the `get_knowledge_articles` tool.
        short_description: The short description for updating a knowledge article in ServiceNow.
        knowledge_base: The knowledge_base of the knowledge article, returned by the
            `get_knowledge_bases` tool.
        article_type: The article_type of the knowledge article, returned by the `get_article_types`
            tool. Based on the selected type, the article's content will be adjusted accordingly.
        description: The description for the knowledge article in ServiceNow.
        knowledge_category: The category of the knowledge article, returned by the
            `get_knowledge_categories` tool.
        text: The text content of the article.This is used to update the content when the
            article_type is selected as text.
        wiki: The content of the article.This is used to update the content when the article_type is
            selected as wiki.
        topic: The topic of the knowledge article, returned by the `get_knowledge_topics` tool.
        validity_end_date: The validity end date of the article in ISO 8601 format (e.g., YYYY-MM-
            DD).
        published_date: The published date of the article in ISO 8601 format (e.g., YYYY-MM-DD).
        display_attachments_flag: Indicates if attachments are displayed.
        disable_commenting: Indicates whether commenting is disabled.
        active: Indicates if the article is active.

    Returns:
        Confirmation of the knowledge article update.
    """
    client = get_servicenow_client()

    payload = {
        "short_description": short_description,
        "kb_knowledge_base": knowledge_base,
        "article_type": article_type,
        "kb_category": knowledge_category,
        "text": text,
        "wiki": wiki,
        "description": description,
        "topic": topic,
        "valid_to": validity_end_date,
        "published": published_date,
        "display_attachments": display_attachments_flag,
        "disable_commenting": disable_commenting,
        "active": active,
    }
    payload = {key: value for key, value in payload.items() if value}
    response = client.patch_request(
        entity="kb_knowledge", entity_id=knowledge_article_number_system_id, payload=payload
    )
    return UpdateKnowledgeArticleResponse(http_code=response.get("status_code", ""))
