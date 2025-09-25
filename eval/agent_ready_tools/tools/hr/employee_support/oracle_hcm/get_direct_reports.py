from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.tools.hr.employee_support.oracle_hcm.get_assignment_details import (
    get_worker_work_relationship,
)
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OracleDirectReport:
    """Represents the single detail of the direct report from Oracle HCM."""

    assignment_name: str
    person_number: str
    display_name: str
    manager_person_number: str
    relationship_type: str
    level: Optional[int] = None


@dataclass
class OracleDirectReportsResponse:
    """The response containing the list of direct reports details from Oracle HCM."""

    direct_reports: List[OracleDirectReport]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def oracle_get_direct_reports(
    worker_id: str, assignment_uniq_id: str
) -> OracleDirectReportsResponse:
    """
    Gets a list of direct reports in Oracle HCM.

    Args:
        worker_id: The worker_id uniquely identifying a worker within the Oracle HCM is returned by
            the `get_user_oracle_ids` tool.
        assignment_uniq_id: The assignment_uniq_id of the worker's assignment as returned by
            `get_assignment_details` tool.

    Returns:
        The list of direct reports.
    """

    client = get_oracle_hcm_client()

    get_worker_work = get_worker_work_relationship(worker_id).worker_work_relationship[0]
    period_of_service_id = get_worker_work.period_of_service_id
    response = client.get_request(
        entity=f"/workers/{worker_id}/child/workRelationships/{period_of_service_id}/child/assignments/{assignment_uniq_id}/child/allReports",
    )
    direct_reports_list = [
        OracleDirectReport(
            assignment_name=reports.get("AssignmentName", ""),
            person_number=reports.get("PersonNumber", ""),
            display_name=reports.get("DisplayName", ""),
            manager_person_number=reports.get("ManagerPersonNumber", ""),
            relationship_type=reports.get("RelationshipType", ""),
            level=reports.get("Level", 0),
        )
        for reports in response.get("items", [])
    ]

    return OracleDirectReportsResponse(direct_reports=direct_reports_list)
