from typing import List

from fuzzywuzzy import process
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS

_TOP_N = 10


@dataclass
class ProvincePicklistOption:
    """Represents a single province option in the country's province picklist."""

    picklist_id: str
    province: str


@dataclass
class ProvincesByCountryResult:
    """Represents the best matches to a province query in the country's province picklist."""

    options: List[ProvincePicklistOption]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_provinces_by_country(country: str, province_query: str) -> ProvincesByCountryResult:
    """
    Searches for the province in the specified country's province picklist.

    Args:
        country: The 3-letter ISO code of the country.
        province_query: The province name to look for in the country's picklist options.

    Returns:
        The best matches to the query in the province picklist, along with their IDs.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field=f"PROVINCE_{country}")

    # TODO Add support for querying in different languages
    picklist_options: List[ProvincePicklistOption] = []
    for option in response["d"]["picklistOptions"]["results"]:
        label_en = get_first_en_label(labels=option["picklistLabels"]["results"])
        picklist_options.append(ProvincePicklistOption(picklist_id=option["id"], province=label_en))

    query_object = ProvincePicklistOption(picklist_id="", province=province_query)
    top_n_options = [
        option
        for option, score in process.extract(
            query_object, picklist_options, processor=lambda opt: opt.province, limit=_TOP_N
        )
    ]
    return ProvincesByCountryResult(options=top_n_options)
