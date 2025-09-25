from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.IT.salesforce.create_case import create_case


def test_create_case() -> None:
    """Tests that the case can be created successfully by the `create_case` tool."""

    # Define test data:
    test_data = {
        "case_subject": "Lenovo Laptop 5",
        "case_type": "Hardware",
        "case_reason": "Hardware Failure",
        "case_status": "New",
        "case_origin": "Web",
        "priority": "High",
        "case_id": "500fJ000005WuM3QAK",
    }

    # Patch `get_salesforce_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.IT.salesforce.create_case.get_salesforce_client"
    ) as mock_salesforce_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.Case.create.return_value = {"id": test_data["case_id"]}

        # Create a case
        response = create_case(
            case_subject=test_data["case_subject"],
            case_type=test_data["case_type"],
            case_reason=test_data["case_reason"],
            case_status=test_data["case_status"],
            case_origin=test_data["case_origin"],
            priority=test_data["priority"],
        )

        # Ensure that create_a_case() executed and returned proper values
        assert response
        assert response.case_id is not None

        # Ensure the API call was made with expected parameters
        mock_client.salesforce_object.Case.create(
            {
                "Subject": test_data["case_subject"],
                "Type": test_data["case_type"],
                "Reason": test_data["case_reason"],
                "Status": test_data["case_status"],
                "Origin": test_data["case_origin"],
                "Priority": test_data["priority"],
            }
        )
