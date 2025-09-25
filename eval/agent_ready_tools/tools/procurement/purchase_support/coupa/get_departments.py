import json
from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool

from agent_ready_tools.clients.coupa_client import get_coupa_client
from agent_ready_tools.tools.procurement.common_dataclasses import ToolResponse
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaDepartment,
    CoupaDepartmentList,
)
from agent_ready_tools.tools.procurement.utils import coupa_format_error_string
from agent_ready_tools.utils.tool_credentials import COUPA_CONNECTIONS


@tool(expected_credentials=COUPA_CONNECTIONS)
def coupa_get_departments() -> ToolResponse[CoupaDepartmentList]:
    """
    Retrieves the available departments in Coupa.

    Returns:
        The retrieved list of departments in this Coupa instance.
    """
    try:
        client = get_coupa_client()
    except (ValueError, AssertionError):
        return ToolResponse(success=False, message="Failure to retrieve credentials")

    params = {"fields": json.dumps(["id", "name", "active"])}

    response = client.get_request_list(resource_name="departments", params=params)
    if len(response) == 0:
        return ToolResponse(success=False, message="No departments found.")

    if "errors" in response[0]:
        return ToolResponse(success=False, message=coupa_format_error_string(response[0]))

    department_list: List[CoupaDepartment] = []
    for department in response:
        department_list.append(
            CoupaDepartment(
                department_id=department["id"],
                department_name=department["name"],
                active_status=department["active"],
            )
        )

    return ToolResponse(
        success=True,
        message="Departments retrieved successfully.",
        content=CoupaDepartmentList(department_list=department_list),
    )
