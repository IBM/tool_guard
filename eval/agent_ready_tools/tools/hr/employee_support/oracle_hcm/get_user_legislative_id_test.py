from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_user_legislative_id import (
    get_user_legislative_id,
)


def test_get_user_legislative_id() -> None:
    """Tests that the `get_user_legislative_id` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D942344DC50000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000195B5FFE00078",
        "legislative_id": "00020000000EACED00057708000110D942344DC80000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000195B5FFE00078",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_user_legislative_id.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "links": [
                        {
                            "href": f"example.com/workers/{test_data['worker_id']}/child/legislativeInfo/{test_data['legislative_id']}",
                        }
                    ],
                }
            ]
        }

        # Get legislative id based on worker id
        response = get_user_legislative_id(worker_id=test_data["worker_id"])

        # Ensure that get_user_legislative_id() is executed and returns proper values
        assert response

        assert response.legislative_id == test_data["legislative_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity=f"workers/{test_data["worker_id"]}/child/legislativeInfo"
        )
