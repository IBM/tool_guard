from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_absence_reasons import (
    get_absence_reasons,
)


def test_get_absence_reasons() -> None:
    """Tests that the `get_absence_reasons` function returns the expected response."""

    # Define test data
    test_data = {
        "absence_type_id": "300000188023220",
        "reason": "Landurend Zorgverlof",
    }

    # Patch get_oracle_hcm_client to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_absence_reasons.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {"items": [{"Name": test_data["reason"]}]}

        # Get absence reasons
        response = get_absence_reasons(absence_type_id=test_data["absence_type_id"])

        # Ensure that get_absence_reasons() executed and returned proper values
        assert response is not None
        assert response.absence_reasons[0].reason == test_data["reason"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "absenceTypeReasonsLOV",
            q_expr=f"AbsenceTypeId={test_data['absence_type_id']}",
        )
