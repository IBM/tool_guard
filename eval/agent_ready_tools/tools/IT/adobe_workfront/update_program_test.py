from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.update_program import (
    UpdateProgramResponse,
    update_program,
)


def test_update_program() -> None:
    """Verifies that the `update_program` tool updates the program details in Adobe Workfront."""

    # Define test data:
    test_data = {
        "program_id": "68258e6000010187da59c9ea22e73de0",
        "program_name": "Update a program",
        "description": "Testing",
        "is_active": True,
        "owner_id": "679cd07f00010fee7b8927d7dfea3321",
        "portfolio_id": "682b1775000efd21d7a1bf33d07d45e2",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_program.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.put_request.return_value = {
            "data": {
                "name": test_data["program_name"],
                "description": test_data["description"],
                "isActive": test_data["is_active"],
            }
        }

        # Update a program
        response = update_program(
            program_id=test_data["program_id"],
            program_name=test_data["program_name"],
            description=test_data["description"],
            is_active=test_data["is_active"],
            owner_id=test_data["owner_id"],
            portfolio_id=test_data["portfolio_id"],
        )

        expected_response = UpdateProgramResponse(
            program_name=str(test_data["program_name"]),
            description=str(test_data["description"]),
            is_active=bool(test_data["is_active"]),
        )

        # Ensure that update_program() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        mock_client.put_request.assert_called_once_with(
            entity=f"prgm/{test_data['program_id']}",
            payload={
                "name": test_data["program_name"],
                "description": test_data["description"],
                "isActive": test_data["is_active"],
                "ownerID": test_data["owner_id"],
                "portfolioID": test_data["portfolio_id"],
            },
        )
