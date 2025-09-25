from string import punctuation
from typing import List, Optional

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.workday_client import get_workday_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass(frozen=True)
class UserWorkdayIDs:
    """Represents the response from getting a user's unique identifiers from Workday."""

    name: Optional[str]
    email: Optional[str]
    person_id: Optional[str]
    user_id: Optional[str]


@dataclass(frozen=True)
class UserIDsResponse:
    """Represents the response from getting user ids."""

    workers: List[UserWorkdayIDs]


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_user_workday_ids(name: str) -> UserIDsResponse:
    """
    Get a user's person_id and user_id from Workday.

    Args:
        name: The worker's name for which to search.

    Returns:
        The user's unique identifiers within Workday.
    """
    client = get_workday_client()
    url = f"api/staffing/v6/{client.tenant_name}/workers"
    params = {"search": name}
    response = client.get_request(url=url, params=params)

    # TODO(DanielD): Return as a message so the agent can handle the response.
    # In the unlikely situation where the API returns more than the max, rather than
    # paginate a clearer name should be provided.
    total = response.get("total")
    if total is not None:
        assert (
            total <= 100
        ), "Please provide a clearer worker name. For example include first and last name."

    # TODO(DanielD): Return as a message so the agent can handle the response.
    assert not any(
        p in name for p in punctuation
    ), f"Name: '{name} is invalid because it contains punctuation."

    workers = []

    workers_data = response.get("data")
    if workers_data is not None:
        for worker in workers_data:
            person = worker.get("person")
            workers.append(
                UserWorkdayIDs(
                    name=worker.get("descriptor"),
                    email=person.get("email") if person is not None else None,
                    person_id=person.get("id") if person is not None else None,
                    user_id=worker.get("id"),  # Workday Instance ID.
                )
            )

    return UserIDsResponse(workers=workers)
