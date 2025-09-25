from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client
from agent_ready_tools.utils.date_conversion import iso_8601_to_sap_date
from agent_ready_tools.utils.tool_credentials import SAP_SUCCESSFACTORS_CONNECTIONS


@dataclass
class InitiateOrganizationTransfer:
    """Represents the result of an organization transfer in SAP SuccessFactors."""

    http_code: int
    message: Optional[str] = None


@tool(expected_credentials=SAP_SUCCESSFACTORS_CONNECTIONS)
def initiate_organization_transfer(
    user_id: str,
    start_date: str,
    business_unit: str,
    division: Optional[str] = None,
    department: Optional[str] = None,
) -> InitiateOrganizationTransfer:
    """
    Initiate an organization transfer in SAP SuccessFactors.

    Args:
        user_id: The user's user_id uniquely identifying them within the SuccessFactors API returned
            by the `get_employees_based_on_relationship_with_logged_in_user` tool.
        start_date: The start date to initiate an employee organization transfer in ISO 8601 format
            (e.g., YYYY-MM-DD).
        business_unit: The business_unit_external_code within the SAP SuccessFactors API returned by
            the tool `get_business_units_sap`.
        division: The division_external_code within the SAP SuccessFactors API returned by the tool
            `search_divisions_by_business_unit`.
        department: The department_external_code within the SAP SuccessFactors API returned by the
            tool `search_departments_by_division_and_country`.

    Returns:
        The result from performing the initiate organization transfer employee.
    """
    client = get_sap_successfactors_client()

    payload = {
        "__metadata": {"uri": "EmpJob", "type": "SFOData.EmpJob"},
        "userId": user_id,
        "businessUnit": business_unit,
        "division": division,
        "department": department,
        "startDate": iso_8601_to_sap_date(start_date),
    }
    response = client.upsert_request(payload=payload)
    try:
        http_code = response["d"][0]["httpCode"]
        message = response["d"][0].get("message")
    except AttributeError as e:
        raise ValueError(f"unexpected Output:", e)

    return InitiateOrganizationTransfer(http_code=http_code, message=message)
