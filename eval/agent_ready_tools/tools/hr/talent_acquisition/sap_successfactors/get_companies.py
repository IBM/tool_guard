from http import HTTPStatus
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from requests.exceptions import HTTPError

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class Company:
    """Represents a company in SAP SuccessFactors."""

    external_code: str
    name: str


@dataclass
class CompanyResponse:
    """A list of companies in SAP SuccessFactors."""

    companies: List[Company]
    http_code: Optional[int]
    message: Optional[str]


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def sap_get_companies(
    company_name: Optional[str] = None,
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
) -> CompanyResponse:
    """
    Retrieves companies from SAP SuccessFactors.

    Args:
        company_name: Name of the company to be retrieved .
        limit: The maximum number of companies records to retrieve.
        skip: The number of companies records to skip.

    Returns:
        A structured list of companies.
    """
    try:
        client = get_sap_successfactors_client()

        # filter expression if company_name is provided
        filter_expr = f"name eq '{company_name}'" if company_name else None
        params = {"$select": "externalCode,name", "$top": limit, "$skip": skip}

        response = client.get_request(entity="FOCompany", filter_expr=filter_expr, params=params)

        results = response.get("d", {}).get("results", [])
        companies = [
            Company(external_code=item.get("externalCode", ""), name=item.get("name", ""))
            for item in results
        ]
        return CompanyResponse(companies=companies, http_code=None, message=None)
    except HTTPError as e:
        error_response = e.response.json() if e.response is not None else {}
        message = (
            error_response.get("error", {}).get("message", {}).get("value", "")
            if error_response
            else "An unexpected error occurred."
        )
        return CompanyResponse(
            companies=[],
            http_code=(
                e.response.status_code
                if e.response and e.response.status_code
                else HTTPStatus.INTERNAL_SERVER_ERROR.value
            ),
            message=message,
        )
