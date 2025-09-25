from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_learnings_communities import (
    LearningCommunityDetails,
    view_learnings_communities,
)


def test_view_learnings_communities() -> None:
    """Tests that the `view_learnings_communities` function returns the expected response."""

    # Define test data:
    test_data = {
        "learningItemId": 300000130268174,
        "learningItemTitle": "HR Leadership Development Community",
        "learningItemStatus": "ORA_ACTIVE",
        "offset": 0,
        "limit": 50,
        "learningCommunityId": "ACED0005737200136A6176612E7574696C2E41727261794C6973747881D21D99C7619D03000149000473697A65787000000003770400000003737200116A6176612E6C616E672E496E746567657212E2A0A4F781873802000149000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B020000787000000AA07371007E0002000000087371007E00020000000378",
        "personId": "300000281382261",
    }

    # Get `view_learnings_communities` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.view_learnings_communities.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "learningItemId": test_data["learningItemId"],
                    "learningItemTitle": test_data["learningItemTitle"],
                    "learningItemStatus": test_data["learningItemStatus"],
                    "links": [
                        {
                            "rel": "self",
                            "href": f"https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/learningCommunities/{test_data["learningCommunityId"]}",
                            "name": "learningCommunities",
                            "kind": "item",
                            "properties": {
                                "changeIndicator": "ACED0005737200136A6176612E7574696C2E41727261794C6973747881D21D99C7619D03000149000473697A65787000000003770400000003737200116A6176612E6C616E672E496E746567657212E2A0A4F781873802000149000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B020000787000000AA07371007E0002000000087371007E00020000000378"
                            },
                        }
                    ],
                }
            ],
        }

        # Get users assigned learnings communities
        response = view_learnings_communities(
            person_id=test_data.get("personId", ""),
            offset=test_data["offset"],
            limit=test_data["limit"],
        ).communities[:1]

        expected_response = [
            LearningCommunityDetails(
                learning_item_id=300000130268174,
                learning_item_status=str(test_data.get("learningItemStatus", "")),
                learning_item_title=str(test_data.get("learningItemTitle", "")),
                learning_community_id=str(test_data.get("learningCommunityId", "")),
            ),
        ]
        # Ensure that view_learnings() executed and returned proper values
        assert response
        assert response == expected_response

        # Ensure the API call was made with expected parameters
        params = {"limit": test_data["limit"], "offset": test_data["offset"]}
        mock_client.get_request.assert_called_once_with(
            "learningCommunities",
            q_expr=f"userAccess.userAccessPersonId={test_data["personId"]}",
            params=params,
            headers={"REST-Framework-Version": "4"},
        )
