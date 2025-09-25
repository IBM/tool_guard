from datetime import datetime
import typing

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDate

from agent_ready_tools.apis.workday_soap_services.staff import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class TerminateEmployeeResponse:
    """Represents the response of terminating an employee in Workday."""

    terminate_event_id: str


def _terminate_employee_payload(
    user_id: str, termination_date: str, primary_reason: str
) -> api.StaffingPortTerminateEmployeeInput:
    """
    Returns a payload object of type StaffingPortTerminateEmployeeInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        termination_date: The termination date of the user.
        primary_reason: The primary reason of the termination.

    Returns:
        The termination event id
    """
    dt = datetime.strptime(termination_date, "%Y-%m-%d")
    return api.StaffingPortTerminateEmployeeInput(
        body=api.StaffingPortTerminateEmployeeInput.Body(
            terminate_employee_request=api.TerminateEmployeeRequest(
                terminate_employee_data=api.TerminateEmployeeDataType(
                    employee_reference=api.EmployeeObjectType(
                        id=[api.EmployeeObjectIdtype(value=user_id, type_value="WID")]
                    ),
                    termination_date=XmlDate(year=dt.year, month=dt.month, day=dt.day),
                    terminate_event_data=api.TerminateEventDataType(
                        primary_reason_reference=api.TerminationSubcategoryObjectType(
                            id=[
                                api.TerminationSubcategoryObjectIdtype(
                                    value=primary_reason, type_value="Termination_Subcategory_ID"
                                )
                            ]
                        )
                    ),
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def workday_terminate_employee(
    user_id: str, termination_date: str, primary_reason: str
) -> TerminateEmployeeResponse:
    """
    Terminates a employee in Workday.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.
        termination_date: The termination date of the user.
        primary_reason: The primary reason of the termination, returnrd by get_reference_ids tool.

    Returns:
        The termination event id details.
    """

    @typing.no_type_check
    def xml_to_internal_response(
        output: api.StaffingPortTerminateEmployeeOutput,
    ) -> TerminateEmployeeResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal TerminateEmployeeResponse object.
        """

        try:
            terminate_event_id_node: api.UniqueIdentifierObjectIdtype() = (
                output.body.terminate_employee_event_response.event_reference.id[0].value
            )

        except (AttributeError, IndexError) as e:
            raise ValueError(
                f"unexpected StaffingPortTerminateEmployeeOutput format: {e}\nraw output:\n{output}"
            )

        return TerminateEmployeeResponse(terminate_event_id=terminate_event_id_node)

    client = get_workday_soap_client()
    response = client.terminate_event(
        _terminate_employee_payload(
            user_id=user_id, termination_date=termination_date, primary_reason=primary_reason
        )
    )

    return xml_to_internal_response(response)
