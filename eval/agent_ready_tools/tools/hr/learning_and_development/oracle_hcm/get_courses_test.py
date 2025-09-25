from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_courses import (
    _get_courses_payload,
    get_courses,
)
from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.learning_test_bytes import (
    COURSE_REPORT_BYTES,
)
from agent_ready_tools.utils.dict_to_object import Obj


def test_get_courses_with_filter() -> None:
    """Test that the `get_courses` function returns the expected response."""

    # Define test data:
    test_data = {
        "course_number": "OLC101105",
        "course_name": "Inspirational Leadership",
        "status": "Active",
        "start_date": "31/10/2017",
        "end_date": "",
        "learning_category": "Leadership",
        "name": "Inspirational Leadership",
        "learning_id": "300000156818214",
        "report_bytes": COURSE_REPORT_BYTES,
    }

    # Patch `get_oracle_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_courses.get_oracle_soap_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_courses.return_value = Obj(
            {
                "body": {
                    "run_report_response": {
                        "run_report_return": {
                            "report_bytes": test_data["report_bytes"],
                        }
                    }
                }
            }
        )

        # Get courses
        response = get_courses().course_details[0]
        # Ensure that get_courses() executed and returned proper values
        assert response
        assert response.course_number == test_data["course_number"]
        assert response.course_name == test_data["course_name"]
        assert response.course_description is not None
        assert response.status == test_data["status"]
        assert response.start_date == test_data["start_date"]
        assert response.learning_category == test_data["learning_category"]
        assert response.learning_id == test_data["learning_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_courses.assert_called_once_with(_get_courses_payload())


def test_get_courses_without_filter() -> None:
    """Test that the `get_courses` function returns the expected response."""

    # Define test data:
    test_data = {
        "course_number": "OLC101105",
        "course_name": "Inspirational Leadership",
        "status": "Active",
        "start_date": "31/10/2017",
        "end_date": "",
        "learning_category": "Leadership",
        "name": "Inspirational Leadership",
        "learning_id": "300000156818214",
        "report_bytes": COURSE_REPORT_BYTES,
    }

    # Patch `get_oracle_soap_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.get_courses.get_oracle_soap_client"
    ) as mock_oracle_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_courses.return_value = Obj(
            {
                "body": {
                    "run_report_response": {
                        "run_report_return": {
                            "report_bytes": test_data["report_bytes"],
                        }
                    }
                }
            }
        )

        # Get courses
        response = get_courses().course_details[0]

        # Ensure that get_courses() executed and returned proper values
        assert response
        assert response.course_number == test_data["course_number"]
        assert response.course_name == test_data["course_name"]
        assert response.course_description is not None
        assert response.status == test_data["status"]
        assert response.start_date == test_data["start_date"]
        assert response.learning_category == test_data["learning_category"]
        assert response.learning_id == test_data["learning_id"]

        # Ensure the API call was made with expected parameters
        mock_client.get_courses.assert_called_once_with(_get_courses_payload())
