from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.tools.hr.talent_acquisition.sap_successfactors.sap_successfactors_schemas import (
    Message,
)
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class StatePicklistOption:
    """Represents a state (province) option in the state picklist."""

    picklist_id: str
    state: str


@dataclass
class StateSearchResult:
    """List of states from SAP SuccessFactors."""

    options: List[StatePicklistOption]
    http_code: Optional[int]
    message: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_states(
    state: Optional[str] = None,
    country: Optional[str] = None,
    top: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> StateSearchResult:
    """
    Retrieves state options from SAP SuccessFactors using the PicklistLabel endpoint.

    Args:
        state: The state name to look for in the country's picklist options.
        country: The 3-letter ISO code of the country.
        top: Number of records to retrieve.
        skip: Number of records to skip (for pagination).

    Returns:
        A list of state (province) options including their picklist IDs and labels. If an error occurs, includes HTTP status code and error message.
    """

    client = get_sap_successfactors_client()

    filter_query = f"picklistOption/picklist/picklistId eq 'state' and locale eq 'en_US'"
    if state:
        filter_query += f" and label eq '{state}'"
    if country:
        filter_query += f" and picklistOption/parentPicklistOption/externalCode eq '{country}'"

    query_params = {
        "$top": top,
        "$skip": skip,
    }
    try:
        response = client.get_request(
            entity="PicklistLabel",
            params=query_params,
            filter_expr=filter_query,
            select_expr="label,picklistOption/id",
            expand_expr="picklistOption/picklist",
        )

        results = response.get("d", {}).get("results", [])
        if not results:
            return StateSearchResult(
                options=[],
                http_code=response.get("status_code", HTTPStatus.OK),
                message=Message.SEARCH_STATE_MESSAGE,
            )
        picklist_options: List[StatePicklistOption] = []

        for item in results:
            label = item.get("label")
            option_id = item.get("picklistOption", {}).get("id")

            if label and option_id:
                picklist_options.append(StatePicklistOption(picklist_id=option_id, state=label))

        http_code = response.get("status_code", HTTPStatus.OK)
        return StateSearchResult(options=picklist_options, http_code=http_code, message=None)

    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else None
        message = (
            error_response.get("error", {}).get("message", {}).get("value", None)
            if error_response
            else None
        )
        if not message:
            message = "An unexpected error occurred."

        return StateSearchResult(
            options=[],
            http_code=(
                e.response.status_code if e.response else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
