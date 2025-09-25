from typing import Any, Dict
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question import (
    create_screening_question,
)
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_schemas import (
    SuccessFactorsQuestionType,
    SuccessFactorsRatingScaleFormat,
)


# Scenario 1: FREE_TEXT question type
def test_create_screening_question_freetext() -> None:
    """Verify that the `create_screening_question` tool can successfully create a freetext screening
    question."""
    # Define test data:
    test_data: Dict[str, Any] = {
        "job_requisition_id": "67943",
        "question_type": "FREE_TEXT",
        "screening_question": "Rate your communication skills",
        "max_length": 200,
        "http_code": 204,
        "required": True,
        "locale": "en_US",
        "question_number": "8",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_new_question_number"
    ) as mock_screening_questions_client:

        # Create a mock for get screening question
        mock_screening_questions_client.return_value = test_data["question_number"]
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {"d": [{"httpCode": test_data["http_code"]}]}

        # Create a screening question
        response = create_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_type=test_data["question_type"],
            screening_question=test_data["screening_question"],
            max_length=test_data["max_length"],
            required=test_data["required"],
        )

        # Ensure that create_screening_question() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "locale": test_data["locale"],
                "jobReqId": test_data["job_requisition_id"],
                "order": test_data["question_number"],
                "questionType": SuccessFactorsQuestionType[
                    test_data["question_type"].upper()
                ].value,
                "questionName": test_data["screening_question"],
                "maxLength": test_data["max_length"],
                "required": test_data["required"],
            }
        )


# Scenario 2: NUMERIC question type
def test_create_screening_question_numeric() -> None:
    """Verify that the `create_screening_question` tool can successfully create a numeric screening
    question."""
    # Define test data:
    test_data: Dict[str, Any] = {
        "job_requisition_id": "67943",
        "screening_question": "How many years of experience do you have?",
        "question_type": "NUMERIC",
        "expected_answer_value": 1.0,
        "expected_direction": "higher",
        "question_weight": 24.0,
        "required": True,
        "disqualifier": False,
        "included_in_score": True,
        "locale": "en_US",
        "response_http_code": 204,
        "question_number": "8",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_new_question_number"
    ) as mock_screening_questions_client:

        # Create a mock for get screening question
        mock_screening_questions_client.return_value = test_data["question_number"]
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"httpCode": test_data["response_http_code"]}]
        }

        # Create a screening question
        response = create_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_type=test_data["question_type"],
            screening_question=test_data["screening_question"],
            expected_answer_value=test_data["expected_answer_value"],
            expected_direction=test_data["expected_direction"],
            question_weight=test_data["question_weight"],
            required=test_data["required"],
            disqualifier=test_data["disqualifier"],
            included_in_score=test_data["included_in_score"],
            locale=test_data["locale"],
        )

        # Ensure that create_screening_question() executed and returned proper values
        assert response
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "locale": test_data["locale"],
                "order": test_data["question_number"],
                "questionType": SuccessFactorsQuestionType[
                    test_data["question_type"].upper()
                ].value,
                "questionName": test_data["screening_question"],
                "expectedAnswerValue": test_data["expected_answer_value"],
                "expectedDir": test_data["expected_direction"],
                "questionWeight": test_data["question_weight"],
                "required": test_data["required"],
                "disqualifier": test_data["disqualifier"],
                "score": test_data["included_in_score"],
            }
        )


# Scenario 3: RATING_SCALES question type
def test_create_screening_question_rating_scale() -> None:
    """Verify that the `create_screening_question` tool can successfully create a rating scales
    screening question."""

    # Define test data:
    test_data: Dict[str, Any] = {
        "job_requisition_id": "67943",
        "question_type": "RATING_SCALES",
        "screening_question": "Rate your communication skills",
        "rating_format": "LIKERT_SCALE",
        "expected_answer_value": "2",
        "expected_direction": "higher",
        "question_weight": 28.0,
        "required": True,
        "disqualifier": False,
        "included_in_score": True,
        "http_code": 204,
        "locale": "en_US",
        "question_number": "8",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_new_question_number"
    ) as mock_screening_questions_client:

        # Create a mock for get screening question
        mock_screening_questions_client.return_value = test_data["question_number"]
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {"d": [{"httpCode": test_data["http_code"]}]}

        # Create a screening question
        response = create_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_type=test_data["question_type"],
            screening_question=test_data["screening_question"],
            rating_format=test_data["rating_format"],
            expected_answer_value=test_data["expected_answer_value"],
            expected_direction=test_data["expected_direction"],
            question_weight=test_data["question_weight"],
            required=test_data["required"],
            disqualifier=test_data["disqualifier"],
            included_in_score=test_data["included_in_score"],
        )

        # Ensure that create_screening_question() executed and returned proper values
        assert response
        assert response.http_code == test_data["http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "locale": test_data["locale"],
                "jobReqId": test_data["job_requisition_id"],
                "order": test_data["question_number"],
                "questionType": SuccessFactorsQuestionType[
                    test_data["question_type"].upper()
                ].value,
                "questionName": test_data["screening_question"],
                "ratingScale": SuccessFactorsRatingScaleFormat[
                    test_data["rating_format"].upper()
                ].value,
                "expectedAnswerValue": test_data["expected_answer_value"],
                "expectedDir": test_data["expected_direction"],
                "questionWeight": test_data["question_weight"],
                "required": test_data["required"],
                "disqualifier": test_data["disqualifier"],
                "score": test_data["included_in_score"],
            }
        )


# Scenario 4: MULTIPLE_CHOICE question type
def test_create_screening_question_multiple_choice() -> None:
    """Verify that the `create_screening_question` tool can successfully create a multiple choice
    screening question."""
    # Define test data:
    test_data: Dict[str, Any] = {
        "job_requisition_id": "67943",
        "screening_question": "Which languages do you speak?",
        "question_type": "MULTIPLE_CHOICE",
        "choice_list": ["match", "123"],
        "question_weight": 29.0,
        "required": True,
        "disqualifier": False,
        "included_in_score": True,
        "locale": "en_US",
        "response_http_code": 204,
        "question_number": "8",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_new_question_number"
    ) as mock_screening_questions_client:

        # Create a mock for get screening question
        mock_screening_questions_client.return_value = test_data["question_number"]
        # Create a mock client instance
        mock_client = MagicMock()
        mock_sap_client.return_value = mock_client
        mock_client.upsert_request.return_value = {
            "d": [{"httpCode": test_data["response_http_code"]}]
        }

        # Create a screening question
        response = create_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_type=test_data["question_type"],
            screening_question=test_data["screening_question"],
            choice_list=test_data["choice_list"],
            question_weight=test_data["question_weight"],
            required=test_data["required"],
            disqualifier=test_data["disqualifier"],
            included_in_score=test_data["included_in_score"],
            locale=test_data["locale"],
        )

        # Ensure that create_screening_question() executed and returned proper values
        assert response.http_code == test_data["response_http_code"]

        # Ensure the API call was made with expected parameters
        mock_client.upsert_request.assert_called_once_with(
            payload={
                "__metadata": {
                    "uri": "JobReqScreeningQuestion",
                    "type": "SFOData.JobReqScreeningQuestion",
                },
                "jobReqId": test_data["job_requisition_id"],
                "locale": test_data["locale"],
                "order": test_data["question_number"],
                "questionType": SuccessFactorsQuestionType[
                    test_data["question_type"].upper()
                ].value,
                "questionName": test_data["screening_question"],
                "choices": {"results": [{"optionLabel": "match"}, {"optionLabel": "123"}]},
                "questionWeight": test_data["question_weight"],
                "required": test_data["required"],
                "disqualifier": test_data["disqualifier"],
                "score": test_data["included_in_score"],
            }
        )


# Scenario 5: Invalid job_requisition_id
def test_create_screening_question_invalid_job_req_id() -> None:
    """Tests that create a screening question fails with an invalid job_requisition_id."""

    test_data: Dict[str, Any] = {
        "job_requisition_id": "679",
        "question_type": "FREE_TEXT",
        "screening_question": "Dummy?",
        "locale": "en_US",
        "max_length": 100,
        "response_http_code": 400,
        "response_message": "An unexpected error occurred.",
        "question_number": "8",
    }

    # Patch `get_sap_successfactors_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_sap_successfactors_client"
    ) as mock_sap_client, patch(
        "agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.create_screening_question.get_new_question_number"
    ) as mock_screening_questions_client:

        # Create a mock for get screening question
        mock_screening_questions_client.return_value = test_data["question_number"]
        # Create a mock client instance
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
        response = create_screening_question(
            job_requisition_id=test_data["job_requisition_id"],
            question_type=test_data["question_type"],
            screening_question=test_data["screening_question"],
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
                "questionType": SuccessFactorsQuestionType[
                    test_data["question_type"].upper()
                ].value,
                "questionName": test_data["screening_question"],
                "maxLength": test_data["max_length"],
            }
        )
