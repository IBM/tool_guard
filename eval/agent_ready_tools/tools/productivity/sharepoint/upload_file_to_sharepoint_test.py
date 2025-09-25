from io import BytesIO
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.upload_file_to_sharepoint import (
    upload_file_to_sharepoint,
)


def test_upload_file_to_sharepoint() -> None:
    """Tests that a file can be uploaded successfully by the `upload_file_to_sharepoint` tool."""

    text = (
        "What is a SharePoint?\n"
        "SharePoint in Microsoft 365 is a cloud-based service, hosted by Microsoft, for businesses of all sizes. "
        "Instead of installing and deploying the SharePoint Server on-premises, any business can subscribe to a Microsoft 365 plan "
        "or to the standalone SharePoint Online service. Your employees can create sites to share documents and information with "
        "colleagues, partners, and customers."
    )

    file_stream_bytes = BytesIO(text.encode("utf-8"))
    file_stream = file_stream_bytes.getvalue()

    # Define test data
    test_data = {
        "id": "de8bc8b5-d9f9-48b1-a8ad-b748da725064",
        "name": "test_123.txt",
        "site_id": "wxodomains.sharepoint.com,b8613266-b0a3-40d0-98ce-3b27481881b9,ec0156ed-2431-46c2-8a51-9a590ff910f6",
        "folder_id": "01JHX3AJXZGUQKG5DLTJE3S4TC57HAKNAB",
        "status_code": 201,
    }

    # Patch the `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.upload_file_to_sharepoint.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "id": test_data["id"],
            "name": test_data["name"],
            "status_code": test_data["status_code"],
        }

        # Call the function
        response = upload_file_to_sharepoint(
            site_id=test_data["site_id"],
            folder_id=test_data["folder_id"],
            file_name=test_data["name"],
            file_bytes=file_stream,
        )

        assert response
        assert response.uploaded_file
        assert response.uploaded_file.id == test_data["id"]
        assert response.uploaded_file.name == test_data["name"]
        assert response.uploaded_file.status_code == test_data["status_code"]
        assert response.message == "File uploaded successfully."

        # Ensure the API call was made with appropriate parameters
        mock_client.put_request.assert_called_once()
        _, kwargs = mock_client.put_request.call_args

        assert f"drive/items/{test_data['folder_id']}:/" in kwargs["endpoint"]
        assert test_data["name"] in kwargs["endpoint"]
        assert kwargs["data"] == file_stream
