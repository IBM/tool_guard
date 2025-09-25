from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_utility import (
    get_new_question_number,
)


def test_get_new_question_number() -> None:
    """Tests that the `get_new_question_number` function returns the expected response."""
    # Define test data:
    test_data: Dict[str, Any] = {"job_req_id": "67997", "question_number": 7}

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_utility.get_sap_successfactors_client"
    ) as mock_get_client:

        # Create a mock client instance
        mock_client = MagicMock()
        mock_response = {"d": {"results": [{"order": test_data["question_number"]}]}}

        mock_client.get_request.return_value = mock_response
        mock_get_client.return_value = mock_client

        # Check the order value
        result = get_new_question_number(test_data["job_req_id"])

        # Ensure that get_screening_questions() executed and returned proper values
        assert result == test_data["question_number"] + 1

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            entity="JobReqScreeningQuestion", filter_expr=f"jobReqId eq '{test_data["job_req_id"]}'"
        )
