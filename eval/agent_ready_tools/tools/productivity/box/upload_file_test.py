from io import BytesIO
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.box.upload_file import upload_file


def test_upload_file() -> None:
    """Tests that a file can be uploaded successfully by the `upload_file` tool."""

    text = (
        "Call me Ishmael. Some years ago-never mind how long precisely-having little or no money in my purse, "
        "and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.\n"
        "It is a way I have of driving off the spleen and regulating the circulation.\n"
        "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; "
        "Whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; "
        "and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from "
        "deliberately stepping into the street, and methodically knocking people's hats off-then , I account it high time to get to see as soon as I can.\n"
    )

    file_stream_bytes = BytesIO(text.encode("utf-8"))
    file_stream = file_stream_bytes.getvalue()

    # Define test data
    test_data = {
        "type_of_file": "file",
        "id": "123456789",
        "file_name": "sample_text_rahul2.txt",
        "parent_folder_id": 123456,
        "status_code": 201,
    }

    # Patch `get_box_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.box.upload_file.get_box_client"
    ) as mock_box_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_box_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "entries": [
                {
                    "type": test_data["type_of_file"],
                    "id": test_data["id"],
                    "name": test_data["file_name"],
                    "status_code": test_data["status_code"],
                }
            ],
            "total_count": 1,
        }

        # Upload a file
        response = upload_file(
            file_name=test_data["file_name"],
            parent_folder_id=test_data["parent_folder_id"],
            file_bytes=file_stream,
        )
        assert response
        assert response.uploaded_file
        assert response.uploaded_file.name == test_data["file_name"]
        assert response.uploaded_file.type_of_file == test_data["type_of_file"]
        assert response.uploaded_file.status_code == test_data["status_code"]

        # Ensure that API call was made with expected response

        mock_client.post_request.assert_called_once()
        _, kwargs = mock_client.post_request.call_args

        assert "file" in kwargs["files"]
        assert kwargs["files"]["file"][0] == test_data["file_name"]
        assert isinstance(kwargs["files"]["file"][1], BytesIO)
