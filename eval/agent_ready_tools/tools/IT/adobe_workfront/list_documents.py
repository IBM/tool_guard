from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.adobe_workfront_client import get_adobe_workfront_client
from agent_ready_tools.utils.tool_credentials import ADOBE_WORKFRONT_CONNECTIONS


@dataclass
class Documents:
    """Represents a document in Adobe Workfront."""

    document_id: str
    document_name: str
    document_description: Optional[str]
    object_code: Optional[str]
    last_update_date: Optional[str]


@dataclass
class ListDocumentsResponse:
    """Represents list of documents in Adobe Workfront."""

    documents: List[Documents]


@tool(expected_credentials=ADOBE_WORKFRONT_CONNECTIONS)
def list_documents(
    document_name: Optional[str] = None,
    project_id: Optional[str] = None,
    limit: Optional[int] = 100,
    skip: Optional[int] = 0,
) -> ListDocumentsResponse:
    """
    Gets a list of Documents from Adobe Workfront.

    Args:
        document_name: The name of the document in Adobe Workfront.
        project_id: The id of the project where the document is located in Adobe Workfront.
        limit: The number of documents returned.
        skip: The number of documents to skip.

    Returns:
        List of documents.
    """

    client = get_adobe_workfront_client()
    params = {"name": document_name, "projectID": project_id, "$$LIMIT": limit, "$$FIRST": skip}
    params = {key: value for key, value in params.items() if value}
    response = client.get_request(entity="docu/search", params=params)

    documents: List[Documents] = [
        Documents(
            document_id=result.get("ID", ""),
            document_name=result.get("name", ""),
            document_description=result.get("description", ""),
            last_update_date=result.get("lastUpdateDate", ""),
            object_code=result.get("objCode", ""),
        )
        for result in response.get("data", [])
    ]
    return ListDocumentsResponse(
        documents=documents,
    )
