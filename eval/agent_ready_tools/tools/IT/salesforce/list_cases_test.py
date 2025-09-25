from typing import Any
from unittest.mock import MagicMock, patch

from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.tools.IT.salesforce.list_cases import list_cases
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import Case


def test_list_cases() -> None:
    """Tests that the `list_cases` tool returns the expected response."""

    # Define test case status data
    test_data: dict[str, Any] = {
        "case_id": "500fJ000000kioYQAQ",
        "case_name": "Agent case update",
        "case_number": "00001000",
        "account_id": "001fJ00000223n6QAA",
        "owner_id": "005fJ000000L0jNQAS",
        "created_date": "2024-12-03T19:14:49.000+0000",
    }

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_cases.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["case_id"],
                "Subject": test_data["case_name"],
                "CaseNumber": test_data["case_number"],
                "AccountId": test_data["account_id"],
                "OwnerId": test_data["owner_id"],
                "CreatedDate": test_data["created_date"],
            }
        ]

        # Call the function
        response = list_cases("Subject = 'Agent case update' AND CaseNumber = '00001000'")

        # Construct expected object
        expected_value = [
            Case(
                case_id=test_data["case_id"],
                case_name=test_data["case_name"],
                case_number=test_data["case_number"],
                account_id=test_data["account_id"],
                owner_id=test_data["owner_id"],
                created_date=test_data["created_date"],
            )
        ]

        # Assertions
        assert response == expected_value

        # Ensure the salesforce object call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                f"SELECT Id, Subject, CaseNumber, AccountId, OwnerId, CreatedDate FROM Case WHERE Subject = 'Agent case update' AND CaseNumber = '00001000'"
            )
        )


def test_list_cases_without_filter() -> None:
    """Tests that the `list_cases` tool returns the expected response."""

    # Define test case status data
    test_data: dict[str, Any] = {
        "case_id": "500fJ000000kioZQAQ",
        "case_name": "Performance inadequate for second consecutive week",
        "case_number": "00001001",
        "account_id": "001fJ00000223nBQAQ",
        "owner_id": "005fJ000000L0jNQAS",
        "created_date": "2024-12-02T19:14:49.000+0000",
    }

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_cases.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["case_id"],
                "Subject": test_data["case_name"],
                "CaseNumber": test_data["case_number"],
                "AccountId": test_data["account_id"],
                "OwnerId": test_data["owner_id"],
                "CreatedDate": test_data["created_date"],
            }
        ]

        # Call the function
        response = list_cases()

        # Construct expected object
        expected_value = [
            Case(
                case_id=test_data["case_id"],
                case_name=test_data["case_name"],
                case_number=test_data["case_number"],
                account_id=test_data["account_id"],
                owner_id=test_data["owner_id"],
                created_date=test_data["created_date"],
            )
        ]

        # Assertions
        assert response[:1] == expected_value

        # Ensure the salesforce object call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                f"SELECT Id, Subject, CaseNumber, AccountId, OwnerId, CreatedDate FROM Case "
            )
        )
