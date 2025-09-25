from io import BytesIO
import json
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
import requests

from agent_ready_tools.clients.box_client import get_box_client
from agent_ready_tools.utils.tool_credentials import BOX_CONNECTIONS


@dataclass
class UploadFile:
    """Represents an uploaded file in box."""

    type_of_file: str
    name: str
    status_code: int


@dataclass
class UploadFileResponse:
    """Represents a response for uploading a file in box."""

    message: str
    uploaded_file: Optional[UploadFile] = None


@tool(expected_credentials=BOX_CONNECTIONS)
def upload_file(file_name: str, parent_folder_id: str, file_bytes: bytes) -> UploadFileResponse:
    """
    Uploads a file in Box.

    Args:
        file_name: The name of the file to be uploaded along with the file extension.
        parent_folder_id: The unique folder id of the parent folder returned by the `get_folder_details_by_name` tool,
            if mentioned as root folder/top level folder items then folder_id has to be 0.
        file_bytes: The byte format of the file to be uploaded.

    Returns:
        The response containing the details of the uploaded file
    """
    try:
        stream_file = BytesIO(file_bytes)
        if "." in file_name and file_name.rsplit(".", 1)[1]:
            stream_file.name = file_name
        else:
            raise ValueError("Filename must include a valid file extension")
        files = {
            "attributes": (
                None,  # Since attribute is a metadata field and not an actual file, we pass
                # (None, value, content_type)
                json.dumps({"name": file_name, "parent": {"id": parent_folder_id}}),
                "application/json",
            ),
            "file": (file_name, stream_file),
        }
        client = get_box_client()

        response = client.post_request(entity="files/content", files=files, api_type="upload")

        # Safely Get the first uploaded file's metadata
        file_info = response.get("entries", [{}])[0]

        if not file_info.get("id"):
            return UploadFileResponse(
                uploaded_file=None, message="No file found in upload response"
            )

        uploaded_file = UploadFile(
            type_of_file=file_info.get("type", ""),
            name=file_info.get("name", ""),
            status_code=response.get("status_code", 201),
        )
        return UploadFileResponse(
            uploaded_file=uploaded_file, message="File uploaded successfully."
        )

    except ValueError as ve:
        return UploadFileResponse(uploaded_file=None, message=f"Validation Error: {str(ve)}")

    except requests.exceptions.RequestException as req_err:
        return UploadFileResponse(uploaded_file=None, message=f"Network error: {req_err}")
