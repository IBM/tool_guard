from typing import Any, Dict
from unittest.mock import patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_screening_questions import (
    get_sap_screening_questions,
)


def test_search_screening_questions() -> None:
    """Test that the `get_sap_screening_questions` function returns the expected response."""

    test_data: Dict[str, Any] = {
        "question_id": "106",
        "question_category": "Basic Screening",
        "question_source": "Recruiting",
        "top": "5",
        "skip": "0",
        "question_name": "Are you at least 18 years of age?",
        "question_type": "QUESTION_MULTI_CHOICE",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.search_screening_questions.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = mock_sap_client.return_value
        mock_client.get_request.return_value = {
            "d": {
                "results": [
                    {
                        "questionId": test_data["question_id"],
                        "questionCategory": test_data["question_category"],
                        "questionSource": test_data["question_source"],
                        "questionName": test_data["question_name"],
                        "questionType": test_data["question_type"],
                    }
                ]
            }
        }

        response = get_sap_screening_questions(
            top=test_data["top"],
            skip=test_data["skip"],
        )

        assert response
        question = response.questions[0]
        assert question.question_id == test_data["question_id"]
        assert question.question_category == test_data["question_category"]
        assert question.question_source == test_data["question_source"]
        assert question.question_name == test_data["question_name"]
        assert question.question_type == test_data["question_type"]

        mock_client.get_request.assert_called_once_with(
            entity="JobReqQuestion",
            params={
                "$top": test_data["top"],
                "$skip": test_data["skip"],
            },
        )
