from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.tools.common_classes import Currency
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class SalaryBasis:
    """Represents the values for determining an employee's fixed compensation amount each pay
    period."""

    salary_basis_name: str
    salary_basis_id: int
    payment_frequency: str
    "Frequency of the salary basis such as Annually, Monthly, Weekly, or Hourly."
    currency: Currency
    "Currency that salary amount is stored in, such as US Dollar."


@dataclass
class SalaryBasisResponse:
    """Represents the response from retrieving salary bases."""

    salary_bases: List[SalaryBasis]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_salary_bases(currency_code: str) -> SalaryBasisResponse:
    """
    Get salary bases in Oracle HCM.

    Args:
        currency_code: Standardized three-letter abbreviation used to represent a specific currency,
            as defined by the ISO 4217. For example "USD" or "CYN".

    Returns:
        The Oracle deployment's salary bases.
    """

    input_currency = Currency(code=currency_code.upper())

    q_expr = f"InputCurrencyCode='{input_currency.code}'"

    client = get_oracle_hcm_client()
    response = client.get_request("salaryBasisLov", q_expr=q_expr)

    salary_bases: List[SalaryBasis] = [
        SalaryBasis(
            salary_basis_name=result.get("SalaryBasisName"),
            salary_basis_id=result.get("SalaryBasisId"),
            payment_frequency=result.get("FrequencyName"),
            currency=Currency(code=result.get("InputCurrencyCode", "")),
        )
        for result in response["items"]
    ]

    return SalaryBasisResponse(salary_bases=salary_bases)
