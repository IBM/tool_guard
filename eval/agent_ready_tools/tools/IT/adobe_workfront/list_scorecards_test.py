from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.list_scorecards import Scorecard, list_scorecards


def test_list_scorecards_with_pagination() -> None:
    """Verifies that the `list_scorecards` tool can successfully retrieve Adobe Workfront groups."""

    # Define test data
    test_data = {
        "scorecard_id": "682c0e9100029f055125b9d4def4efff",
        "scorecard_name": "Score Card for portfolio",
        "description": "A basic scorecard that captures the identified goals of a portfolio.",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_scorecards.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        # Create mock client
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client

        # Mock the API response
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["scorecard_id"],
                    "name": test_data["scorecard_name"],
                    "description": test_data["description"],
                }
            ]
        }

        # List Adobe Workfront scorecards
        response = list_scorecards(scorecard_name=test_data["scorecard_name"], limit=50, skip=0)

        # Ensure that list_scorecards() has executed and returned proper values
        expected_scorecard = Scorecard(
            scorecard_id=test_data["scorecard_id"],
            scorecard_name=test_data["scorecard_name"],
            description=test_data["description"],
        )

        assert response.scorecards[0] == expected_scorecard

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="score/search",
            params={
                "name": test_data["scorecard_name"],
                "$$LIMIT": 50,
                "$$FIRST": 0,
            },
        )
