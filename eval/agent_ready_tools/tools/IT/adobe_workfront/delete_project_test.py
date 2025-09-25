from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.delete_project import delete_project


def test_delete_project() -> None:
    """Tests that a project can be deleted successfully by the `delete_project` tool."""
    # Define test data:
    test_data = {"project_id": "682b46530014bb951b186e9d58663b9a", "http_code": 200}

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.delete_project.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.delete_request.return_value = test_data["http_code"]

        # Call the function
        response = delete_project(project_id=test_data["project_id"])

        # Ensure that the delete_project() has been executed and returned the expected response
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.delete_request.assert_called_once_with(entity=f"proj/{test_data["project_id"]}")
