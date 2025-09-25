from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class SalesMarketingResponse:
    """Dataclass representing the sales and marketing info response from Dnb."""

    primary_name: Optional[str] = None  # primaryName
    country: Optional[str] = None  # countryISOAlpha2Code
    marketing_risk_description: Optional[str] = None  # marketingRiskClass
    risk_segment_description: Optional[str] = None  # riskSegment
    composite_risk_score: Optional[int] = None  # triplePlay CompositeRiskScore
    decision_power_score: Optional[int] = None  # decisionPowerScore
    is_decision_hq: Optional[bool] = None  # isDecisionHeadQuarter


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def get_sales_marketing_insight(duns_number: str) -> SalesMarketingResponse:
    """
    Retrieves Data Blocks on sales and marketing insight based on a request for a single DUNS.

    Args:
        duns_number: A single duns number.

    Returns:
        Selected fields in CompanyInfoResponsSalesMarketingResponse from the DnB REST API.
    """

    # Retrieve the DNB client using the helper function.
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)

    query_parameters = {"blockIDs": "salesmarketinginsight_L3_v2"}

    response = client.get_request(
        version="v1",  # The API version.
        category="data",  # The API category.
        endpoint="duns",  # The command endpoint.
        path_parameter=duns_number,  # path parameter
        params=query_parameters,  # query parameters
    )

    return SalesMarketingResponse(
        primary_name=response["organization"]["primaryName"],
        country=response["organization"]["countryISOAlpha2Code"],
        marketing_risk_description=response["organization"]["salesMarketingAssessment"][
            "marketingRiskClass"
        ]["description"],
        risk_segment_description=response["organization"]["salesMarketingAssessment"][
            "materialChange"
        ]["riskSegment"]["description"],
        composite_risk_score=response["organization"]["salesMarketingAssessment"]["triplePlay"][
            "compositeRiskScore"
        ],
        decision_power_score=response["organization"]["salesMarketingAssessment"][
            "decisionPowerScore"
        ],
        is_decision_hq=response["organization"]["salesMarketingAssessment"][
            "isDecisionHeadQuarter"
        ],
    )
