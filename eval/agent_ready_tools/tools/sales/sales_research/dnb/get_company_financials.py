from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import DNBEntitlements
from agent_ready_tools.clients.dnb_client import get_dnb_client
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_schemas import ErrorResponse
from agent_ready_tools.tools.sales.sales_research.dnb.dnb_utils import process_dnb_error
from agent_ready_tools.utils.tool_credentials import DNB_SALES_CONNECTIONS


@dataclass
class CompanyFinancialsResponse:
    """Dataclass representing the company latest financials response from DnB."""

    name: Optional[str] = None  # mapped from "primaryName"
    country: Optional[str] = None  # mapped from "countryISOAlpha2Code"
    financial_statement_duration: Optional[str] = None  # mapped from "financialStatementDuration"
    financial_statement_start: Optional[str] = None  # mapped from "financialStatementFromDate"
    financial_statement_end: Optional[str] = None  # mapped from "financialStatementToDate"
    currency: Optional[str] = None  # mapped from "currency"
    units: Optional[str] = None  # mapped from "units"
    sales_revenue: Optional[float] = None  # mapped from "salesRevenue"
    operating_profit: Optional[float] = None  # mapped from "operatingProfit"
    profit_before_taxes: Optional[float] = None  # mapped from "profitBeforeTaxes"
    quick_ratio: Optional[float] = None  # mapped from "quickRatio"
    total_assets: Optional[float] = None  # mapped from "totalAssets"
    total_liabilities: Optional[float] = None  # mapped from "totalLiabilities"


@tool(expected_credentials=DNB_SALES_CONNECTIONS)
def get_company_financials(duns_number: str) -> Optional[CompanyFinancialsResponse] | ErrorResponse:
    """
    Retrieve financial details for a company using its DUNS number.

    Args:
        duns_number: A duns number.

    Returns:
        A list of CompanyFinancialsResponses object from the DnB REST API. Each object
        contains:
            - name (str): Single name by which the organization is primarily known or identified.
            - country (str): The two-letter country code
            - financial_statement_duration (str): The period of the financial statement expressed as a time interval.
            - financial_statement_start (str): The period of the financial statement expressed as a time interval.
            - financial_statement_end (str):  The date when the accounting period of the Latest Financials' financial statement ended.
            - currency (str): The currency in which the figures in the Latest Financials' financial statement are stated.
            - units (str):  The unit size (e.g., units, thousands, millions) in which the figures in the Latest Financials' financial statement are stated.
            - sales_revenue (str):  The income generated from the sale of goods and services for the Latest Financials. This is dependent upon the volume of a product sold and the price of the product shown net of returns, allowances and discounts. Also known as Turnover.
            - operating_profit (float): The profit from business operations after operating expenses but before deduction of interest and taxes for the Latest Financials.
            - profit_before_taxes (float):  The Latest Financials' disclosed profit before tax, which will reflect deductions for all operating and non-operating costs.
            - quick_ratio (float): A ratio for the Latest Financials that measures the extent to which the organization can cover its current liabilities with those current assets that are readily convertible to cash.
            - total_assets (float): The combined value of Current Assets and Total Long Term Assets for the Latest Financials
            - total_liabilities (float):  The combined value of Total Long Term Liabilities and Total Current Liabilities for the Latest Financials. This is therefore the total value of all claims on the financial resources of the organization and obligations of payment.
    """

    # Retrieve the DNB client using the helper function.
    client = get_dnb_client(entitlement=DNBEntitlements.SALES)
    # Hard code block_id for company financials specifically
    block_id = "companyfinancials_L1_v3"

    response = client.get_request(
        version="v1",  # The API version.
        category="data",  # The API category.
        endpoint="duns",  # The command endpoint.
        path_parameter=duns_number,  # path parameters
        params={"blockIDs": block_id},  # block_id parameter
    )

    cf_organization = response.get("organization", None)
    if cf_organization is not None:
        cf_latest_financials = cf_organization.get("latestFiscalFinancials", {})
        cf_latest_financials_overview = cf_latest_financials.get("overview", {})
    else:
        cf_latest_financials = {}
        cf_latest_financials_overview = {}

    # Check if we have an error in the response.
    api_url = "https://plus.dnb.com/v1/data/duns"
    url_params = {"blockIDs": block_id}
    error_response = process_dnb_error(response, api_url, url_params)

    # Construct and append the CompanyFinancialsResponse object if cf_organization is not None.
    # Otherwise return error_response
    if cf_organization:
        return CompanyFinancialsResponse(
            name=cf_organization.get("primaryName", None),
            country=cf_organization.get("countryISOAlpha2Code", None),
            financial_statement_duration=cf_latest_financials.get(
                "financialStatementDuration", None
            ),
            financial_statement_start=cf_latest_financials.get("financialStatementFromDate", None),
            financial_statement_end=cf_latest_financials.get("financialStatementToDate", None),
            currency=cf_latest_financials.get("currency", None),
            units=cf_latest_financials.get("units", None),
            sales_revenue=cf_latest_financials_overview.get("salesRevenue", None),
            operating_profit=cf_latest_financials_overview.get("operatingProfit", None),
            profit_before_taxes=cf_latest_financials_overview.get("profitBeforeTaxes", None),
            quick_ratio=cf_latest_financials_overview.get("quickRatio", None),
            total_assets=cf_latest_financials_overview.get("totalAssets", None),
            total_liabilities=cf_latest_financials_overview.get("totalLiabilities", None),
        )
    else:
        return error_response
