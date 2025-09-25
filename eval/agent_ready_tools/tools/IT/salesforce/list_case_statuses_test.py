from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.list_case_statuses import list_case_statuses
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseStatus


def test_list_case_statuses() -> None:
    """Tests that the `list_case_statuses` function returns the expected response."""

    # Define test data
    test_data = {
        "case_status_id": "01JgL000007NyXrUAK",
        "case_status_name": "New",
        "sort_order": 1,
        "created_date": "2025-04-11T03:36:12.000+0000",
    }

    expected = CaseStatus(**test_data)  # type: ignore[arg-type]

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_statuses.get_salesforce_client"
    ) as mock_salesforce_client:
        # Set up the mock Salesforce client and its response
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["case_status_id"],
                "MasterLabel": test_data["case_status_name"],
                "SortOrder": test_data["sort_order"],
                "CreatedDate": test_data["created_date"],
            }
        ]

        # Call the tool function with a mock search clause
        response = list_case_statuses("MasterLabel = 'New' OR Id = '01JgL000007NyXrUAK'")

        # Assert the output matches the expected result
        assert response[0] == expected

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            "SELECT Id, MasterLabel, SortOrder, CreatedDate FROM CaseStatus WHERE MasterLabel = 'New' OR Id = '01JgL000007NyXrUAK'"
        )
