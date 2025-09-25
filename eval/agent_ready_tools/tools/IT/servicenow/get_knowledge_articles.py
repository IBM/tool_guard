from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class KnowledgeArticle:
    """Represents a single record of knowledge article in ServiceNow."""

    knowledge_article_number: str
    system_id: str
    text: str
    article_type: str
    active: str
    topic: str
    short_description: Optional[str] = None
    updated_on_date: Optional[str] = None
    valid_to_date: Optional[str] = None
    workflow_state: Optional[str] = None
    wiki: Optional[str] = None
    display_attachments: Optional[str] = None
    published_date: Optional[str] = None
    knowledge_base: Optional[str] = None
    knowledge_category: Optional[str] = None


@dataclass
class KnowledgeArticlesResponse:
    """Represents the response of the list of knowledge articles in ServiceNow."""

    knowledge_articles: list[KnowledgeArticle]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_knowledge_articles(
    search: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> KnowledgeArticlesResponse:
    """
    Retrieve the list of knowledge articles from ServiceNow.

    Args:
        search: Custom query in sysparm_query format for advanced filtering (e.g.,
            "number=KB0010093^active=true").
        limit: The maximum number knowledge article to retrieve in a single API call. Defaults to
            10. Use this to control the size of the result set.
        skip: The number of knowledge article to skip for pagination.

    Returns:
        A list of knowledge articles.
    """
    client = get_servicenow_client()

    params = {
        "sysparm_query": search,
        "sysparm_display_value": True,
        "sysparm_limit": limit,
        "sysparm_offset": skip,
    }

    params = {key: value for key, value in params.items() if value is not None}

    response = client.get_request(entity="kb_knowledge", params=params)

    knowledge_articles = [
        KnowledgeArticle(
            short_description=item.get("short_description", ""),
            updated_on_date=item.get("sys_updated_on", ""),
            knowledge_article_number=item.get("number", ""),
            system_id=item.get("sys_id", ""),
            valid_to_date=item.get("valid_to", ""),
            workflow_state=item.get("workflow_state", ""),
            text=item.get("text", ""),
            wiki=item.get("wiki", ""),
            display_attachments=item.get("display_attachments", ""),
            article_type=item.get("article_type", ""),
            active=item.get("active", ""),
            published_date=item.get("published", ""),
            knowledge_base=(
                item.get("kb_knowledge_base", {}).get("display_value", "")
                if isinstance(item.get("kb_knowledge_base"), dict)
                else item.get("kb_knowledge_base", "")
            ),
            topic=item.get("topic", ""),
            knowledge_category=(
                item.get("kb_category", {}).get("display_value", "")
                if isinstance(item.get("kb_category"), dict)
                else item.get("kb_category", "")
            ),
        )
        for item in response.get("result", [])
    ]

    return KnowledgeArticlesResponse(knowledge_articles)
