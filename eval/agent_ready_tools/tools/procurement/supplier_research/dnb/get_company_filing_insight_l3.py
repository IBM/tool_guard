from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class FilingEventInsight:
    """Represents a financial strength of a company."""

    duns_number: str
    has_bankruptcy: Optional[bool] = None
    has_judgement: Optional[bool] = None
    has_control_change: Optional[bool] = None
    has_liquidation: Optional[bool] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_filing_insight_l3(duns_number: str) -> ToolResponse[FilingEventInsight]:
    """
    Returns the company's filing insight.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 3 filing insight.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "eventfilings_L3_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    org = response.get("organization")

    if org is None or "legalEvents" not in org:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = FilingEventInsight(duns_number=org["duns"])

    result.has_bankruptcy = org["legalEvents"].get("hasBankruptcy")
    result.has_judgement = org["legalEvents"].get("hasJudgments")
    result.has_liquidation = org["legalEvents"].get("hasLiquidation")
    result.has_control_change = org.get("significantEvents", {}).get(
        "hasControlChange",
    )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
