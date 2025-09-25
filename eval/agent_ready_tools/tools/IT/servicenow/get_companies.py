from typing import Any, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class Company:
    """Represents single company object in ServiceNow."""

    company: str
    system_id: str


@dataclass
class CompanyResponse:
    """A response containing the list of companies from ServiceNow."""

    companies: list[Company]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_companies(
    company: Optional[str] = None, system_id: Optional[str] = None
) -> CompanyResponse:
    """
    Gets a list of companies from ServiceNow.

    Args:
        company: The name of the company.
        system_id: The unique system id of the company.

    Returns:
        A list of company records.
    """

    client = get_servicenow_client()

    params: dict[str, Any] = {
        "name": company,
        "sys_id": system_id,
    }

    params = {key: value for key, value in params.items() if value}

    response = client.get_request(entity="core_company", params=params)

    company_list: list[Company] = [
        Company(
            company=companies.get("name", ""),
            system_id=companies.get("sys_id", ""),
        )
        for companies in response["result"]
    ]

    return CompanyResponse(companies=company_list)
