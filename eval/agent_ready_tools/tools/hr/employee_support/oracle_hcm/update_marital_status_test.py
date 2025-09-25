from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_marital_status import (
    update_marital_status,
)


def test_update_marital_status() -> None:
    """Tests that an address can be updated successfully by the `update_marital_status` tool."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D942344DC50000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000195B5FFE00078",
        "legislative_id": "00020000000EACED00057708000110D942344DC80000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000195B5FFE00078",
        "marital_status_id": "M",
        "http_code": "200",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_marital_status.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {"status_code": test_data["http_code"]}

        # Get Update marital status
        response = update_marital_status(
            worker_id=test_data["worker_id"],
            legislative_id=test_data["legislative_id"],
            marital_status_id=test_data["marital_status_id"],
        )

        # Ensure that update_marital_status() is executed and returns proper values
        assert response
        assert response.http_code == int(test_data["http_code"])

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/legislativeInfo/{test_data['legislative_id']}",
            payload={"MaritalStatus": test_data["marital_status_id"]},
        )
