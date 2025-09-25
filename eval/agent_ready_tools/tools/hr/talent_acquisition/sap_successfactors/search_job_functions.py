from http import HTTPStatus
from typing import List, Optional

from fuzzywuzzy import process
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS

_TOP_N = 10
_MIN_SCORE_THRESHOLD = 70


@dataclass
class JobFunctionOption:
    """Represents a single job function option."""

    picklist_id: str
    job_function: str


@dataclass
class JobFunctionsResponse:
    """Represents the best matches to an employee type query."""

    options: List[JobFunctionOption]
    http_code: Optional[int]
    error_message: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_job_functions(job_function_query: Optional[str] = None) -> JobFunctionsResponse:
    """
    Retrieves all job functions from the SAP SuccessFactors picklist.

    Args:
        job_function_query: The job function from SAP SuccessFactors.

    Returns:
        A list of job functions with their corresponding picklist IDs.
    """
    try:
        client = get_sap_successfactors_client()
        response = client.get_picklist_options(picklist_field="jobFunction")

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )
        return JobFunctionsResponse(
            options=[],
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            error_message=message if message else "An unexpected error occurred.",
        )

    picklist_options: List[JobFunctionOption] = []
    response_data = response.get("d", {}).get("picklistOptions", {}).get("results", [])

    if response_data:
        for option in response_data:
            labels = option.get("picklistLabels", {}).get("results", [])
            label_en = get_first_en_label(labels=labels)
            if label_en:
                picklist_options.append(
                    JobFunctionOption(picklist_id=option.get("id", None), job_function=label_en)
                )

        if job_function_query:
            label_to_option = {opt.job_function: opt for opt in picklist_options}
            matches = process.extract(job_function_query, label_to_option.keys(), limit=_TOP_N)

            # Filter out weak matches
            filtered_matches = [
                (label, score) for label, score in matches if score >= _MIN_SCORE_THRESHOLD
            ]
            top_n_options = [label_to_option[label] for label, score in filtered_matches]
        else:
            top_n_options = picklist_options[:_TOP_N]

        http_code = response.get("status_code", HTTPStatus.OK)
        return JobFunctionsResponse(options=top_n_options, http_code=http_code, error_message=None)

    else:
        return JobFunctionsResponse(
            options=[],
            http_code=response.get("status_code", HTTPStatus.OK),
            error_message="Search job function query data does not exist.",
        )
