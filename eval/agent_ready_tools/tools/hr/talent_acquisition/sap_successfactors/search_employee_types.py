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


@dataclass
class EmployeeTypePicklistOption:
    """Represents a single employee type option."""

    picklist_id: str
    employee_type: str


@dataclass
class EmployeeTypeSearchResult:
    """Represents the best matches to an employee type query."""

    options: List[EmployeeTypePicklistOption]
    http_code: Optional[int] = None
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_employee_type(employee_type_query: Optional[str] = None) -> EmployeeTypeSearchResult:
    """
    Searches for employee types in the employType picklist using fuzzy matching.

    Args:
        employee_type_query: The employee type name to look for.

    Returns:
        A list of employee types and their corresponding IDs.
    """
    try:
        client = get_sap_successfactors_client()
        response = client.get_picklist_options(picklist_field="employType")
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )
        return EmployeeTypeSearchResult(
            options=[],
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )

    picklist_options: List[EmployeeTypePicklistOption] = []
    for option in response["d"]["picklistOptions"]["results"]:
        labels = option.get("picklistLabels", {}).get("results", [])
        label_en = get_first_en_label(labels=labels)
        if label_en:
            picklist_options.append(
                EmployeeTypePicklistOption(picklist_id=option["id"], employee_type=label_en)
            )

    if employee_type_query:
        query_object = EmployeeTypePicklistOption(picklist_id="", employee_type=employee_type_query)
        top_n_options = [
            option
            for option, score in process.extract(
                query_object,
                picklist_options,
                processor=lambda opt: opt.employee_type,
                limit=_TOP_N,
            )
        ]
    else:
        top_n_options = picklist_options[:_TOP_N]

    return EmployeeTypeSearchResult(options=top_n_options)
