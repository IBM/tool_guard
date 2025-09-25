from decimal import Decimal
import typing
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.integrations import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class CompensationChangeReasonReference:
    """Represents a reason reference for requesting a compensation change."""

    reference: str


@dataclass
class CompensationChangeReasonResponse:
    """Represents the response from getting the reason references for requesting a compensation
    change."""

    references: list[CompensationChangeReasonReference]


def _get_compensation_change_reasons_payload(
    count: Optional[Decimal] = None,
) -> api.GetReferencesInput:
    """
    Returns a payload object of type GetReferencesInput filled.

    Args:
        count: The maximum number of events to return.

    Returns:
        The GetReferencesInput object
    """
    return api.GetReferencesInput(
        body=api.GetReferencesInput.Body(
            get_references_request=api.GetReferencesRequest(
                request_criteria=api.GetReferencesRequestCriteriaType(
                    reference_id_type="General_Event_Subcategory_ID",
                    include_defaulted_values_only=False,
                ),
                response_filter=api.ResponseFilterType(count=count),
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_compensation_change_reasons(
    count: Optional[Decimal] = None,
) -> CompensationChangeReasonResponse:
    """
    Gets the possible reasons for changing compensation in Workday.

    Args:
        count: The maximum number of events to return.

    Returns:
        The possible reasons for changing compensation.
    """

    @typing.no_type_check
    def xml_to_internal_response(
        output: api.GetReferencesOutput,
    ) -> CompensationChangeReasonResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal CompensationChangeReasonResponse object.
        """

        try:
            reference_id_types: list[api.ReferenceIdtype] = (
                output.body.get_references_response.response_data.reference_id
            )
        except AttributeError as e:
            raise ValueError(f"unexpected GetReferencesOutput format: {e}\nraw output:\n{output}")

        try:

            references: list[CompensationChangeReasonReference] = [
                CompensationChangeReasonReference(reference=ref_id.reference_id_data.id)
                for ref_id in reference_id_types
                if "Request_Compensation_Change" in ref_id.reference_id_data.id
            ]

        except AttributeError as e:
            raise ValueError(f"unexpected GetReferencesOutput format: {e}\nraw output:\n{output}")

        return CompensationChangeReasonResponse(references=references)

    client = get_workday_soap_client()

    if count is None:
        count = Decimal("999.0")

    payload = _get_compensation_change_reasons_payload(count=count)
    xml_response = client.get_compensation_change_references(payload)
    return xml_to_internal_response(xml_response)
