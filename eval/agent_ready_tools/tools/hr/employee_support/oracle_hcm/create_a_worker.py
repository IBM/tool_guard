from enum import StrEnum
from http import HTTPStatus
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS

# Work email and phone types for a worker in Oracle HCM

EMAIL_TYPE = "W1"
PHONE_TYPE = "W1"


@dataclass
class ActionCodes(StrEnum):
    """Represents the Action codes for creating worker in Oracle HCM."""

    HIRE = "HIRE"
    PENDING_WORKER = "ADD_PEN_WKR"
    CONTINGENT_WORKER = "ADD_CWK"
    NON_WORKER = "ADD_NON_WKR"


@dataclass
class CreateWorkerResponse:
    """Represents the results of worker create operation in Oracle HCM."""

    http_code: int
    message: Optional[str]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def create_a_worker(
    employee_last_name: str,
    employee_first_name: str,
    date_of_birth: str,
    country_code: str,
    legal_employer_name: str,
    business_unit_name: str,
    employee_email_address: str,
    employee_phone_number: str,
    action_code: str,
) -> CreateWorkerResponse:
    """
    Creates a worker in Oracle HCM.

    Args:
        employee_last_name: The last name of the worker.
        employee_first_name: The first name of the worker.
        date_of_birth: The date of birth of the worker in ISO 8601 format (e.g., YYYY-MM-DD).
        country_code: The country code of the worker address.
        legal_employer_name: The name of the legal employer returned by the `get_legal_employer`
            tool.
        business_unit_name: The name of the business unit returned by the
            `get_business_units_oracle` tool.
        employee_email_address: The email address of the worker.
        employee_phone_number: The phone number of the worker.
        action_code: The action code representing the action taken when creating a worker.

    Returns:
        The result from performing the create a worker.
    """

    client = get_oracle_hcm_client()
    action_codes = [action_code.name for action_code in ActionCodes]
    if action_code and action_code.upper() not in action_codes:
        raise ValueError(
            f"Action code type '{action_code}' is not a valid value. Accepted values are {action_codes}"
        )
    payload = {
        "names": [
            {
                "LastName": employee_last_name,
                "FirstName": employee_first_name,
                "LegislationCode": country_code,
            }
        ],
        "DateOfBirth": date_of_birth,
        "workRelationships": [
            {
                "LegalEmployerName": legal_employer_name,
                "assignments": [
                    {
                        "ActionCode": ActionCodes[action_code.upper()].value,
                        "BusinessUnitName": business_unit_name,
                    }
                ],
            }
        ],
        "emails": [{"EmailAddress": employee_email_address, "EmailType": EMAIL_TYPE}],
        "phones": [{"PhoneNumber": employee_phone_number, "PhoneType": PHONE_TYPE}],
    }
    response = client.post_request(entity="workers", payload=payload)
    if response.get("status_code") == HTTPStatus.CREATED:
        return CreateWorkerResponse(http_code=response.get("status_code", ""), message=None)
    else:
        return CreateWorkerResponse(
            http_code=response.get("status_code", ""), message=response.get("message", None)
        )
