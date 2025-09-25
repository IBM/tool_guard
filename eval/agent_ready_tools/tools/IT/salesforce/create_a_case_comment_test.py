from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_a_case_comment import create_a_case_comment


def test_create_a_case_comment() -> None:
    """Verifies that the `create_a_case_comment` tool can successfully create a comment for a case
    in Salesforce."""

    # Define test data
    test_data = {
        "case_id": "500fJ000005XAddQAG",
        "comment": "Case closed.",
        "comment_id": "00afJ000001whwrQAA",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_a_case_comment.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.CaseComment.create.return_value = {
            "id": test_data["comment_id"]
        }

        # Create a case comment
        response = create_a_case_comment(
            case_id=test_data["case_id"],
            comment=test_data["comment"],
        )

        # Ensure that create_a_case_comment() executed and returned proper values
        assert response
        assert hasattr(response, "comment_id")

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.CaseComment.create(
            {
                "ParentId": test_data["case_id"],
                "CommentBody": test_data["comment"],
            }
        )
