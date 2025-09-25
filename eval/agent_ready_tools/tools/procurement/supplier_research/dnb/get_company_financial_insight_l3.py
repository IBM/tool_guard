from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.utils.tool_credentials import DNB_PROCUREMENT_CONNECTIONS


@dataclass
class CompanyFinancialInsight:
    """Represents company financial insight of a company."""

    duns_number: str
    accounts_payable: Optional[float] = None
    accounts_receivable: Optional[float] = None
    capital_stock: Optional[int] = None
    cash_and_liquid_asset: Optional[int] = None
    cost_of_sales: Optional[float] = None
    gross_profit: Optional[float] = None
    net_income: Optional[float] = None
    ebitda: Optional[float] = None
    quick_ratio: Optional[float] = None
    current_ratio: Optional[float] = None
    operating_profit: Optional[float] = None
    sales_revenue: Optional[int] = None
    total_liabilities: Optional[int] = None
    long_term_debt: Optional[int] = None
    financial_statement_to_date: Optional[str] = None
    financial_statement_from_date: Optional[str] = None
    financial_statement_duration: Optional[str] = None
    is_audited: Optional[bool] = None
    is_fiscal: Optional[bool] = None
    is_final: Optional[bool] = None
    is_signed: Optional[bool] = None
    accountant_name: Optional[str] = None
    accountant_opinions: Optional[str] = None

    sales_revenue_prev: Optional[str] = None
    financial_statement_to_date_prev: Optional[str] = None
    gross_profit_prev: Optional[float] = None
    operating_profit_prev: Optional[float] = None
    net_income_prev: Optional[str] = None


@tool(expected_credentials=DNB_PROCUREMENT_CONNECTIONS)
def dnb_get_company_financial_insight_l3(duns_number: str) -> ToolResponse[CompanyFinancialInsight]:
    """
    Returns the company's financial insight.

    Args:
        duns_number: The company's duns number.

    Returns:
        The level 3 financial insight.
    """
    try:
        client = get_dnb_client(entitlement=DNBEntitlements.PROCUREMENT)
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"blockIDs": "companyfinancials_L3_v1"}
    response = client.get_request("v1", "data", "duns/" + duns_number, params=params)
    if "error" in response and "errorMessage" in response["error"]:
        return ToolResponse(success=False, message=response["error"]["errorMessage"])

    org = response.get("organization")

    if org is None or "latestFinancials" not in org or "overview" not in org["latestFinancials"]:
        return ToolResponse(
            success=False, message="The information is not available for this company"
        )

    result = CompanyFinancialInsight(duns_number=org["duns"])

    result.accounts_payable = org["latestFinancials"]["overview"].get("accountsPayable")
    result.accounts_receivable = org["latestFinancials"]["overview"].get("accountsReceivable")
    result.capital_stock = org["latestFinancials"]["overview"].get("capitalStock")
    result.cash_and_liquid_asset = org["latestFinancials"]["overview"].get("cashAndLiquidAssets")
    result.cost_of_sales = org["latestFinancials"]["overview"].get("costOfSales")
    result.gross_profit = org["latestFinancials"]["overview"].get("grossProfit")
    result.net_income = org["latestFinancials"]["overview"].get("netIncome")
    result.ebitda = org["latestFinancials"]["overview"].get("ebitda")
    result.quick_ratio = org["latestFinancials"]["overview"].get("quickRatio")
    result.current_ratio = org["latestFinancials"]["overview"].get("currentRatio")
    result.operating_profit = org["latestFinancials"]["overview"].get("operatingProfit")
    result.sales_revenue = org["latestFinancials"]["overview"].get("salesRevenue")
    result.total_liabilities = org["latestFinancials"]["overview"].get("totalLiabilities")
    result.long_term_debt = org["latestFinancials"]["overview"].get("longTermDebt")
    result.financial_statement_to_date = org["latestFinancials"].get("financialStatementToDate")
    result.financial_statement_from_date = org["latestFinancials"].get("financialStatementFromDate")
    result.financial_statement_duration = org["latestFinancials"].get("financialStatementDuration")
    result.is_fiscal = org["latestFinancials"].get("isFiscal")
    result.is_audited = org["latestFinancials"].get("isAudited")
    result.is_final = org["latestFinancials"].get("isFinal")
    result.is_signed = org["latestFinancials"].get("isSigned")
    result.accountant_name = org["latestFinancials"].get("accountantName")
    if "accountantOpinions" in org["latestFinancials"]:
        result.accountant_opinions = " ".join(
            [o.get("description", "") for o in org["latestFinancials"]["accountantOpinions"]]
        )
    if len(org["previousFinancials"]) > 0:
        result.operating_profit_prev = org["previousFinancials"][0]["overview"].get(
            "operatingProfit"
        )
        result.net_income_prev = org["previousFinancials"][0]["overview"].get("netIncome")
        result.sales_revenue_prev = org["previousFinancials"][0]["overview"].get("salesRevenue")
        result.gross_profit_prev = org["previousFinancials"][0]["overview"].get("grossProfit")
        result.financial_statement_to_date_prev = org["previousFinancials"][0].get(
            "financialStatementToDate"
        )

    return ToolResponse(success=True, message="The data was successfully retrieved", content=result)
