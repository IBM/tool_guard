from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_recommendations_made import (
    RecommendationDetailsResponse,
    view_recommendations_made,
)


def test_view_recommendations_made() -> None:
    """Tests that `view_recommendations_made` function returns the expected response."""

    # Define test data:
    test_data = {
        "person_id": 300000047888610,
        # Since there are duplicates in the learning recommendations, and since we cannot return list in a mock client
        # we are individually assigning the unique learning recommendations to separate keys
        "learning_item_title": "Emotional Intelligence & Resilience",
        "learning_item_title2": "Customer Service Superstars",
        "learning_item_title3": "Workplace Safety",
        "learning_item_title4": "Leadership Level 2",
        "learning_item_title5": "Understanding Prostate Cancer",
        "learning_item_title6": "Sleep Disorders: an Introduction",
        "learning_item_title7": "Valuing Diversity",
        "limit": 50,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_recommendations_made.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {"learningItemTitle": test_data["learning_item_title"]},
                {"learningItemTitle": test_data["learning_item_title2"]},
                {"learningItemTitle": test_data["learning_item_title3"]},
                {"learningItemTitle": test_data["learning_item_title4"]},
                {"learningItemTitle": test_data["learning_item_title5"]},
                {"learningItemTitle": test_data["learning_item_title6"]},
                {"learningItemTitle": test_data["learning_item_title7"]},
            ]
        }

        # Get user recommended learnings
        response = view_recommendations_made(
            person_id=test_data["person_id"], limit=test_data["limit"]
        )

        expected_response = RecommendationDetailsResponse(
            recommendations=[
                "Emotional Intelligence & Resilience",
                "Customer Service Superstars",
                "Workplace Safety",
                "Leadership Level 2",
                "Understanding Prostate Cancer",
                "Sleep Disorders: an Introduction",
                "Valuing Diversity",
            ]
        )

        # Ensure that view_recommendations_made() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure that API call was made with expected parameters
        q_expr = f"assignerId={test_data["person_id"]}"
        params = {"limit": test_data["limit"]}
        mock_client.get_request.assert_called_once_with(
            "learningRecommendations",
            q_expr=q_expr,
            params=params,
            headers={"REST-Framework-Version": "4"},
        )
