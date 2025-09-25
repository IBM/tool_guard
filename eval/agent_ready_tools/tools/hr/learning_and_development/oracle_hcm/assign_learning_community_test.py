from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.assign_learning_community import (
    assign_learning_community,
)


def test_assign_learning_community() -> None:
    """Test that assigning a worker to a learning community was successful by the
    `assign_learning_community` tool."""

    # Define data test
    test_data = {
        "learning_community_id": "00020000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E",
        "person_id": "300000078990691",
        "user_access_type": "MEMBER",
        "http_code": 201,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.assign_learning_community.get_oracle_hcm_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # assign_learning_community
        response = assign_learning_community(
            learning_community_id=test_data["learning_community_id"],
            person_id=test_data["person_id"],
            user_access_type=test_data["user_access_type"],
        )

        # Ensure that assign_learning_community() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"/learningCommunities/{test_data['learning_community_id']}/child/userAccess",
            payload={
                "userAccessPersonId": test_data["person_id"],
                "userAccessType": "ORA_CMNTY_REGULAR_MEMBER",
            },
        )
