from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_display_name_oracle import (
    update_display_name_oracle,
)


def test_update_display_name_oracle() -> None:
    """Test that the `update_display_name_oracle` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D93445B0480000004AAC",
        "names_id": "00020000000EACED00057708000110D932469A130000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000196E5D7140078",
        "first_name": "John",
        "last_name": "Wick",
        "display_name": "John Wick",
        "url": "https://test.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_display_name_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "FirstName": test_data["first_name"],
            "LastName": test_data["last_name"],
            "DisplayName": test_data["display_name"],
        }

        # Update display name
        response = update_display_name_oracle(
            worker_id=test_data["worker_id"],
            names_id=test_data["names_id"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
        )

        # Ensure that update_display_name_oracle() executed and returned proper values
        assert response
        assert response.first_name == test_data["first_name"]
        assert response.last_name == test_data["last_name"]
        assert response.display_name == test_data["display_name"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            entity=f"workers/{test_data['worker_id']}/child/names/{test_data['names_id']}",
            payload={
                "FirstName": test_data["first_name"],
                "LastName": test_data["last_name"],
            },
        )
