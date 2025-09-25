from agent_ready_tools.clients.sap_successfactors_client import get_sap_successfactors_client


def get_new_question_number(job_req_id: str) -> int:
    """
    Returns the next available, unused question number for a job requisition from SAP
    SuccessFactors.

    Args:
        job_req_id: The id of the job requisition from which screening questions are to be retrieved, returned by the tool `get_job_requisitions`.

    Returns:
        The highest question number of the screening question.
    """
    order = 0
    client = get_sap_successfactors_client()

    response = client.get_request(
        entity="JobReqScreeningQuestion",
        filter_expr=f"jobReqId eq '{job_req_id}'",
    )

    result = response.get("d", {}).get("results", [])

    for item in result:
        order_int = int(item.get("order", ""))
        if order < order_int:
            order = order_int

    return order + 1
