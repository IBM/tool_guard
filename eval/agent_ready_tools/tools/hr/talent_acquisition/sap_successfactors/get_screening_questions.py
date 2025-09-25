from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class ScreeningQuestion:
    """Represents a single screening question with available choices."""

    text: str
    type: Optional[str] = None
    order: Optional[str] = None
    description: Optional[str] = None
    choices: Optional[List[str]] = None


@dataclass
class ScreeningQuestionsResponse:
    """List of screening questions for a given job requisition."""

    questions: List[ScreeningQuestion]
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def get_screening_questions(job_req_id: str) -> ScreeningQuestionsResponse:
    """
    Retrieves screening questions for a job requisition from SAP SuccessFactors.

    Args:
        job_req_id: The id of the job requisition from which screening questions are to be retrieved, returned by the tool `get_all_job_requisitions`.

    Returns:
        The list of screening questions.
    """

    try:
        client = get_sap_successfactors_client()

        response = client.get_request(
            entity="JobReqScreeningQuestion",
            filter_expr=f"jobReqId eq '{job_req_id}'",
            expand_expr="choices",
        )

        result = response.get("d", {}).get("results", [])

        questions: List[ScreeningQuestion] = []

        for item in result:
            raw_choices = item.get("choices", {}).get("results", [])

            choices = [
                choice["optionLabel"]
                for choice in raw_choices
                if isinstance(choice, dict) and "optionLabel" in choice
            ]

            questions.append(
                ScreeningQuestion(
                    order=item.get("order", ""),
                    text=item.get("questionName", ""),
                    type=item.get("questionType", ""),
                    description=item.get("questionDescription", ""),
                    choices=choices,
                )
            )

        return ScreeningQuestionsResponse(questions=questions)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )

        return ScreeningQuestionsResponse(
            questions=[],
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
