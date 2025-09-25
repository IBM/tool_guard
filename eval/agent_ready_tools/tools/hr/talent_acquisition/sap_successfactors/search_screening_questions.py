from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class QuestionDetails:
    """Represents a single predefined screening question."""

    question_id: Optional[str]
    question_category: Optional[str]
    question_source: Optional[str]
    question_type: Optional[str]
    question_name: Optional[str]


@dataclass
class ScreeningQuestionResponse:
    """List of predefined screening questions."""

    questions: List[QuestionDetails]
    http_code: Optional[int]
    message: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_sap_screening_questions(
    top: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> ScreeningQuestionResponse:
    """
    Retrieves predefined screening questions from SAP SuccessFactors.

    Args:
        top: The maximum number of screening questions to retrieve in a single API call. Defaults to 10. Use this to control the size of the result set.
        skip: The number of screening questions to skip for pagination purposes. Defaults to 0.

    Returns:
        The list of predefined screening questions.
    """

    questions: List[QuestionDetails] = []
    client = get_sap_successfactors_client()

    params = {"$top": top, "$skip": skip}
    try:
        response = client.get_request(
            entity="JobReqQuestion",
            params=params,
        )

        result = response.get("d", {}).get("results", [])
        # if results is empty
        if not result:
            return ScreeningQuestionResponse(
                questions=[],
                http_code=response.get("status_code", HTTPStatus.OK),
                message="No screening questions data returned from API",
            )

        questions = [
            QuestionDetails(
                question_id=item.get("questionId", ""),
                question_category=item.get("questionCategory", ""),
                question_source=item.get("questionSource", ""),
                question_type=item.get("questionType", ""),
                question_name=item.get("questionName", ""),
            )
            for item in result
        ]

        return ScreeningQuestionResponse(
            questions=questions,
            http_code=response.get("status_code", HTTPStatus.OK),
            message=None,
        )

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return ScreeningQuestionResponse(
            questions=[],
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
