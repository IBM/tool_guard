from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.view_upcoming_time_off import (
    view_upcoming_time_off,
)


def test_view_upcoming_time_off_first_record() -> None:
    """Tests that the `view_upcoming_time_off` tool returns the expected first  record."""

    # Define test data:
    test_data = {
        "person_id": "300000047626100",
        "start_date": "2025-05-01",
        "end_date": "2025-05-01",
        "absence_type": "Vacation",
        "formatted_duration": "9 Hours",
        "employer": "US1 Legal Entity",
        "absence_status": "Completed",
        "approval_status": "APPROVED",
        "limit": 50,
        "offset": 0,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.view_upcoming_time_off.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "employer": test_data["employer"],
                    "absenceType": test_data["absence_type"],
                    "startDate": test_data["start_date"],
                    "endDate": test_data["end_date"],
                    "formattedDuration": test_data["formatted_duration"],
                    "absenceDispStatusMeaning": test_data["absence_status"],
                    "approvalStatusCd": test_data["approval_status"],
                }
            ]
        }

        # Call the view_upcoming_time_off function
        response = view_upcoming_time_off(
            person_id=test_data["person_id"],
            start_date=test_data["start_date"],
            limit=test_data["limit"],
            offset=test_data["offset"],
        )

        # Ensure that the response is not None and contains data
        assert response is not None
        assert len(response.upcoming_absences) > 0

        # Get the first record from the response
        first = response.upcoming_absences[0]

        assert first.employer == test_data["employer"]
        assert first.absence_type == test_data["absence_type"]
        assert first.start_date == test_data["start_date"]
        assert first.end_date == test_data["end_date"]
        assert first.duration == test_data["formatted_duration"]
        assert first.absence_status == test_data["absence_status"]
        assert first.approval_status == test_data["approval_status"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "absences",
            finder_expr=(
                f"findByPersonAbsenceTypeIdAndAbsDate;personId={test_data['person_id']},startDate={test_data['start_date']}"
            ),
            params={"limit": test_data["limit"], "offset": test_data["offset"]},
        )
