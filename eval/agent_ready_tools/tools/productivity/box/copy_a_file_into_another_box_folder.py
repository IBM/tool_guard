import http
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class CopyFile:
    """Represents the result of copying a file into another box folder."""

    file_name: str
    http_code: Optional[int]
    new_file_id: str


@dataclass
class CopyFileResult:
    """Represents the result of copying a file into another box folder."""

    message: str
    file: Optional[CopyFile] = None


@tool(expected_credentials=BOX_CONNECTIONS)
def copy_a_file_into_another_box_folder(file_id: str, target_folder_id: str) -> CopyFileResult:
    """
    Copies a file into another folder in BOX.

    Args:
        file_id: The id of the source file returned by the `get_file_details_by_name` tool.
        target_folder_id: The id of the target folder returned by the `get_folder_details_by_name`
            tool.

    Returns:
        Confirmation of copying the file into another folder.
    """

    client = get_box_client()

    payload = {"parent": {"id": target_folder_id}}
    entity = f"files/{file_id}/copy"
    response = client.post_request(entity=entity, data=payload)

    if (
        "status" in response and response.get("status") == http.HTTPStatus.CONFLICT.value
    ):  # If the file with the given name is already exist, it will return the message.
        message = response.get("message", "")
        return CopyFileResult(message=message)

    file = CopyFile(
        file_name=response.get("name", ""),
        new_file_id=response.get("id", ""),
        http_code=response.get("status_code", None),
    )
    return CopyFileResult(file=file, message="File copied successfully.")
