from decimal import Decimal
import typing
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.integrations import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS

REFERENCE_TYPE = "Termination_Subcategory_ID"


@dataclass
class ReferenceIdData:
    """Represents the data for a single reference ID."""

    reference_id: str


@dataclass
class ReferenceIdsResponse:
    """Represents the response from getting reference ids in Workday."""

    reference_ids: List[ReferenceIdData]


def _get_references_ids_payload(
    reference_id_type: str,
    page: Optional[Decimal] = Decimal(1),
    count: Optional[Decimal] = Decimal(20),
) -> api.GetReferencesInput:
    """
    Returns a payload object of type GetReferencesInput filled.

    Args:
        reference_id_type: The type of the Reference ID (e.g. Location_ID).
        page: The page number for pagination. This parameter determines which page of the reference
            ids list to retrieve. Defaults to 1.
        count: The number of reference IDs to retrieve per page. This parameter specifies the
            maximum number of reference IDs to return in the response. Defaults to 20.

    Returns:
        The list of reference ids
    """

    return api.GetReferencesInput(
        body=api.GetReferencesInput.Body(
            get_references_request=api.GetReferencesRequest(
                request_criteria=api.GetReferencesRequestCriteriaType(
                    reference_id_type=reference_id_type
                ),
                response_filter=api.ResponseFilterType(page=page, count=count),
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_reference_ids(reference_id_type: str = REFERENCE_TYPE) -> ReferenceIdsResponse:
    """
    Gets a list of reference ids in Workday.

    Args:
        reference_id_type: The type of the Reference ID (e.g. Location_ID).

    Returns:
        The reference unique identifier details.
    """

    @typing.no_type_check
    def xml_to_internal_response(output: api.GetReferencesOutput) -> ReferenceIdsResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal ReferenceIdsResponse object.
        """

        try:
            reference_ids_list = [
                ReferenceIdData(
                    reference_id=ref_id.reference_id_data.id,
                )
                for ref_id in output.body.get_references_response.response_data.reference_id
            ]
        except AttributeError as e:
            raise ValueError(f"unexpected GetReferencesOutput format: {e}\nraw output:\n{output}")

        return ReferenceIdsResponse(reference_ids=reference_ids_list)

    client = get_workday_soap_client()
    response = client.get_reference_ids(
        _get_references_ids_payload(
            reference_id_type=reference_id_type,
        )
    )

    return xml_to_internal_response(response)
