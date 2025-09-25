from io import BytesIO
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
import requests

from agent_ready_tools.clients.microsoft_client import get_microsoft_client
from agent_ready_tools.utils.tool_credentials import MICROSOFT_CONNECTIONS


@dataclass
class UploadedFile:
    """Represents the details of uploaded file in Microsoft SharePoint."""

    id: str
    name: str
    status_code: Optional[int] = None


@dataclass
class UploadFileResponse:
    """Represents the message and details of uploaded file in Microsoft SharePoint."""

    message: str
    uploaded_file: Optional[UploadedFile] = None
    error_code: Optional[int] = None
    error_message: Optional[str] = None


@tool(expected_credentials=MICROSOFT_CONNECTIONS)
def upload_file_to_sharepoint(
    file_name: str, site_id: str, file_bytes: bytes, folder_id: str = "root"
) -> UploadFileResponse:
    """
    Uploads a file in Microsoft SharePoint.

    Args:
        file_name: The name of the file to be uploaded along with the file extension.
        site_id: The site_id uniquely identifying them within the MS Graph API, returned by
            `get_sites` tool.
        file_bytes: The byte format of the file to be uploaded.
        folder_id: The item_id of the folder returned by the `sharepoint_get_folders`
            tool in which the file will be uploaded. Default is "root" (root folder).

    Returns:
        The response containing the details of the uploaded file
    """
    try:
        if "." not in file_name or not file_name.rsplit(".", 1)[1]:
            raise ValueError("Filename must include a valid file extension")

        stream_file = BytesIO(file_bytes)
        stream_file.name = file_name
        stream_file.seek(0)

        endpoint = f"sites/{site_id}/drive/items/{folder_id}:/{file_name}:/content"
        client = get_microsoft_client()

        rsp = client.put_request(endpoint=endpoint, data=stream_file.read())

        return UploadFileResponse(
            message="File uploaded successfully.",
            uploaded_file=UploadedFile(
                id=rsp.get("id", ""),
                name=rsp.get("name", ""),
                status_code=rsp.get("status_code", None),
            ),
            error_code=None,
            error_message=None,
        )

    except ValueError as ve:
        return UploadFileResponse(
            message="File upload failed.", uploaded_file=None, error_code=400, error_message=str(ve)
        )

    except requests.exceptions.RequestException as req_err:
        status_code = getattr(req_err.response, "status_code", None)
        return UploadFileResponse(
            message="File upload failed.",
            uploaded_file=None,
            error_code=status_code,
            error_message=str(req_err),
        )
