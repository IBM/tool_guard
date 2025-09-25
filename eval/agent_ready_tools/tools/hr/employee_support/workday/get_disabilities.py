from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class Disability:
    """Represents disabilities in Workday."""

    disability_reference_wid: str
    disability_data_name: str
    disability_data_id: str


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_disabilities(limit: Optional[str] = "30", offset: Optional[str] = "0") -> list[Disability]:
    """
    Gets a list of disabilities for this Workday deployment.

    Args:
        limit: The maximum number of disabilities to retrieve in a single API call. Defaults to
            30. Use this to control the size of the result set.
        offset: The number of disabilities to skip for pagination purposes. Use this to retrieve
            subsequent pages of results when handling large datasets.

    Returns:
        The list of disabilities.
    """
    client = get_workday_soap_client()

    xml_response = client.get_disabilities()

    array = (
        xml_response.body.get_disabilities_response.response_data.disability
        if xml_response.body
        and xml_response.body.get_disabilities_response
        and xml_response.body.get_disabilities_response.response_data
        and xml_response.body.get_disabilities_response.response_data.disability
        else []
    )

    disabilities: list[Disability] = []
    for disability in array:
        new_disability_reference_wid = (
            disability.disability_reference.id[0].value
            if disability.disability_reference
            and disability.disability_reference.id
            and disability.disability_reference.id[0].value
            else ""
        )
        new_disability_reference_wid = str(new_disability_reference_wid)
        if not new_disability_reference_wid:
            raise ValueError(f"Unexpected get_disabilities format \nRaw output:\n{xml_response}")

        new_disability_data_name = (
            disability.disability_data.name if disability.disability_data else ""
        )
        new_disability_data_name = str(new_disability_data_name)

        new_disability_data_id = disability.disability_data.id if disability.disability_data else ""
        new_disability_data_id = str(new_disability_data_id)

        disabilities.append(
            Disability(
                disability_reference_wid=new_disability_reference_wid,
                disability_data_name=new_disability_data_name,
                disability_data_id=new_disability_data_id,
            )
        )

    limit_int = int(limit) if limit is not None else 30
    offset_int = int(offset) if offset is not None else 0

    return disabilities[offset_int : offset_int + limit_int]
