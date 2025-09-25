from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_my_learning_journeys import (
    view_my_learning_journeys,
)


def test_view_my_learning_journeys() -> None:
    """Test that the `view_my_learning_journeys` function returns the expected response."""

    # Patch `view_my_learning_journeys` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_my_learning_journeys.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "result": {
                "summary": [{"offset": "0", "limit": "25", "count": "1", "hasMore": "false"}],
                "items": [
                    {
                        "JourneyId": "300000281745020",
                        "Description": "null",
                        "CreatedBy": "Yugandhar.Sonawane1@partner.ibm.com",
                        "FavouriteFlag": "N",
                        "Level": "ORA_PERSONAL",
                        "CategoryMeaning": "Learn",
                        "BackgroundThumbnailURL": "null",
                        "LevelMeaning": "Personal",
                        "Name": "Learning Journey Test",
                    }
                ],
            }
        }

        # Get email types
        response = view_my_learning_journeys()

        # Ensure that view_my_learning_journeys() executed and returned proper values
        assert response

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="journeys/action/findByAdvancedSearchQuery",
            headers={"Content-Type": "application/vnd.oracle.adf.action+json"},
            payload={
                "limit": 20,
                "offset": 0,
                "filters": [
                    {"name": ["Mode"], "value": ["ORA_PERSONAL"]},
                    {"name": ["Category"], "value": ["ORA_LEARN"]},
                ],
                "displayFields": [
                    "JourneyId",
                    "CategoryMeaning",
                    "Name",
                    "Description",
                    "BackgroundThumbnailURL",
                    "Level",
                    "FavouriteFlag",
                    "LevelMeaning",
                    "CreatedBy",
                ],
            },
        )
