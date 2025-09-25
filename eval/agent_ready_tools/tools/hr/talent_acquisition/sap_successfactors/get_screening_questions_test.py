from typing import Any, Dict
from unittest.mock import patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_screening_questions import (
    get_screening_questions,
)


def test_screening_questions() -> None:
    """Test that the `get_screening_questions` function returns the expected response."""

    test_data: Dict[str, Any] = {
        "job_req_id": "66984",
        "text": "what is your primary language",
        "type": "QUESTION_MULTI_CHOICE",
        "order": "2",
        "description": None,
        "choices": ["java", "c", "c++", "other"],
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.get_screening_questions.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = mock_sap_client.return_value
        mock_choices = {"results": [{"optionLabel": choice} for choice in test_data["choices"]]}
        expected_choices = test_data["choices"]

        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "order": test_data["order"],
                        "questionName": test_data["text"],
                        "questionType": test_data["type"],
                        "questionDescription": test_data["description"],
                        "choices": mock_choices,
                    }
                ]
            }
        }

        response = get_screening_questions(job_req_id=test_data["job_req_id"])

        assert response
        question = response.questions[0]
        assert question.text == test_data["text"]
        assert question.type == test_data["type"]
        assert question.order == test_data["order"]
        assert question.description == test_data["description"]
        assert question.choices == expected_choices

        mock_client.get_request.assert_called_once_with(
            entity="JobReqScreeningQuestion",
            filter_expr=f"jobReqId eq '{test_data['job_req_id']}'",
            expand_expr="choices",
        )
