from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_absence_types import (
    get_absence_types,
)


def test_get_absence_types_success() -> None:
    """Tests that the `get_absence_types` function returns the expected response."""

    # Define test data
    test_data = {
        "person_id": "300000123456789",
        "absence_type_id": 300000144465190,
        "employer_id": 300000048608288,
        "absence_type_name": "Vacation",
        "description": "Paid vacation time",
        "unit_of_measure": "Days",
    }

    # Patch get_oracle_hcm_client to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_absence_types.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "AbsenceTypeId": test_data["absence_type_id"],
                    "EmployerId": test_data["employer_id"],
                    "AbsenceTypeName": test_data["absence_type_name"],
                    "Description": test_data["description"],
                    "DurationUOMCodeMeaning": test_data["unit_of_measure"],
                }
            ]
        }

        # Get absence types
        response = get_absence_types(person_id=test_data["person_id"])

        # Ensure that get_absence_types() executed and returned proper values
        assert response
        assert response.absence_types[0].absence_type_id == test_data["absence_type_id"]
        assert response.absence_types[0].employer_id == test_data["employer_id"]
        assert response.absence_types[0].absence_type_name == test_data["absence_type_name"]
        assert response.absence_types[0].description == test_data["description"]
        assert response.absence_types[0].unit_of_measure == test_data["unit_of_measure"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "absenceTypesLOV",
            finder_expr=f"findByWord;PersonId={test_data['person_id']}",
        )
