from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.request_time_off_oracle import (
    request_time_off_oracle,
)


def test_request_time_off_oracle_success() -> None:
    """Tests that the `request_time_off_oracle` function returns the expected response."""

    # Define test data
    test_data = {
        "person_id": "300000050798130",
        "absence_type_name": "Vacation",
        "start_date": "2025-05-29",
        "end_date": "2025-05-29",
        "start_time": "11:00",
        "end_time": "17:00",
        "employer_id": 300000046974965,
        "absence_type_id": 300000144465190,
        "status": "AWAITING",
        "employer": "US1 Legal Entity",
        "formatted_duration": "6 Hours",
        "absence_request_id": 300000283182505,
        "absenceStatusCd": "SUBMITTED",
    }

    # Patch get_oracle_hcm_client to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.request_time_off_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "personAbsenceEntryId": test_data["absence_request_id"],
            "approvalStatusCd": test_data["status"],
            "absenceType": test_data["absence_type_name"],
            "employer": test_data["employer"],
            "startDate": test_data["start_date"],
            "endDate": test_data["end_date"],
            "formattedDuration": test_data["formatted_duration"],
        }

        # Request time off oracle
        response = request_time_off_oracle(
            person_id=test_data["person_id"],
            absence_type_name=test_data["absence_type_name"],
            employer_id=test_data["employer_id"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
            start_time=test_data["start_time"],
            end_time=test_data["end_time"],
        )

        # Ensure that request_time_off() executed and returned proper values
        assert response.absence_request_id == test_data["absence_request_id"]
        assert response.status == test_data["status"]
        assert response.absence_type == test_data["absence_type_name"]
        assert response.employer == test_data["employer"]
        assert response.start_date == test_data["start_date"]
        assert response.end_date == test_data["end_date"]
        assert response.formatted_duration == test_data["formatted_duration"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="absences",
            payload={
                "personId": test_data["person_id"],
                "absenceType": test_data["absence_type_name"],
                "legalEntityId": test_data["employer_id"],
                "startDate": test_data["start_date"],
                "endDate": test_data["end_date"],
                "startTime": test_data["start_time"],
                "endTime": test_data["end_time"],
                "absenceStatusCd": test_data["absenceStatusCd"],
            },
        )


def test_request_time_off_oracle_with_durations() -> None:
    """Tests that the `request_time_off_oracle` function returns the expected response with start
    and end date durations."""

    # Define test data
    test_data = {
        "person_id": "300000050798130",
        "absence_type_name": "Authorized Leave",
        "start_date": "2025-05-28",
        "end_date": "2025-05-29",
        "start_time": "08:00",
        "end_time": "17:00",
        "employer_id": 300000046974965,
        "status": "AWAITING",
        "employer": "US1 Legal Entity",
        "formatted_duration": "1.5 Calendar Days",
        "absence_request_id": 300000283182505,
        "absenceStatusCd": "SUBMITTED",
        "duration": "1",
    }

    # Patch get_oracle_hcm_client to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.request_time_off_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "personAbsenceEntryId": test_data["absence_request_id"],
            "approvalStatusCd": test_data["status"],
            "absenceType": test_data["absence_type_name"],
            "employer": test_data["employer"],
            "startDate": test_data["start_date"],
            "endDate": test_data["end_date"],
            "formattedDuration": test_data["formatted_duration"],
        }

        # Request time off oracle
        response = request_time_off_oracle(
            person_id=test_data["person_id"],
            absence_type_name=test_data["absence_type_name"],
            employer_id=test_data["employer_id"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
            start_time=test_data["start_time"],
            end_time=test_data["end_time"],
            duration=test_data["duration"],
        )

        # Ensure that request_time_off() executed and returned proper values
        assert response.absence_request_id == test_data["absence_request_id"]
        assert response.status == test_data["status"]
        assert response.absence_type == test_data["absence_type_name"]
        assert response.employer == test_data["employer"]
        assert response.start_date == test_data["start_date"]
        assert response.end_date == test_data["end_date"]
        assert response.formatted_duration == test_data["formatted_duration"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="absences",
            payload={
                "personId": test_data["person_id"],
                "absenceType": test_data["absence_type_name"],
                "legalEntityId": test_data["employer_id"],
                "startDate": test_data["start_date"],
                "endDate": test_data["end_date"],
                "startTime": test_data["start_time"],
                "endTime": test_data["end_time"],
                "startDateDuration": test_data["duration"],
                "endDateDuration": test_data["duration"],
                "absenceStatusCd": test_data["absenceStatusCd"],
            },
        )


def test_request_time_off_oracle_with_absence_reason() -> None:
    """Tests that the `request_time_off_oracle` function returns the expected response with an
    absence reason."""

    # Define test data
    test_data = {
        "person_id": "300000050798130",
        "absence_type_name": "Special Leave",
        "start_date": "2025-05-29",
        "end_date": "2025-05-29",
        "start_time": "10:00",
        "end_time": "17:00",
        "employer_id": 300000046974965,
        "status": "AWAITING",
        "employer": "Netherlands Legal Entity",
        "formatted_duration": "1 Days",
        "absence_request_id": 300000283182505,
        "absenceStatusCd": "SUBMITTED",
        "absence_reason": "Family Emergency",
    }

    # Patch get_oracle_hcm_client to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.request_time_off_oracle.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "personAbsenceEntryId": test_data["absence_request_id"],
            "approvalStatusCd": test_data["status"],
            "absenceType": test_data["absence_type_name"],
            "employer": test_data["employer"],
            "startDate": test_data["start_date"],
            "endDate": test_data["end_date"],
            "formattedDuration": test_data["formatted_duration"],
        }

        # Request time off
        response = request_time_off_oracle(
            person_id=test_data["person_id"],
            absence_type_name=test_data["absence_type_name"],
            employer_id=test_data["employer_id"],
            start_date=test_data["start_date"],
            end_date=test_data["end_date"],
            start_time=test_data["start_time"],
            end_time=test_data["end_time"],
            absence_reason=test_data["absence_reason"],
        )

        # Ensure that request_time_off() executed and returned proper values
        assert response.absence_request_id == test_data["absence_request_id"]
        assert response.status == test_data["status"]
        assert response.absence_type == test_data["absence_type_name"]
        assert response.employer == test_data["employer"]
        assert response.start_date == test_data["start_date"]
        assert response.end_date == test_data["end_date"]
        assert response.formatted_duration == test_data["formatted_duration"]

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="absences",
            payload={
                "personId": test_data["person_id"],
                "absenceType": test_data["absence_type_name"],
                "legalEntityId": test_data["employer_id"],
                "startDate": test_data["start_date"],
                "endDate": test_data["end_date"],
                "startTime": test_data["start_time"],
                "endTime": test_data["end_time"],
                "absenceStatusCd": test_data["absenceStatusCd"],
                "absenceReason": test_data["absence_reason"],
            },
        )
