from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_programs import Programs, list_programs


def test_list_programs() -> None:
    """Verify that the `list_programs` tool can successfully retrieve Adobe Workfront programs."""

    # Define test data:
    test_data = {
        "program_id": "6596dfb000128b8364d609b75675034e",
        "program_name": "MSSPs / ISVs",
        "description": "new in 2024",
        "is_active": True,
        "portfolio_id": "65e8a7ab0027881c9a200a8f3511ea1a",
        "creation_date": "2025-08-12",
        "user_id": "679cd07f00010fee7b8927d7dfea3321",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_programs.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["program_id"],
                    "name": test_data["program_name"],
                    "description": test_data["description"],
                    "isActive": test_data["is_active"],
                }
            ]
        }

        # List Adobe Workfront programs
        response = list_programs(program_name="MSSPs / ISVs").programs[0]

        # Ensure that list_programs() has executed and returned proper values
        expected_data = Programs(
            program_id=str(test_data["program_id"]),
            program_name=str(test_data["program_name"]),
            description=str(test_data["description"]),
            is_active=bool(test_data["is_active"]),
        )

        assert response
        assert response == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="prgm/search", params={"name": "MSSPs / ISVs", "$$LIMIT": 50, "isActive": True}
        )
