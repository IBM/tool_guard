from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.update_preferred_name import (
    _update_preferred_name_payload,
    update_preferred_name,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_update_preferred_name() -> None:
    """Test that the `update_preferred_name` function returns the expected response."""

    # Define test data:
    test_data = {
        "user_id": "0e44c92412d34b01aQce61e80a47aaf6d",
        "country_code": "USA",
        "first_name": "Logan",
        "last_name": "McNeill",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.update_preferred_name.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.change_preferred_name.return_value = Obj({"body": {"fault": None}})

        # Update user's preferred name
        response = update_preferred_name(
            user_id=test_data["user_id"],
            country_code=test_data["country_code"],
            first_name=test_data["first_name"],
            last_name=test_data["last_name"],
        )

        # Ensure that update_preferred_name() executed and returned proper values
        assert response
        assert response.success

        # Ensure the API call was made with expected parameters
        mock_client.change_preferred_name.assert_called_once_with(
            _update_preferred_name_payload(
                user_id=test_data["user_id"],
                first_name=test_data["first_name"],
                last_name=test_data["last_name"],
                country_code=test_data["country_code"],
                middle_name=None,
            )
        )
