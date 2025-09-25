from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.delete_program import delete_program


def test_delete_program() -> None:
    """Tests that a program can be deleted successfully by the `delete_program` tool."""
    # Define test data:
    test_data = {"program_id": "68258dba0000f39eff67f2e40f652ff3", "http_code": 204}

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.delete_program.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Call the function
        response = delete_program(program_id=test_data["program_id"])

        # Ensure that the delete_program() has been executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"prgm/{test_data["program_id"]}")
