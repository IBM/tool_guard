from typing import List

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.oraclehcm_client import get_oracle_hcm_client
from agent_ready_tools.utils.get_id_from_links import get_id_from_links
from agent_ready_tools.utils.tool_credentials import ORACLE_HCM_CONNECTIONS


@dataclass
class LearningRecord:
    """Represents the learning_record_id from learner learning records api."""

    learning_record_id: str


@dataclass
class LearningRecordResponse:
    """Represents the response from getting learning record ids from Oracle HCM."""

    learning_records: List[LearningRecord]


@dataclass
class LearningStatusesResponse:
    """Represents the response from getting learning statuses from Oracle HCM."""

    learning_status_code: str


# This method retrieves learning record IDs using a person_id. To obtain the learning status, the learning_record_id is required.
def get_learning_record_id(person_id: int) -> LearningRecordResponse:
    """
    Gets a worker's learning record id in Oracle HCM.

    Args:
        person_id: The person_id uniquely identifies them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.

    Returns:
        The worker's learning record id.
    """

    client = get_oracle_hcm_client()
    response = client.get_request(
        "learnerLearningRecords",
        q_expr=f"assignedToId={person_id}",
        headers={"REST-Framework-Version": "4"},
    )
    learning_records: list[LearningRecord] = []
    for result in response["items"]:
        learning_records.append(
            LearningRecord(learning_record_id=get_id_from_links(result["links"][0]["href"]))
        )
    return LearningRecordResponse(learning_records=learning_records)


@tool(expected_credentials=ORACLE_HCM_CONNECTIONS)
def get_learning_statuses(status: str, person_id: int) -> LearningStatusesResponse:
    """
    Gets learning statuses from Oracle HCM.

    Args:
        status: The status of the learning in Oracle HCM.
        person_id: The person_id uniquely identifies them within the Oracle HCM returned by the
            `get_user_oracle_ids` tool.

    Returns:
        The learning statuses within Oracle HCM.
    """
    # Invoking the get_learning_record_id method to obtain the learning_record_ids.
    learning_records = get_learning_record_id(person_id).learning_records

    if learning_records:
        # Retrieving the first learning_record_id from the list of learning_records.
        learning_name = learning_records[0].learning_record_id
    else:
        raise ValueError("No learning records found.")

    client = get_oracle_hcm_client()

    q_expr = f"Meaning='{status}'"

    response = client.get_request(
        f"learnerLearningRecords/{learning_name}/lov/AssignmentStatusLOV", q_expr=q_expr
    )

    result = response["items"][0]
    return LearningStatusesResponse(
        learning_status_code=result["LookupCode"],
    )
