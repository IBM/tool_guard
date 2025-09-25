from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.update_project import update_project


def test_update_project() -> None:
    """Verifies that the `update_project` tool can successfully update a project in Adobe
    Workfront."""

    test_data = {
        "project_id": "682b3a25000ac9d6e7196c10924a8cfc",
        "project_name": "Test Project",
        "priority": "High",
        "planned_start_date": "2024-01-15",
        "status": "CUR",
        "owner_id": "67e168720af75981a4c50727a739cd29",
        "program_id": "6596dfb000128b8364d609b75675034e",
        "portfolio_id": "62225baf0011b754d8df8eb624c0e1f6",
    }

    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_project.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client

        mock_client.put_request.return_value = {
            "data": {
                "ID": test_data["project_id"],
                "name": test_data["project_name"],
                "status": test_data["status"],
            }
        }

        response = update_project(
            project_id=test_data["project_id"],
            project_name=test_data["project_name"],
            priority=test_data["priority"],
            planned_start_date=test_data["planned_start_date"],
            status=test_data["status"],
            owner_id=test_data["owner_id"],
            program_id=test_data["program_id"],
            portfolio_id=test_data["portfolio_id"],
        )

        assert response
        assert response.project_id == test_data["project_id"]
        assert response.name == test_data["project_name"]
        assert response.status == test_data["status"]

        mock_client.get_request.assert_not_called()

        mock_client.put_request.assert_called_once_with(
            entity=f"proj/{test_data['project_id']}",
            payload={
                "name": test_data["project_name"],
                "priority": test_data["priority"],
                "planned_start_date": test_data["planned_start_date"],
                "status": test_data["status"],
                "owner_id": test_data["owner_id"],
                "program_id": test_data["program_id"],
                "portfolio_id": test_data["portfolio_id"],
            },
        )


def test_update_project_minimal_params() -> None:
    """Verifies that the `update_project` tool works with minimal parameters."""

    test_data = {
        "project_id": "simple123",
        "project_name": "Simple Project",
        "status": "CUR",
    }

    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_project.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client

        mock_client.put_request.return_value = {
            "data": {
                "ID": test_data["project_id"],
                "name": test_data["project_name"],
                "status": test_data["status"],
            }
        }

        response = update_project(
            project_id=test_data["project_id"],
            project_name=test_data["project_name"],
            status=test_data["status"],
        )

        assert response
        assert response.project_id == test_data["project_id"]
        assert response.name == test_data["project_name"]
        assert response.status == test_data["status"]

        mock_client.get_request.assert_not_called()

        mock_client.put_request.assert_called_once_with(
            entity=f"proj/{test_data['project_id']}",
            payload={"name": test_data["project_name"], "status": test_data["status"]},
        )


def test_update_project_only_optional_params() -> None:
    """Verifies that the `update_project` tool works when only optional parameters are provided."""

    test_data = {
        "project_id": "optional123",
        "project_name": "Optional Project",
        "priority": "Medium",
    }

    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.update_project.get_adobe_workfront_client"
    ) as mock_adobe_workfront_client:
        mock_client = MagicMock()
        mock_adobe_workfront_client.return_value = mock_client

        mock_client.put_request.return_value = {
            "data": {
                "ID": test_data["project_id"],
                "name": test_data["project_name"],
                "status": "CUR",
            }
        }

        response = update_project(
            project_id=test_data["project_id"],
            project_name=test_data["project_name"],
            priority=test_data["priority"],
        )

        assert response
        assert response.project_id == test_data["project_id"]
        assert response.name == test_data["project_name"]
        assert response.status == "CUR"

        mock_client.get_request.assert_not_called()

        mock_client.put_request.assert_called_once_with(
            entity=f"proj/{test_data['project_id']}",
            payload={
                "name": test_data["project_name"],
                "priority": test_data["priority"],
            },
        )
