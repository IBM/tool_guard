from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.common.oracle_hcm.get_user_names_id import get_user_names_id


def test_get_user_names_id() -> None:
    """Tests that the `get_user_names_id` tool functions as expected."""

    # Define test data:
    test_data = {
        "email": "john.smith@oraclepdemos.com",
        "names_id": "00020000000EACED00057708000110D9344C61220000004AAC7",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.oracle_hcm.get_user_names_id.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "names": {
                        "items": [
                            {
                                "links": [
                                    {
                                        "href": f'https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/workers/00020000000EACED00057708000110D9344C61220000004AAC/child/names/{test_data["names_id"]}'
                                    }
                                ],
                            }
                        ]
                    },
                }
            ]
        }

        # Get User Names ID.
        response = get_user_names_id(email=test_data["email"])
        # Ensure that get_user_names_id() got executed properly and returned proper values
        assert response
        assert response.names_id == test_data["names_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "workers",
            q_expr=f"emails.EmailAddress='{test_data['email']}'",
            expand_expr="names",
            headers={"REST-Framework-Version": "4"},
        )


def test_get_user_names_id_without_names_links() -> None:
    """Tests that the `get_user_names_id` tool functions as expected without the names link."""

    # Define test data:
    test_data = {
        "email": "john.smith@oraclepdemos.com",
        "names_id": "",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.common.oracle_hcm.get_user_names_id.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "names": {"items": []},
                }
            ]
        }

        # Get User Names ID
        response = get_user_names_id(email=test_data["email"])
        # Ensure that get_user_names_id() got executed properly and returned proper values
        assert response
        assert response.names_id is None

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "workers",
            q_expr=f"emails.EmailAddress='{test_data['email']}'",
            expand_expr="names",
            headers={"REST-Framework-Version": "4"},
        )
