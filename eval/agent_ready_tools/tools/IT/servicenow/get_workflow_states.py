from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.clients.servicenow_client import get_servicenow_client
from agent_ready_tools.utils.tool_credentials import SERVICENOW_CONNECTIONS


@dataclass
class WorkflowState:
    """Represents a Workflow state in ServiceNow."""

    work_flow_state: str
    work_flow_state_value: str


@dataclass
class WorkflowStateResponse:
    """Represents the response from getting a list of workflow states."""

    workflow_state: list[WorkflowState]


@tool(expected_credentials=SERVICENOW_CONNECTIONS)
def get_workflow_states() -> WorkflowStateResponse:
    """
    Gets a workflow state list in ServiceNow.

    Returns:
        The list of workflow states.
    """
    client = get_servicenow_client()

    response = client.get_request(
        entity="sys_choice", params={"name": "kb_knowledge", "element": "workflow_state"}
    )

    workflow_state = [
        WorkflowState(
            work_flow_state=record.get("label"), work_flow_state_value=record.get("value")
        )
        for record in response["result"]
    ]
    return WorkflowStateResponse(workflow_state=workflow_state)
