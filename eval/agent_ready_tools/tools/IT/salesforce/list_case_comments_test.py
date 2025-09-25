from typing import Any
from unittest.mock import MagicMock, patch

from simple_salesforce import format_soql  # type: ignore[attr-defined]

from agent_ready_tools.tools.IT.salesforce.list_case_comments import list_case_comments
from agent_ready_tools.tools.IT.salesforce.salesforce_schemas import CaseComment


def test_list_case_comments() -> None:
    """Tests that the `list_case_comments` tool returns the expected response."""

    # Define test case status data
    test_data: dict[str, Any] = {
        "comment_id": "00agL000000M3X7QAK",
        "case_id": "500gL000003hm4TQAQ",
        "comment": "This is a comment on the case.",
        "comment_created_date": "2025-04-23T10:06:31.000+0000",
        "published": False,
    }

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_comments.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["comment_id"],
                "ParentId": test_data["case_id"],
                "CommentBody": test_data["comment"],
                "CreatedDate": test_data["comment_created_date"],
                "IsPublished": test_data["published"],
            }
        ]

        # Call the function
        response = list_case_comments(
            "ParentId = '500gL000003hm4TQAQ' AND CommentBody = 'This is a comment on the case.'"
        )

        # Construct expected object
        expected_value = [
            CaseComment(
                comment_id=test_data["comment_id"],
                case_id=test_data["case_id"],
                comment=test_data["comment"],
                comment_created_date=test_data["comment_created_date"],
                published=test_data["published"],
            )
        ]

        # Assertions
        assert response == expected_value

        # Ensure the salesforce object call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                f"SELECT Id, CommentBody, ParentId, CreatedDate, IsPublished FROM CaseComment WHERE ParentId = '500gL000003hm4TQAQ' AND CommentBody = 'This is a comment on the case.'"
            )
        )


def test_list_case_comments_without_filter() -> None:
    """Tests that the `list_case_comments` tool returns the expected response."""

    # Define test case status data
    test_data: dict[str, Any] = {
        "comment_id": "00agL000000M3X7QAK",
        "case_id": "500gL000003hm4TQAQ",
        "comment": "This is a comment on the case.",
        "comment_created_date": "2025-04-23T10:06:31.000+0000",
        "published": False,
    }

    # Patch the Salesforce client used in the tool
    with patch(
        "agent_ready_tools.tools.IT.salesforce.list_case_comments.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create mock client and set up return value
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "Id": test_data["comment_id"],
                "ParentId": test_data["case_id"],
                "CommentBody": test_data["comment"],
                "CreatedDate": test_data["comment_created_date"],
                "IsPublished": test_data["published"],
            }
        ]

        # Call the function
        response = list_case_comments()

        # Construct expected object
        expected_value = [
            CaseComment(
                comment_id=test_data["comment_id"],
                case_id=test_data["case_id"],
                comment=test_data["comment"],
                comment_created_date=test_data["comment_created_date"],
                published=test_data["published"],
            )
        ]

        # Assertions
        assert response[:1] == expected_value

        # Ensure the salesforce object call was made with expected parameters
        mock_client.salesforce_object.query_all_iter.assert_called_once_with(
            format_soql(
                f"SELECT Id, CommentBody, ParentId, CreatedDate, IsPublished FROM CaseComment "
            )
        )
