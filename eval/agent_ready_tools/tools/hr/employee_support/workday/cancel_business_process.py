import typing

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.integration import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class CancelBusinessProcessResponse:
    """Represents the response from cancel Business process request in Workday."""

    event_id: str


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def cancel_business_process(
    event_id: str,
) -> api.IntegrationsPortCancelBusinessProcessOutput:
    """
    Cancel a business process event.

    Args:
        event_id: The event's id uniquely identifying them within the Workday API.

    Returns:
        The canceled event  info.
    """
    client = get_workday_soap_client()
    payload = api.IntegrationsPortCancelBusinessProcessInput(
        body=api.IntegrationsPortCancelBusinessProcessInput.Body(
            cancel_business_process_request=api.CancelBusinessProcessRequest(
                event_reference=api.ActionEventObjectType(
                    id=[api.ActionEventObjectIdtype(type_value="WID", value=event_id)]
                )
            )
        )
    )

    xml_response = client.post_cancel_business_process_request(payload)

    # TODO Investigate whether this logic can be cleaned up/simplified
    @typing.no_type_check
    def xml_to_internal_response(
        output: api.IntegrationsPortCancelBusinessProcessOutput,
    ) -> CancelBusinessProcessResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal CancelBusinessProcessResponse object.
        """

        try:
            return CancelBusinessProcessResponse(
                event_id=output.body.cancel_business_process_response.event_reference.id[0].value
            )
        except (IndexError, AttributeError) as e:
            raise ValueError(
                f"unexpected post_cancel_business_process_request format: {e}\nraw output:\n{output}"
            )

    return xml_to_internal_response(xml_response)
