from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.update_screening_question import (
    update_screening_question,
)


# Scenario 1: FREE‑TEXT question type
def test_update_screening_question_free_text() -> None:
    """Test updating a free text screening question."""

    test_data: Dict[str, Any] = {
        "job_requisition_id": "67979",
        "question_number": "1",
        "question_name": "What is your updated name?",
        "question_type": "FREE_TEXT",
        "max_length": 200,
        "required": True,
        "locale": "en_US",
        "response_http_code": 204,
        "response_message": "Question updated successfully",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.update_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        response = update_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_number=test_data["question_number"],
            question_type=test_data["question_type"],
            question_name=test_data["question_name"],
            max_length=test_data["max_length"],
            required=test_data["required"],
            locale=test_data["locale"],
        )

        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "locale": test_data["locale"],
                "order": test_data["question_number"],
                "questionType": "QUESTION_TEXT",
                "questionName": test_data["question_name"],
                "maxLength": test_data["max_length"],
                "required": test_data["required"],
            }
        )


# Scenario 2: NUMERIC question type
def test_update_screening_question_numeric() -> None:
    """Test updating a numeric screening question."""

    test_data: Dict[str, Any] = {
        "job_requisition_id": "67979",
        "question_number": "2",
        "question_name": "How many years of experience do you have?",
        "question_type": "NUMERIC",
        "expected_answer_value": 1.0,
        "expected_direction": "higher",
        "question_weight": 24.0,
        "required": True,
        "disqualifier": False,
        "score": True,
        "locale": "en_US",
        "response_http_code": 204,
        "response_message": "Question updated successfully",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.update_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        response = update_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_number=test_data["question_number"],
            question_type=test_data["question_type"],
            question_name=test_data["question_name"],
            expected_answer_value=test_data["expected_answer_value"],
            expected_direction=test_data["expected_direction"],
            question_weight=test_data["question_weight"],
            required=test_data["required"],
            disqualifier=test_data["disqualifier"],
            score=test_data["score"],
            locale=test_data["locale"],
        )

        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "locale": test_data["locale"],
                "order": test_data["question_number"],
                "questionType": "QUESTION_NUMERIC",
                "questionName": test_data["question_name"],
                "expectedAnswerValue": test_data["expected_answer_value"],
                "expectedDir": test_data["expected_direction"],
                "questionWeight": test_data["question_weight"],
                "required": test_data["required"],
                "disqualifier": test_data["disqualifier"],
                "score": test_data["score"],
            }
        )


# Scenario 3: RATING‑SCALE question type
def test_update_screening_question_rating_scale() -> None:
    """Test updating a rating scale type screening question."""

    test_data: Dict[str, Any] = {
        "job_requisition_id": "67979",
        "question_number": "3",
        "question_name": "Rate your communication skills",
        "question_type": "RATING_SCALES",
        "rating_format": "PERFORMANCE_RATING_SCALE",
        "expected_answer_label": "Extraordinary",
        "question_weight": 28.0,
        "required": True,
        "disqualifier": False,
        "score": True,
        "expected_direction": "higher",
        "locale": "en_US",
        "response_http_code": 204,
        "response_message": "Question updated successfully",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.update_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        response = update_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_number=test_data["question_number"],
            question_type=test_data["question_type"],
            question_name=test_data["question_name"],
            rating_format=test_data["rating_format"],
            expected_answer_label=test_data["expected_answer_label"],
            expected_direction=test_data["expected_direction"],
            question_weight=test_data["question_weight"],
            required=test_data["required"],
            disqualifier=test_data["disqualifier"],
            score=test_data["score"],
            locale=test_data["locale"],
        )

        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "locale": test_data["locale"],
                "order": test_data["question_number"],
                "questionType": "QUESTION_RATING",
                "questionName": test_data["question_name"],
                "ratingScale": "Performance Rating Scale",
                "expectedAnswerValue": 5,
                "expectedDir": test_data["expected_direction"],
                "questionWeight": test_data["question_weight"],
                "required": test_data["required"],
                "disqualifier": test_data["disqualifier"],
                "score": test_data["score"],
            }
        )


# Scenario 4: MULTIPLE‑CHOICE question type
def test_update_screening_question_multiple_choice() -> None:
    """Test updating a multiple choice screening question."""

    test_data: Dict[str, Any] = {
        "job_requisition_id": "67979",
        "question_number": "4",
        "question_name": "Which languages do you speak?",
        "question_type": "MULTIPLE_CHOICE",
        "choice_list": ["match", "123"],
        "question_weight": 29.0,
        "required": True,
        "disqualifier": False,
        "score": True,
        "locale": "en_US",
        "response_http_code": 204,
        "response_message": "Question updated successfully",
    }

    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.update_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        response = update_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_number=test_data["question_number"],
            question_type=test_data["question_type"],
            question_name=test_data["question_name"],
            choice_list=test_data["choice_list"],
            question_weight=test_data["question_weight"],
            required=test_data["required"],
            disqualifier=test_data["disqualifier"],
            score=test_data["score"],
            locale=test_data["locale"],
        )

        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "locale": test_data["locale"],
                "order": test_data["question_number"],
                "questionType": "QUESTION_MULTI_CHOICE",
                "questionName": test_data["question_name"],
                "choices": {"results": [{"optionLabel": "match"}, {"optionLabel": "123"}]},
                "questionWeight": test_data["question_weight"],
                "required": test_data["required"],
                "disqualifier": test_data["disqualifier"],
                "score": test_data["score"],
            }
        )


# Scenario 5: Invalid job_requisition_id
def test_update_screening_question_invalid_job_req_id() -> None:
    """Tests that updating a screening question fails with an invalid job_requisition_id."""

    test_data: Dict[str, Any] = {
        "job_requisition_id": "Invalid",
        "question_number": "1",
        "question_type": "FREE_TEXT",
        "question_name": "Dummy?",
        "locale": "en_US",
        "max_length": 100,
        "response_http_code": 400,
        "response_message": 'Property jobReqId has invalid value. For input string: "Invalid", required type is Edm.Int64.',
        "error_message": None,
        "error_description": None,
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.update_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client:
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [
                {
                    "httpCode": test_data["response_http_code"],
                    "message": test_data["response_message"],
                }
            ]
        }

        # Attempt to update a screening question with an invalid job_requisition_id
        response = update_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_number=test_data["question_number"],
            question_type=test_data["question_type"],
            question_name=test_data["question_name"],
            max_length=test_data["max_length"],
        )

        # Validate the result object
        assert response
        assert response.http_code == test_data["response_http_code"]
        assert response.message == test_data["response_message"]

        # Ensure the API call was made with the expected payload
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "order": test_data["question_number"],
                "locale": test_data["locale"],
                "questionType": "QUESTION_TEXT",
                "questionName": test_data["question_name"],
                "maxLength": test_data["max_length"],
            }
        )
