from unittest.mock import MagicMock, patch

from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.tools.IT.salesforce.list_solutions import list_solutions


def test_list_solutions() -> None:
    """Tests that the `list_solutions` tool retrieves solutions successfully."""

    # Define test data
    test_data = {
        "solution_id": "501gL000003fjdxQAA",
        "solution_name": "GC1020 Portable Generator Switch Malfunctioning",
        "solution_number": "00000001",
        "solution_status": "Reviewed",
        "solution_note": "If the generator switch is not working, remove the switch and re-assemble it. Often the switch gets displaced by a fraction of an inch preventing it from engaging with the internal generator mechanism.",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_solutions.get_salesforce_client"
    ) as mock_salesforce_client:

        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["solution_id"],
                "SolutionName": test_data["solution_name"],
                "SolutionNumber": test_data["solution_number"],
                "Status": test_data["solution_status"],
                "SolutionNote": test_data["solution_note"],
            }
        ]

        # List all solutions
        response = list_solutions()

        assert response
        assert response.solutions[0].id == test_data["solution_id"]
        assert response.solutions[0].name == test_data["solution_name"]
        assert response.solutions[0].number == test_data["solution_number"]
        assert response.solutions[0].status == test_data["solution_status"]
        assert response.solutions[0].description == test_data["solution_note"]

        # Ensure the API call was made with expected parameters

        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                "SELECT Id, SolutionName, SolutionNumber,Status,SolutionNote FROM Solution "
            )
        )


def test_list_solutions_with_solution_number() -> None:
    """Tests that the `list_solutions` tool retrieves solutions successfully."""

    # Define test data
    test_data = {
        "solution_id": "501gL000003fjdxQAA",
        "solution_name": "GC1020 Portable Generator Switch Malfunctioning",
        "solution_number": "00000001",
        "solution_status": "Reviewed",
        "solution_note": "If the generator switch is not working, remove the switch and re-assemble it. Often the switch gets displaced by a fraction of an inch preventing it from engaging with the internal generator mechanism.",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_solutions.get_salesforce_client"
    ) as mock_salesforce_client:

        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["solution_id"],
                "SolutionName": test_data["solution_name"],
                "SolutionNumber": test_data["solution_number"],
                "Status": test_data["solution_status"],
                "SolutionNote": test_data["solution_note"],
            }
        ]

        # List all solutions
        response = list_solutions(f"SolutionNumber={test_data["solution_number"]}")

        assert response
        assert response.solutions[0].id == test_data["solution_id"]
        assert response.solutions[0].name == test_data["solution_name"]
        assert response.solutions[0].number == test_data["solution_number"]
        assert response.solutions[0].status == test_data["solution_status"]
        assert response.solutions[0].description == test_data["solution_note"]

        # Ensure the API call was made with expected parameters

        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                "SELECT Id, SolutionName, SolutionNumber,Status,SolutionNote FROM Solution WHERE SolutionNumber = '00000001'",
            )
        )
