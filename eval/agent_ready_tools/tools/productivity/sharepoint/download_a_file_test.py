from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.sharepoint.download_a_file import download_a_file


def test_download_a_file() -> None:
    """Verifies that the `download_a_file` tool can successfully retrieve the file download url in
    Microsoft SharePoint."""

    # Define test data:
    test_data = {
        "file_name": "Test Data - April 02.txt",
        "file_path": "SKSharePointTest/Test Data - April 02.txt",
        "site_name": "MyTestSite",
        "site_id": "ibmappcon.sharepoint.com,0ca33b1e-0e6c-4732-a347-85f18a01c33c,1f54f7f0-fbb0-46f2-afa4-22ff2f93cbba",
        "http_code": 200,
        "Url": "https://ibmappcon.sharepoint.com/sites/MyTestSite/_layouts/15/download.aspx?UniqueId=d6e931ac-8052-42c3-8a6d-36622f76b9ee&Translate=false&tempauth=v1.eyJzaXRlaWQiOiIwY2EzM2IxZS0wZTZjLTQ3MzItYTM0Ny04NWYxOGEwMWMzM2MiLCJhcHBfZGlzcGxheW5hbWUiOiJHcmFwaCBFeHBsb3JlciIsImFwcGlkIjoiZGU4YmM4YjUtZDlmOS00OGIxLWE4YWQtYjc0OGRhNzI1MDY0IiwiYXVkIjoiMDAwMDAwMDMtMDAwMC0wZmYxLWNlMDAtMDAwMDAwMDAwMDAwL2libWFwcGNvbi5zaGFyZXBvaW50LmNvbUAwMTk1ZWE4Ny0xODM5LTRkZjAtOTczOS1iZjdlZWM2ZGU5MjUiLCJleHAiOiIxNzQ0Mjk4Nzk3In0.CgoKBHNuaWQSAjY5EgsIts-0w7eR_D0QBRoMNDAuMTI2LjIzLjk3KixiWm9KRjY5N0xEWkIyU3VXOFpRcW0wdmJiVy9HVFlyWHAvU1E4Z0JpN0VNPTCJATgBQhChkyRVGKAAwFBp16lJvzP2ShBoYXNoZWRwcm9vZnRva2VuUghbImttc2kiXXIpMGguZnxtZW1iZXJzaGlwfDEwMDMzZmZmYTZhNTZlYzlAbGl2ZS5jb216ATKCARIJh-qVATkY8E0Rlzm_fuxt6SWSAQZjc3Rlc3SaAQZjc3Rlc3SiASBjc3Rlc3RAaWJtYXBwY29uLm9ubWljcm9zb2Z0LmNvbaoBEDEwMDMzRkZGQTZBNTZFQzmyAWhhbGxmaWxlcy53cml0ZSBncm91cC5yZWFkIGdyb3VwLndyaXRlIGFsbHNpdGVzLndyaXRlIGFsbHByb2ZpbGVzLnJlYWQgYWxscHJvZmlsZXMucmVhZCBhbGxwcm9maWxlcy53cml0ZcgBAQ.Bu9RDlPMyniouK0DuFLseN1dibZvNQ6zIuXuD4XSnYM&ApiVersion=2.1",
    }

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.sharepoint.download_a_file.get_microsoft_client"
    ) as mock_microsoft_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_microsoft_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "status_code": test_data["http_code"],
            "@microsoft.graph.downloadUrl": test_data["Url"],
        }

        # Call the function
        response = download_a_file(
            site_id=test_data["site_id"],
            file_path=test_data["file_path"],
        )

        # Ensures that download_a_file() executed and returned proper values
        assert response.url is not None
        assert response.http_code == test_data["http_code"]

        # Ensures the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint=f"sites/{test_data['site_id']}/drive/root:/{test_data['file_path']}"
        )
