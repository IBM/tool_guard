from decimal import Decimal
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_compensation_change_reasons import (
    _get_compensation_change_reasons_payload,
    get_compensation_change_reasons,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_compensation_change_reasons() -> None:
    """Test that `get_compensation_change_reasons` produces the expected output."""

    # Define test data:
    test_data = {
        "reference": "Request_Compensation_Change_Incentive_Assign_Bonus",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_compensation_change_reasons.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_compensation_change_references.return_value = Obj(
            {
                "body": {
                    "get_references_response": {
                        "response_data": {
                            "reference_id": [
                                Obj({"reference_id_data": {"id": test_data["reference"]}})
                            ],
                        }
                    },
                },
            }
        )

        # Get compensation change reasons
        response = get_compensation_change_reasons()

        # Ensure that get_compensation_change_reasons() executed and returned proper values
        assert response
        assert len(response.references)
        assert response.references[0].reference == test_data["reference"]

        # Ensure the API call was made with expected parameters
        mock_client.get_compensation_change_references.assert_called_once_with(
            _get_compensation_change_reasons_payload(count=Decimal("999.0"))
        )
