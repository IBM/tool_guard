from typing import List, Optional

from fuzzywuzzy import process
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class OraclePositions:
    """Represents position details in Oracle HCM."""

    position_name: str
    position_code: str
    position_id: int
    job_id: int
    job_code: str
    job_name: str
    hiring_status: str
    department_id: int
    department_name: str
    business_unit_id: int


@dataclass
class GetPositionsResponse:
    """Represents the response from getting a position in Oracle HCM."""

    positions: List[OraclePositions]


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_positions_oracle(position_name: Optional[str] = None) -> GetPositionsResponse:
    """
    Retrieves the list of positions in Oracle HCM.

    Args:
        position_name: The name of the position to filter results.

    Returns:
        A response containing a list of positions.
    """

    client = get_oracle_hcm_client()

    response = client.get_request(entity="positionsLov")
    positions_list = [
        OraclePositions(
            position_name=position.get("PositionName", ""),
            position_code=position.get("PositionCode", ""),
            position_id=position.get("PositionId", ""),
            job_id=position.get("JobId", ""),
            job_code=position.get("JobCode", ""),
            job_name=position.get("JobName", ""),
            hiring_status=position.get("HiringStatus", ""),
            department_id=position.get("DepartmentId", ""),
            department_name=position.get("DepartmentName", ""),
            business_unit_id=position.get("BusinessUnitId", ""),
        )
        for position in response["items"]
    ]
    if position_name:
        query_object = OraclePositions(
            position_name=position_name,
            position_code="",
            position_id=0,
            job_id=0,
            job_code="",
            job_name="",
            hiring_status="",
            department_id=0,
            department_name="",
            business_unit_id=0,
        )
        top_option = [
            option
            for option, score in process.extract(
                query_object, positions_list, processor=lambda opt: opt.position_name, limit=1
            )
        ]
        positions_list = top_option

    return GetPositionsResponse(positions=positions_list)
