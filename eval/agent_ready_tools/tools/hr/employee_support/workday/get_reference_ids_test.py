from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.workday.get_reference_ids import (
    _get_references_ids_payload,
    get_reference_ids,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_reference_ids() -> None:
    """Test that `get_reference_ids` tool gets the expected response."""

    # Define test data:
    test_data = {
        "reference_id_type": "Termination_Subcategory_ID",
        "reference_id": "Terminate_Employee_Involuntary_RIF",
    }

    # Patch `get_workday_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.workday.get_reference_ids.get_workday_soap_client"
    ) as mock_workday_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workday_client.return_value = mock_client
        mock_client.get_reference_ids.return_value = Obj(
            {
                "body": {
                    "get_references_response": {
                        "response_data": {
                            "reference_id": [
                                Obj({"reference_id_data": {"id": test_data["reference_id"]}})
                            ]
                        }
                    },
                },
            }
        )

        # Request a get_reference_ids
        response = get_reference_ids(test_data["reference_id_type"])

        # Ensure that get_reference_ids() executed and returned proper values
        assert response
        assert response.reference_ids[0].reference_id == test_data["reference_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_reference_ids.assert_called_once_with(
            _get_references_ids_payload(
                reference_id_type=test_data["reference_id_type"],
            )
        )
