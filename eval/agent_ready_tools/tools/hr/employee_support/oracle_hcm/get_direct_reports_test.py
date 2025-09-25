from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_direct_reports import (
    oracle_get_direct_reports,
)


def test_oracle_get_direct_reports() -> None:
    """Test that the get_direct_reports tool function returns the expected response."""

    # Define data
    test_data = {
        "worker_id": "00020000000EACED00057708000110D942344D750000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000196D664000078",
        "period_of_service_id": "300000281382272",
        "assignment_uniq_id": "00020000000EACED00057708000110D942344D860000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000196D664000078",
        "assignment_name": "E6587",
        "person_number": "6587",
        "display_name": "Agent test Agent from1",
        "manager_person_number": "6519",
        "relationship_type": "LINE_MANAGER",
        "level": 1,
    }

    with patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_direct_reports.get_worker_work_relationship"
    ) as mock_get_worker_work_relationship, patch(
        "agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_direct_reports.get_oracle_hcm_client"
    ) as mock_oracle_client:

        # Mock the Oracle HCM client
        mock_client = MagicMock()
        mock_oracle_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "items": [
                {
                    "AssignmentName": test_data["assignment_name"],
                    "PersonNumber": test_data["person_number"],
                    "DisplayName": test_data["display_name"],
                    "ManagerPersonNumber": test_data["manager_person_number"],
                    "RelationshipType": test_data["relationship_type"],
                    "Level": test_data["level"],
                }
            ]
        }

        # Mock the work relationship structure
        mock_workrelation = MagicMock()
        mock_workrelation.period_of_service_id = test_data["period_of_service_id"]

        mock_all_workrelation = MagicMock()
        mock_all_workrelation.worker_work_relationship = [mock_workrelation]

        mock_get_worker_work_relationship.return_value = mock_all_workrelation

        # Call the function under test
        response = oracle_get_direct_reports(
            worker_id=test_data["worker_id"],
            assignment_uniq_id=test_data["assignment_uniq_id"],
        )

        # Assertions
        assert response
        assert response.direct_reports[0].assignment_name == test_data["assignment_name"]
        assert response.direct_reports[0].person_number == test_data["person_number"]
        assert response.direct_reports[0].display_name == test_data["display_name"]
        assert (
            response.direct_reports[0].manager_person_number == test_data["manager_person_number"]
        )
        assert response.direct_reports[0].relationship_type == test_data["relationship_type"]
        assert response.direct_reports[0].level == test_data["level"]

        mock_client.get_request.assert_called_once_with(
            entity=f"/workers/{test_data['worker_id']}/child/workRelationships/{test_data['period_of_service_id']}/child/assignments/{test_data['assignment_uniq_id']}/child/allReports"
        )
