from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.update_solution import update_solution


def test_update_solution() -> None:
    """Test that the `update_solution` tool returns the expected response."""

    # Define data
    test_data = {
        "solution_id": "501gL000003fjdxQAA",
        "solution_name": "GC1020 Portable Generator Switch Malfunctioning",
        "status": "Reviewed",
        "solution_details": "If the generator switch is not working, remove the switch and re-assemble it. Often the switch gets displaced by a fraction of an inch preventing it from engaging with the internal generator mechanism.",
        "is_public": True,
        "is_visible_in_public_knowledge_base": False,
    }
    test_response = 204

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.update_solution.get_salesforce_client"
    ) as mock_salesforce_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Solution.update.return_value = test_response

        # Update Solution
        response = update_solution(**test_data)

        # Ensure that update_solution() executed and returned proper values
        assert response
        assert response == test_response

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Solution.update(test_data, test_data["solution_id"])
