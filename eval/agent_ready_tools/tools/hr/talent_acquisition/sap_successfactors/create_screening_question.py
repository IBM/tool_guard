from http import HTTPStatus
import json
from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_schemas import (
    SuccessFactorsQuestionType,
    SuccessFactorsRatingScaleFormat,
)
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_utility import (
    get_new_question_number,
)
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class CreateScreeningResponse:
    """Represents the result of create_screening_question in SAP SuccessFactors."""

    http_code: int
    message: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def create_screening_question(
    job_requisition_id: str,
    question_type: str,
    screening_question: str,
    question_id: Optional[str] = None,
    rating_format: Optional[str] = None,
    expected_answer_label: Optional[str] = None,
    expected_answer_value: Optional[str] = None,
    max_length: Optional[int] = None,
    expected_direction: Optional[str] = None,
    choice_list: Optional[List[str]] = None,
    question_weight: Optional[float] = None,
    required: Optional[bool] = None,
    disqualifier: Optional[bool] = None,
    included_in_score: Optional[bool] = None,
    locale: str = "en_US",
) -> CreateScreeningResponse:
    """
    Creates a screening question for a job requisition in SAP SuccessFactors.

    Args:
        job_requisition_id: The job requisition id, returned by `get_job_requisitions` tool.
        question_type: The type of the screening question, returned by `get_sap_screening_questions` tool.
        screening_question: The screening question.
        question_id: The unique identifier of the predefined screening question, returned by `get_sap_screening_questions` tool.
        rating_format: The rating scale format for the rating questions.
        expected_answer_label: The label of the expected answer.
        expected_answer_value: The value of the expected answer.
        max_length: The maximum length of the answer text (for free text questions).
        expected_direction: The expected direction of the answer (e.g. higher/lower).
        choice_list: A list of choices for multiple-choice questions.
        question_weight: The weight of the question in scoring.
        required: Whether the question is mandatory.
        disqualifier: Whether the question disqualifies candidates based on the answer.
        included_in_score: Whether the question contributes to the candidate's score.
        locale: The locale for the question text (default: en_US).

    Returns:
        The result from performing the insert operation of screening question.
    """

    client = get_sap_successfactors_client()

    # Validate question_type
    question_types = [question.name for question in SuccessFactorsQuestionType]
    if question_type and question_type.upper() not in question_types:
        raise ValueError(
            f"Question type '{question_type}' is not a valid value. Accepted values are {question_types}"
        )
    question_type_enum = SuccessFactorsQuestionType[question_type]

    # Validate rating_format if required
    if question_type_enum is SuccessFactorsQuestionType.RATING_SCALES:
        if not rating_format:
            raise ValueError("rating_format is required when question_type is RATING_SCALES.")
        valid_rating_formats = [format.name for format in SuccessFactorsRatingScaleFormat]
        if rating_format not in valid_rating_formats:
            raise ValueError(
                f"Rating format '{rating_format}' s not a valid value. Accepted values: {valid_rating_formats}"
            )
        rating_format_enum = SuccessFactorsRatingScaleFormat[rating_format]

    order_response = get_new_question_number(job_req_id=job_requisition_id)
    payload: Dict[str, Any] = {
        "__metadata": {
            "uri": "JobReqScreeningQuestion",
            "type": "SFOData.JobReqScreeningQuestion",
        },
        "jobReqId": job_requisition_id,
        "locale": locale,
        "order": str(order_response),
        "questionType": question_type_enum.value,
        "questionName": screening_question,
    }

    if (
        question_type_enum is SuccessFactorsQuestionType.NUMERIC
        and expected_answer_value is not None
    ):
        payload["expectedAnswerValue"] = expected_answer_value

    if question_type_enum is SuccessFactorsQuestionType.MULTIPLE_CHOICE:
        if choice_list:
            parsed_choices = (
                json.loads(choice_list) if isinstance(choice_list, str) else choice_list
            )
            payload["choices"] = {"results": [{"optionLabel": label} for label in parsed_choices]}

    if question_type_enum is SuccessFactorsQuestionType.RATING_SCALES:
        if rating_format_enum:
            payload["ratingScale"] = rating_format_enum.value
        if expected_answer_value is not None:
            payload["expectedAnswerValue"] = expected_answer_value
        elif expected_answer_label and rating_format_enum:
            payload["expectedAnswerValue"] = rating_format_enum.get_score(expected_answer_label)

    if question_type_enum is SuccessFactorsQuestionType.FREE_TEXT and max_length is not None:
        payload["maxLength"] = max_length

    if question_id is not None:
        payload["questionId"] = question_id
    if expected_direction:
        payload["expectedDir"] = expected_direction
    if question_weight is not None:
        payload["questionWeight"] = question_weight
    if required is not None:
        payload["required"] = required
    if disqualifier is not None:
        payload["disqualifier"] = disqualifier
    if included_in_score is not None:
        payload["score"] = included_in_score

    try:
        response = client.upsert_request(payload=payload)
        response_data = response.get("d", [])
        message = next(
            (res.get("message") for res in response_data if res.get("message")),
            None,
        )
        return CreateScreeningResponse(http_code=response_data[0].get("httpCode"), message=message)

    except HTTPError as e:
        error_response = e.response.json() if e.response else None
        message = (
            error_response.get("d", [])[0].get("message", "None")
            if error_response
            else "An unexpected error occurred."
        )
        return CreateScreeningResponse(
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
