from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class ArticleTypes:
    """Represents a article type record in ServiceNow."""

    article_type: str


@dataclass
class ArticleTypesResponse:
    """A response containing the article type records."""

    articletypes: list[ArticleTypes]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_article_types() -> ArticleTypesResponse:
    """
    Gets a list of article types records.

    Returns:
        A list of article types records.
    """
    client = get_servicenow_client()
    response = client.get_request(
        entity="sys_choice", params={"name": "kb_knowledge", "element": "article_type"}
    )

    articletypes_list = [
        ArticleTypes(article_type=item.get("value", "")) for item in response.get("result", [])
    ]

    return ArticleTypesResponse(articletypes=articletypes_list)
