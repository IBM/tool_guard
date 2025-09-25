from typing import List

from fuzzywuzzy import process
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS

_TOP_N = 10


@dataclass
class StatePicklistOption:
    """Represents a single state option in the country's state picklist."""

    picklist_id: str
    state: str


@dataclass
class StatesByCountryResult:
    """Represents the best matches to a state query in the country's state picklist."""

    options: List[StatePicklistOption]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_states_by_country(country: str, state_query: str) -> StatesByCountryResult:
    """
    Searches for the state in the specified country's state picklist.

    Args:
        country: The 3-letter ISO code of the country.
        state_query: The state name to look for in the country's picklist options.

    Returns:
        The best matches to the query in the state picklist, along with their IDs.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field=f"STATE_{country}")

    # TODO Add support for querying in different languages
    picklist_options: List[StatePicklistOption] = []
    for option in response["d"]["picklistOptions"]["results"]:
        label_en = get_first_en_label(labels=option["picklistLabels"]["results"])
        picklist_options.append(StatePicklistOption(picklist_id=option["id"], state=label_en))

    query_object = StatePicklistOption(picklist_id="", state=state_query)
    top_n_options = [
        option
        for option, score in process.extract(
            query_object, picklist_options, processor=lambda opt: opt.state, limit=_TOP_N
        )
    ]
    return StatesByCountryResult(options=top_n_options)
