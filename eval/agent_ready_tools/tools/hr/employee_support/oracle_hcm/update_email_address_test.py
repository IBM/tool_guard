from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_email_address import (
    update_email_address,
)


def test_update_email_address() -> None:
    """Test that the `update_email_address` function returns the expected response."""

    # Define test data:
    test_data = {
        "worker_id": "00020000000EACED00057708000110D9424C4C740000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000196D664000078",
        "email_id": 300000282955174,
        "email_address": "test@oracle.com",
        "email_type": "H1",
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.update_email_address.get_oracle_hcm_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.update_request.return_value = {
            "EmailAddress": test_data["email_address"],
            "EmailType": test_data["email_type"],
        }

        # Update user's email address
        response = update_email_address(
            worker_id=test_data["worker_id"],
            email_id=test_data["email_id"],
            email_address=test_data["email_address"],
            email_type=test_data["email_type"],
        )

        # Ensure that update_email_address() executed and returned proper values
        assert response
        assert response.email_address == test_data["email_address"]

        # Ensure the API call was made with expected parameters
        mock_client.update_request.assert_called_once_with(
            payload={
                "EmailAddress": test_data["email_address"],
                "EmailType": test_data["email_type"],
            },
            entity=f"workers/{test_data['worker_id']}/child/emails/{test_data['email_id']}",
        )
