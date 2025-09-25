from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.delete_solution import delete_solution


def test_delete_solution() -> None:
    """Test that the `delete_solution` function returns the expected response."""

    solution_id = "501fJ00001yIczpQAC"
    test_response = 204

    with patch(
        "agent_ready_tools.tools.IT.salesforce.delete_solution.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Solution.delete.return_value = test_response

        response = delete_solution(solution_id)

        assert response
        assert response == test_response

        mock_client.salesforce_object.Solution.delete.assert_called_once_with(solution_id)
