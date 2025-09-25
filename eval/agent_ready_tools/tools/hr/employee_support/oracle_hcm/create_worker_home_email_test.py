from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_worker_home_email import (
    create_worker_home_email,
)


def test_create_worker_home_email() -> None:
    """Test that the worker home email address is successfully created by the
    `create_worker_home_email` tool."""

    # Define test case
    test_data = {
        "worker_id": "00020000000EACED00057708000110D9424FB9950000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B59741903000078707708000001971430500078",
        "email_address": "rahul_sample_test10@example.com",
        "http_code": 201,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.create_worker_home_email.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {"status_code": test_data["http_code"]}

        # Create worker home email address
        response = create_worker_home_email(
            worker_id=test_data["worker_id"],
            email_address=test_data["email_address"],
        )

        # Ensure that create_worker_home_email() executed and returned proper values
        assert response
        assert response.http_code == 201

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity=f"workers/{test_data["worker_id"]}/child/emails",
            payload={
                "EmailAddress": test_data["email_address"],
                "EmailType": "H1",
            },
        )
