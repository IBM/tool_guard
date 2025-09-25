from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_solution import create_solution
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Solution


def test_create_solution() -> None:
    """Test that the `create_solution` function returns the expected response."""

    test_data = {
        "name": "Solution 1",
        "status": "Draft",
        "description": "Test Solution",
    }

    solution_data = {
        "id": "001",
        "name": "Solution 1",
        "status": "Draft",
        "description": "Test Solution",
    }

    expected = Solution(**solution_data)  # type: ignore[arg-type]

    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_solution.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Solution.create.return_value = {
            "id": "001",
            "success": True,
            "errors": [],
        }

        response = create_solution(**test_data)

        assert response
        assert response == expected

        mock_client.salesforce_object.Solution.create(
            {
                "Name": test_data["name"],
                "Status": test_data["status"],
                "Description": test_data["description"],
            }
        )
