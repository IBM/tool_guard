from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.productivity.teams.get_teams import Teams, get_teams


def test_get_all_teams() -> None:
    """Tests that the teams can be retrieved by the `get_teams` tool in Microsoft Teams."""

    # Define test data
    test_data = {
        "team_id": "3e1596e1-9163-4405-86a6-5b12f1ccb46c",
        "team_name": "woehmqigqhyh",
        "team_description": "woehmqigqhyh",
        "output_limit": 50,
        "output_skip_token": "RFNwdAoAAAAAAAAAAAAAFAAAAEaKSx0F_QtLqDEb5_kJbB4CAAAAAAAAAAAAAAAAAAAXMS4yLjg0MC4xMTM1NTYuMS40LjIzMzEGAAAAAAABAu2FWVlNOEaeQSzFC4cyfwHhAAAAAQIAAAA",
    }
    limit = 50
    skip_token = "RFNwdAoAAQAAAAAAAAAAFAAAAEaKSx0F_QtLqDEb5_kJbB4BAAAAAAAAAAAAAAAAAAAXMS4yLjg0MC4xMTM1NTYuMS40LjIzMzEGAAAAAAABAu2FWVlNOEaeQSzFC4cyfwHhAAAAAQIAAAA"

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_teams.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["team_id"],
                    "displayName": test_data["team_name"],
                    "description": test_data["team_description"],
                }
            ],
            "@odata.nextLink": f"https://example.com/nextLink?$select=id,displayName,description&$top={test_data["output_limit"]}&$skiptoken={test_data["output_skip_token"]}",
        }

        # Call the function
        response = get_teams(limit=limit, skip_token=skip_token)
        print(response)

        # Verify that the team details matches the expected data
        expected_teams = Teams(
            team_id=str(test_data["team_id"]),
            team_name=str(test_data["team_name"]),
            team_description=str(test_data["team_description"]),
        )

        assert response.teams[0] == expected_teams
        assert response.limit == test_data["output_limit"]
        assert response.skip_token == test_data["output_skip_token"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="teams",
            params={
                "$top": limit,
                "$select": "id, displayName, description",
                "$skiptoken": skip_token,
            },
        )


# Scenario 2: Filtering through team_name


def test_get_teams() -> None:
    """Tests that the teams can be retrieved with filter parameter(team_name) by the `get_teams`
    tool in Microsoft Teams."""

    # Define test data
    test_data = {
        "team_id": "3e1596e1-9163-4405-86a6-5b12f1ccb46c",
        "team_name": "woehmqigqhyh",
        "team_description": "woehmqigqhyh",
    }
    limit = 50

    # Patch `get_microsoft_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.productivity.teams.get_teams.get_microsoft_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "value": [
                {
                    "id": test_data["team_id"],
                    "displayName": test_data["team_name"],
                    "description": test_data["team_description"],
                }
            ]
        }

        # Call the function
        response = get_teams(team_name="woehmqigqhyh")

        # Verify that the team details matches the expected data
        expected_teams = Teams(
            team_id=str(test_data["team_id"]),
            team_name=str(test_data["team_name"]),
            team_description=str(test_data["team_description"]),
        )

        assert response.teams[0] == expected_teams

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            endpoint="teams",
            params={
                "$top": limit,
                "$filter": f"displayName eq '{test_data["team_name"]}'",
                "$select": "id, displayName, description",
            },
        )
