from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.create_a_candidate import (
    create_candidate_oracle,
)


def test_create_candidate_oracle() -> None:
    """Test that a candidate was created successfully by the `create_a_candidate` tool."""

    # Define data
    test_data = {
        "email_address": "oracle_agent@oracle.com",
        "honors": "Highest",
        "known_as": "Agent_Oracle",
        "suffix": "Bot",
        "first_name": "Agent",
        "last_name": "Oracle",
        "middle_name": "Bot",
        "http_code": 201,
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.oracle_hcm.create_a_candidate.get_oracle_hcm_client"
    ) as mock_oracle_client:

        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        response = create_candidate_oracle(
            email_address=test_data["email_address"],
            honors=test_data["honors"],
            known_as=test_data["known_as"],
            suffix=test_data["suffix"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
            middle_name=test_data["middle_name"],
        )

        assert response
        assert response.http_code == test_data["http_code"]

        mock_client.post_request_assert_called_once_with(
            entity="recruitingCandidates",
            payload={
                "LastName": test_data["last_name"],
                "MiddleNames": test_data["middle_name"],
                "FirstName": test_data["first_name"],
                "Suffix": test_data["suffix"],
                "KnownAs": test_data["known_as"],
                "Honors": test_data["honors"],
                "Email": test_data["email_address"],
            },
        )
