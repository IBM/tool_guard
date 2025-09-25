from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.clients_enums import AccessLevel
from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class JobChangeReason:
    """Represents a job change reason in Workday."""

    id: str
    descriptor: str
    is_for_employee: Optional[bool] = None
    is_for_contingent_worker: Optional[bool] = None
    manager_reason: Optional[bool] = None


@dataclass
class JobChangeReasonResponse:
    """Represents a response for job change group in Workday."""

    job_change_reasons: list[JobChangeReason]
    total: int


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_job_change_reasons() -> JobChangeReasonResponse:
    """
    Gets a job change reason in Workday.

    Returns:
        The job change group reason ids.
    """

    client = get_workday_client(access_level=AccessLevel.MANAGER)

    url = f"api/v1/{client.tenant_name}/jobChangeReasons"
    response = client.get_request(url=url)

    job_change_reasons: list[JobChangeReason] = []
    for report in response["data"]:
        job_change_reasons.append(
            JobChangeReason(
                id=report.get("id", ""),
                descriptor=report.get("descriptor", ""),
                is_for_employee=report.get("isForEmployee", ""),
                is_for_contingent_worker=report.get("isForContingentWorker", ""),
                manager_reason=report.get("managerReason", ""),
            )
        )
    return JobChangeReasonResponse(job_change_reasons=job_change_reasons, total=response["total"])
