import json

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class FileContentResult:
    """Represents the result of retrieving file content in Box."""

    content: str
    is_encoded: bool


@tool(expected_credentials=BOX_CONNECTIONS)
def get_file_content(file_name: str, file_id: str) -> FileContentResult:
    """
    Gets the content present in a file from Box.

    Args:
        file_name: The name of the file returned by the get_file_details_by_name tool.
        file_id: The id of the file returned by the get_file_details_by_name tool.

    Returns:
        file's content in text
    """

    client = get_box_client()

    entity = f"files/{file_id}/content"
    # Setting content to True by default to retrieve the file content as text.
    response = client.get_request(entity=entity, content=True)
    encoded_text = response.get("content", "")

    if file_name.endswith(".txt"):
        # Re-encode and decode to handle encoding issues
        text = encoded_text.encode("latin1").decode("utf-8")
        # Converting dictionary to JSON string to standardize the response across all file types.
        text_content = json.dumps({"text": text})
        return FileContentResult(content=text_content, is_encoded=False)
    elif file_name.endswith(".docx"):
        return FileContentResult(content=encoded_text, is_encoded=True)
    else:
        return FileContentResult(content=encoded_text, is_encoded=False)
