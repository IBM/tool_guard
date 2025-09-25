from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
    AdobeWorkfrontProjectStatus,
)
from agent_ready_tools.tools.IT.adobe_workfront.list_projects import Project, list_projects


def test_list_projects_with_filter() -> None:
    """Verify that the `list_projects` tool can successfully retrieve projects in Adobe Workfront
    with a filter."""

    # Define test data:
    test_data = {
        "project_id": "6662150f0003312748ee577e42704273",
        "project_name": "Creative Assistant Product Lifecycle",
        "projected_completion_date": "2025-02-25T11:05:17:728-0500",
        "status": "COMPLETED",
        "$$LIMIT": 50,
    }
    proj_priority = "NORMAL"

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_projects.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["project_id"],
                    "name": test_data["project_name"],
                    "projectedCompletionDate": test_data["projected_completion_date"],
                    "status": AdobeWorkfrontProjectStatus[str(test_data["status"])].value,
                    "priority": AdobeWorkfrontPriority[proj_priority.upper()].value,
                }
            ]
        }

        # Get Adobe Workfront projects with status filter
        response = list_projects(status=test_data["status"], limit=test_data["$$LIMIT"])
        # Ensure that list_projects() executed and returned proper values
        expected_data = Project(
            project_id=str(test_data["project_id"]),
            project_name=str(test_data["project_name"]),
            projected_completion_date=str(test_data["projected_completion_date"]),
            status=str(test_data["status"]),
            priority=proj_priority,
        )
        assert response
        assert response.projects[0] == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="proj/search",
            params={
                "status": AdobeWorkfrontProjectStatus[str(test_data["status"])].value,
                "$$LIMIT": 50,
            },
        )


def test_list_projects_without_filter() -> None:
    """Verify that the `list_projects` tool can successfully retrieve all Adobe Workfront projects
    without any filters."""

    # Define test data:
    test_data = {
        "project_id": "6662150f0003312748ee577e42704273",
        "project_name": "Creative Assistant Product Lifecycle",
        "projected_completion_date": "2025-02-25T11:05:17:728-0500",
        "status": "COMPLETED",
        "$$LIMIT": 50,
    }
    proj_priority = "NORMAL"

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.list_projects.get_adobe_workfront_client"
    ) as mock_adobe_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_adobe_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "data": [
                {
                    "ID": test_data["project_id"],
                    "name": test_data["project_name"],
                    "projectedCompletionDate": test_data["projected_completion_date"],
                    "status": AdobeWorkfrontProjectStatus[str(test_data["status"])].value,
                    "priority": AdobeWorkfrontPriority[proj_priority.upper()].value,
                }
            ]
        }

        # Get all Adobe Workfront projects without any filters
        response = list_projects(limit=test_data["$$LIMIT"])

        # Ensure that list_projects() executed and returned proper values
        expected_data = Project(
            project_id=str(test_data["project_id"]),
            project_name=str(test_data["project_name"]),
            projected_completion_date=str(test_data["projected_completion_date"]),
            status=str(test_data["status"]),
            priority=proj_priority,
        )
        assert response
        assert response.projects[0] == expected_data

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="proj/search", params={"$$LIMIT": 50}
        )
