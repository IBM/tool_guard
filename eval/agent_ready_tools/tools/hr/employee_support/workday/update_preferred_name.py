from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class UpdatePreferredNameResult:
    """Represents the result of a preferred name update operation in Workday."""

    success: bool


def _update_preferred_name_payload(
    user_id: str,
    first_name: str,
    last_name: str,
    country_code: str,
    middle_name: Optional[str] = None,
) -> api.ChangePreferredNameInput:
    """
    Returns a payload object of type ChangePreferredNameInput filled.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.
        first_name: The user's preferred first name.
        last_name: The user's preferred middle name.
        country_code: The ISO 3166-1 alpha-3 code of the user's country, as specified by the
            `get_user_country_code` tool.
        middle_name: The user's preferred middle name.

    Returns:
        The ChangePreferredNameInput object
    """
    return api.ChangePreferredNameInput(
        body=api.ChangePreferredNameInput.Body(
            change_preferred_name_request=api.ChangePreferredNameRequest(
                change_preferred_name_data=api.ChangePreferredNameBusinessProcessDataType(
                    person_reference=api.RoleObjectType(
                        id=[
                            api.RoleObjectIdtype(
                                value=user_id,
                                type_value="WID",
                            )
                        ]
                    ),
                    name_data=api.PersonNameDetailDataType(
                        first_name=first_name,
                        middle_name=middle_name,
                        last_name=last_name,
                        country_reference=api.CountryObjectType(
                            id=[
                                api.CountryObjectIdtype(
                                    value=country_code, type_value="ISO_3166-1_Alpha-3_Code"
                                )
                            ]
                        ),
                    ),
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def update_preferred_name(
    user_id: str,
    first_name: str,
    last_name: str,
    country_code: str,
    middle_name: Optional[str] = None,
) -> UpdatePreferredNameResult:
    """
    Updates a user's preferred name in Workday.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.
        first_name: The user's preferred first name.
        last_name: The user's preferred middle name.
        country_code: The ISO 3166-1 alpha-3 code of the user's country, as specified by the
            `get_user_country_code` tool.
        middle_name: The user's preferred middle name.

    Returns:
        The result from performing the update to the user's preferred name.
    """
    client = get_workday_soap_client()

    response = client.change_preferred_name(
        _update_preferred_name_payload(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            country_code=country_code,
            middle_name=middle_name,
        )
    )
    success = response.body is not None and response.body.fault is None

    return UpdatePreferredNameResult(success=success)
