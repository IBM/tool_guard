from datetime import datetime
from decimal import Decimal
import typing

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDate

from agent_ready_tools.apis.workday_soap_services.compensation import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class CompensationChangeResponse:
    """Represents the response for a Compensation Change Request in Workday."""

    request_id: str


def _request_compensation_change_payload(
    user_id: str, reason_id: str, effective_date: str, new_compensation_amount: str
) -> api.RequestCompensationChangeInput:
    """
    Returns a payload object of type RequestCompensationChangeInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        reason_id: The id for the reason the compensation request is being made.
        effective_date: The start date for the requested compensation change.
        new_compensation_amount: The requested compensation amount.

    Returns:
        The RequestCompensationChangeInput object
    """
    dt = datetime.strptime(effective_date, "%Y-%m-%d")
    formatted_new_compensation_amount = "{:.2f}".format(float(new_compensation_amount))
    return api.RequestCompensationChangeInput(
        body=api.RequestCompensationChangeInput.Body(
            request_compensation_change_request=api.RequestCompensationChangeRequest(
                request_compensation_change_data=api.RequestCompensationChangeDataType(
                    employee_reference=api.EmployeeObjectType(
                        id=[api.EmployeeObjectIdtype(value=user_id, type_value="WID")]
                    ),
                    compensation_change_date=XmlDate(year=dt.year, month=dt.month, day=dt.day),
                    compensation_change_data=api.CompensationChangeDataType(
                        reason_reference=api.EventClassificationSubcategoryObjectType(
                            id=[
                                api.EventClassificationSubcategoryObjectIdtype(
                                    value=reason_id,
                                    type_value="Event_Classification_Subcategory_ID",
                                )
                            ]
                        ),
                        pay_plan_data=api.ProposedBasePayPlanAssignmentContainerDataType(
                            pay_plan_sub_data=[
                                api.ProposedBasePayPlanAssignmentDataType(
                                    amount=Decimal(formatted_new_compensation_amount)
                                )
                            ],
                            replace=True,
                        ),
                    ),
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def request_compensation_change(
    user_id: str, reason_id: str, effective_date: str, new_compensation_amount: str
) -> CompensationChangeResponse:
    """
    Creates an hourly or salary compensation change request for a user in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        reason_id: The id for the reason the compensation request is being made.
        effective_date: The start date for the requested compensation change.
        new_compensation_amount: The requested compensation amount.

    Returns:
        The request response.
    """

    @typing.no_type_check
    def xml_to_internal_response(
        output: api.RequestCompensationChangeOutput,
    ) -> CompensationChangeResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal CompensationChangeResponse object.
        """

        try:
            request_compensation_event_reference_node: api.UniqueIdentifierObjectType() = (
                output.body.request_compensation_change_response.request_compensation_change_event_reference
            )
        except AttributeError as e:
            raise ValueError(
                f"unexpected RequestCompensationChangeOutput format: {e}\nraw output:\n{output}"
            )

        try:
            request_id: str = request_compensation_event_reference_node.id[0].value
            assert request_id, f"No request_id returned in RequestCompensationChangeOutput"
        except (AttributeError, IndexError, AssertionError) as e:
            raise ValueError(
                f"unexpected RequestCompensationChangeOutput format: {e}\nraw output:\n{output}"
            )

        return CompensationChangeResponse(request_id=request_id)

    client = get_workday_soap_client()
    response = client.request_compensation_change(
        _request_compensation_change_payload(
            user_id=user_id,
            reason_id=reason_id,
            effective_date=effective_date,
            new_compensation_amount=new_compensation_amount,
        )
    )

    return xml_to_internal_response(response)
