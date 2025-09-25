from http import HTTPStatus
from typing import Any, Dict, List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_schemas import (
    SuccessFactorsQuestionType,
    SuccessFactorsRatingScaleFormat,
)
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class UpdateScreeningQuestionResult:
    """Represents the result of updating a screening question in SAP SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def update_screening_question(
    job_requisition_id: str,
    question_number: str,
    question_type: str,
    question_name: str,
    rating_format: Optional[str] = None,
    expected_answer_label: Optional[str] = None,
    expected_answer_value: Optional[str] = None,
    max_length: Optional[int] = None,
    expected_direction: Optional[str] = None,
    choice_list: Optional[List[str]] = None,
    question_weight: Optional[float] = None,
    required: Optional[bool] = None,
    disqualifier: Optional[bool] = None,
    score: Optional[bool] = None,
    locale: str = "en_US",
) -> UpdateScreeningQuestionResult:
    """
    Updates a candidate screening question for a job requisition in SAP SuccessFactors.

    Args:
        job_requisition_id: The ID of the job requisition, returned by the `get_job_requisitions` tool.
        question_number: The number the screening question to update, returned by the `get_screening_questions` tool.
        question_type: The type of the screening question to update.
        question_name: The name of the screening question to update.
        rating_format: The rating scale format for the question.
        expected_answer_label: The label of the expected answer.
        expected_answer_value: The value of the expected answer.
        max_length: The maximum length of the answer text to update.
        expected_direction: The expected direction of the answer (e.g., higher/lower).
        choice_list: A list of choices for multiple-choice questions to update.
        question_weight: The weight of the question in scoring.
        required: Whether the question is mandatory.
        disqualifier: Whether the question disqualifies candidates based on the answer.
        score: Whether the question contributes to the candidate's score.
        locale: The locale for the question text.

    Returns:
        The result from performing the update operation on the candidate screening question.
    """

    try:
        client = get_sap_successfactors_client()

        # Validate question_type
        valid_question_types = [type.name for type in SuccessFactorsQuestionType]
        if question_type not in valid_question_types:
            raise ValueError(
                f"Invalid question_type '{question_type}'. Accepted values: {valid_question_types}"
            )
        question_type_enum = SuccessFactorsQuestionType[question_type]

        # Validate rating_format if required
        if question_type_enum == SuccessFactorsQuestionType.RATING_SCALES:
            if not rating_format:
                raise ValueError("rating_format is required when question_type is RATING_SCALES.")
            valid_rating_formats = [format.name for format in SuccessFactorsRatingScaleFormat]
            if rating_format not in valid_rating_formats:
                raise ValueError(
                    f"Invalid rating_format '{rating_format}'. Accepted values: {valid_rating_formats}"
                )
            rating_format_enum = SuccessFactorsRatingScaleFormat[rating_format]

        payload: Dict[str, Any] = {
            "__metadata": {
                "uri": "JobReqScreeningQuestion",
                "type": "SFOData.JobReqScreeningQuestion",
            },
            "jobReqId": job_requisition_id,
            "locale": locale,
            "order": question_number,
            "questionType": question_type_enum.value,
            "questionName": question_name,
        }

        if (
            question_type_enum == SuccessFactorsQuestionType.NUMERIC
            and expected_answer_value is not None
        ):
            payload["expectedAnswerValue"] = expected_answer_value

        if question_type_enum == SuccessFactorsQuestionType.MULTIPLE_CHOICE:
            if choice_list:
                payload["choices"] = {"results": [{"optionLabel": label} for label in choice_list]}

        if question_type_enum == SuccessFactorsQuestionType.RATING_SCALES:
            if rating_format_enum:
                payload["ratingScale"] = rating_format_enum.value
            if expected_answer_value is not None:
                payload["expectedAnswerValue"] = expected_answer_value
            elif expected_answer_label and rating_format_enum:
                payload["expectedAnswerValue"] = rating_format_enum.get_score(expected_answer_label)

        if max_length is not None:
            payload["maxLength"] = max_length
        if expected_direction:
            payload["expectedDir"] = expected_direction
        if question_weight is not None:
            payload["questionWeight"] = question_weight
        if required is not None:
            payload["required"] = required
        if disqualifier is not None:
            payload["disqualifier"] = disqualifier
        if score is not None:
            payload["score"] = score

        response = client.upsert_request(payload=payload)
        response_data = response.get("d", [])
        message = next(
            (res.get("message") for res in response_data if res.get("message")),
            None,
        )
        return UpdateScreeningQuestionResult(
            http_code=response_data[0].get("httpCode"), message=message
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response else None
        message = (
            error_response.get("d", [])[0].get("message", "")
            if error_response
            else "An unexpected error occurred."
        )
        return UpdateScreeningQuestionResult(
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
