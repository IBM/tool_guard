from datetime import date
import typing

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass
from xsdata.models.datatype import XmlDate

from agent_ready_tools.apis.workday_soap_services.staff import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class InitiatePromotionResponse:
    """Represents the response from the change job request in Workday."""

    event_id: str


def _initiate_promotion_payload(
    user_id: str, change_reason_id: str, effective_date: date, position_id: str
) -> api.StaffingPortChangeJobInput:
    """
    Returns a payload object of type StaffingPortChangeJobInput filled.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        change_reason_id: The change reason id uniquely identifying them within the Workday API.
        effective_date: Date to take place of the change.
        position_id: The position id uniquely identifying them within the Workday API.

    Returns:
        The StaffingPortChangeJobInput object
    """
    return api.StaffingPortChangeJobInput(
        body=api.StaffingPortChangeJobInput.Body(
            change_job_request=api.ChangeJobRequest(
                change_job_data=api.ChangeJobDataType(
                    worker_reference=api.WorkerObjectType(
                        id=[api.WorkerObjectIdtype(type_value="WID", value=user_id)]
                    ),
                    position_reference=api.PositionElementObjectType(
                        id=[api.PositionElementObjectIdtype(type_value="WID", value=position_id)]
                    ),
                    effective_date=XmlDate(
                        effective_date.year, effective_date.month, effective_date.day
                    ),
                    change_job_detail_data=api.ChangeJobDetailDataType(
                        reason_reference=api.ChangeJobSubcategoryObjectType(
                            id=[
                                api.ChangeJobSubcategoryObjectIdtype(
                                    type_value="WID", value=change_reason_id
                                )
                            ],
                            descriptor="Promotion",
                        )
                    ),
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def initiate_promotion(
    user_id: str, change_reason_id: str, effective_date: date, position_id: str
) -> InitiatePromotionResponse:
    """
    Initiate user's promotion in Workday.

    Args:
        user_id: The user's id uniquely identifying them within the Workday API.
        change_reason_id: The change reason id uniquely identifying them within the Workday API.
        effective_date: Date to take place of the change.
        position_id: The position id uniquely identifying them within the Workday API.

    Returns:
        The event created info.
    """
    client = get_workday_soap_client()
    xml_response = client.post_job_change(
        _initiate_promotion_payload(
            user_id=user_id,
            change_reason_id=change_reason_id,
            effective_date=effective_date,
            position_id=position_id,
        )
    )

    # TODO Investigate whether this logic can be cleaned up/simplified
    @typing.no_type_check
    def xml_to_internal_response(
        output: api.StaffingPortChangeJobOutput,
    ) -> InitiatePromotionResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal ChangeJobResponse object.
        """

        try:
            return InitiatePromotionResponse(
                event_id=output.body.change_job_response.event_reference.id[0].value
            )
        except (IndexError, AttributeError) as e:
            raise ValueError(f"unexpected post_job_change format: {e}\nraw output:\n{output}")

    return xml_to_internal_response(xml_response)
