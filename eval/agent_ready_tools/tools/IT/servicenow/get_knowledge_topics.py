from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class KnowledgeTopic:
    """Represents a knowledge topic in ServiceNow."""

    topic: str
    topic_value: str


@dataclass
class KnowledgeTopicResponse:
    """Represents the response from getting a list of knowledge topics."""

    knowledge_topic: list[KnowledgeTopic]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_knowledge_topics() -> KnowledgeTopicResponse:
    """
    Gets a knowledge topic list in ServiceNow.

    Returns:
        The list of knowledge topics.
    """
    client = get_servicenow_client()

    response = client.get_request(
        entity="sys_choice", params={"name": "kb_knowledge", "element": "topic"}
    )

    knowledge_topic = [
        KnowledgeTopic(
            topic=record.get("label"),
            topic_value=record.get("value"),
        )
        for record in response["result"]
    ]
    return KnowledgeTopicResponse(knowledge_topic=knowledge_topic)
