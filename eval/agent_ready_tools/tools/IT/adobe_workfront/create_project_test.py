from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.adobe_workfront.adobe_workfront_schemas import (
    AdobeWorkfrontPriority,
    AdobeWorkfrontProjectStatus,
)
from agent_ready_tools.tools.IT.adobe_workfront.create_project import create_project


def test_create_project() -> None:
    """Verifies that the `create_project` tool can successfully create a project in Adobe
    Workfront."""

    # Define test data with type annotations
    test_data: Dict[str, Any] = {
        "name": "Yousuf Project 2",
        "planned_start_date": "2025-01-01",
        "description": "This is a test project.",
        "priority": "HIGH",  # Ensure this is a string
        "fixed_revenue": 10000.0,
        "portfolio_id": "682b1775000efd21d7a1bf33d07d45e2",
    }

    # Patch `get_adobe_workfront_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.adobe_workfront.create_project.get_adobe_workfront_client"
    ) as mock_workfront_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_workfront_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "data": {"name": test_data["name"], "ID": "mock_project_id", "status": "PLN"}
        }

        # Create a project
        response = create_project(
            name=test_data["name"],
            planned_start_date=test_data["planned_start_date"],
            description=test_data["description"],
            priority=test_data["priority"],
            fixed_revenue=test_data["fixed_revenue"],
            portfolio_id=test_data["portfolio_id"],
        )

        # Ensure the response is not None
        assert response is not None

        # Validate the project name
        assert response.project_name == test_data["name"]
        assert response.project_id is not None
        assert response.status == AdobeWorkfrontProjectStatus.PLANNING.name
        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            entity="proj",
            payload={
                "name": test_data["name"],
                "plannedStartDate": test_data["planned_start_date"],
                "description": test_data["description"],
                "priority": AdobeWorkfrontPriority[str(test_data["priority"]).upper()].value,
                "fixedRevenue": test_data["fixed_revenue"],
                "portfolioID": test_data["portfolio_id"],
            },
        )
