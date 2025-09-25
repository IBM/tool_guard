from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.create_program import create_program


def test_create_program() -> None:
    """Verify that the `create_program` tool can successfully retrieve Adobe Workfront program."""

    # Define test data:
    test_data = {
        "portfolio_id": "682aa61c000ef14bbd0d73d48aeae0a6",
        "program_name": "Secure Sales Plays3",
        "object_code": "PORT",
        "program_description": "This is description of program",
        "active_status": True,
        "program_id": "6638dd7a012b4c993cd6bb17b05e7edc",
        "program_manager": "6822c564000b43a0e1939265d1e61873",
        "group": "cd156b2d85444870bcbeaa4689a4aed7",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.create_program.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": {
                "ID": test_data["program_id"],
                "name": test_data["program_name"],
                "objCode": test_data["object_code"],
                "description": test_data["program_description"],
                "isActive": test_data["active_status"],
            }
        }

        # Get adobe_workfront program
        response = create_program(
            portfolio_id=test_data["portfolio_id"],
            program_name=test_data["program_name"],
            program_description=test_data["program_description"],
            object_code=test_data["object_code"],
            active_status=test_data["active_status"],
            program_manager=test_data["program_manager"],
            group=test_data["group"],
        )

        # Ensure that create_program() executed and returned proper values
        assert response

        assert response.program_id == test_data["program_id"]
        assert response.program_name == test_data["program_name"]
        assert response.active_status == test_data["active_status"]
        assert response.object_code == test_data["object_code"]
        assert response.program_description == test_data["program_description"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="prgm",
            payload={
                "name": test_data["program_name"],
                "description": test_data["program_description"],
                "portfolioID": test_data["portfolio_id"],
                "objCode": test_data["object_code"],
                "isActive": test_data["active_status"],
                "ownerID": test_data["program_manager"],
                "groupID": test_data["group"],
            },
        )
