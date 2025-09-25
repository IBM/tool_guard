from fuzzywuzzy import process
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.label_extractor import get_first_en_label
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS

_TOP_N = 10


@dataclass
class CityPicklistOption:
    """Represents a single city option in the country's city picklist."""

    picklist_id: str
    city: str


@dataclass
class CitiesByCountryResult:
    """Represents the best matches to a city query in the country's city picklist."""

    options: list[CityPicklistOption]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def search_cities_by_country(country: str, city_query: str) -> CitiesByCountryResult:
    """
    Searches for the city in the specified country's city picklist.

    Args:
        country: The 3-letter ISO code of the country.
        city_query: The city name to look for in the country's picklist options.

    Returns:
        The best matches to the query in the cities picklist, along with their IDs.
    """
    client = get_sap_successfactors_client()
    response = client.get_picklist_options(picklist_field=f"CITY_{country}")

    # TODO Add support for querying in different languages
    picklist_options: list[CityPicklistOption] = []
    for option in response["d"]["picklistOptions"]["results"]:
        label_en = get_first_en_label(labels=option["picklistLabels"]["results"])
        picklist_options.append(CityPicklistOption(picklist_id=option["id"], city=label_en))

    query_object = CityPicklistOption(picklist_id="", city=city_query)
    top_n_options = [
        option
        for option, score in process.extract(
            query_object,
            picklist_options,
            processor=lambda picklist_option: picklist_option.city,
            limit=_TOP_N,
        )
    ]
    return CitiesByCountryResult(options=top_n_options)
