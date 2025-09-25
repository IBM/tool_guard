import typing

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from pydantic.dataclasses import dataclass

from agent_ready_tools.apis.workday_soap_services.hr import api
from agent_ready_tools.clients.workday_soap_client import get_workday_soap_client
from agent_ready_tools.utils.tool_credentials import WORKDAY_EMPLOYEE_CONNECTIONS


@dataclass
class CompensationResponse:
    """Represents the response from getting current compensation details in Workday."""

    user_id: str
    compensation_effective_date: str
    total_base_pay: str
    total_salary_and_allowances: str
    primary_compensation_basis: str
    currency: str
    frequency: str


def _get_current_compensation_details_payload(
    user_id: str,
) -> api.GetWorkersInput:
    """
    Returns a payload object of type GetWorkersInput filled.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.

    Returns:
        The GetWorkersInput object
    """
    return api.GetWorkersInput(
        body=api.GetWorkersInput.Body(
            get_workers_request=api.GetWorkersRequest(
                request_references=api.WorkerRequestReferencesType(
                    worker_reference=[
                        api.WorkerObjectType(
                            id=[
                                api.WorkerObjectIdtype(
                                    value=user_id,
                                    type_value="WID",
                                ),
                            ]
                        ),
                    ]
                )
            )
        )
    )


@tool(expected_credentials=WORKDAY_EMPLOYEE_CONNECTIONS)
def get_current_compensation_details(user_id: str) -> CompensationResponse:
    """
    Gets a user's current compensation details in Workday.

    Args:
        user_id: The user's user_id uniquely identifying them within the Workday API.

    Returns:
        The user's compensation details.
    """
    client = get_workday_soap_client()

    payload = _get_current_compensation_details_payload(user_id=user_id)
    xml_response = client.get_current_compensation_details(payload)

    # TODO Investigate whether this logic can be cleaned up/simplified
    @typing.no_type_check
    def xml_to_internal_response(
        output: api.GetWorkersOutput,
    ) -> CompensationResponse:
        """
        Converts SOAP XML output to internal response object.

        Args:
            output: SOAP XML output from endpoint.

        Returns:
            Internal CompensationResponse object.
        """
        response_kwargs = {}

        try:
            worker_data_node: api.WorkerDataType = (
                output.body.get_workers_response.response_data.worker[0].worker_data
            )
        except (IndexError, AttributeError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get user_id from response XML
        try:
            response_kwargs["user_id"] = str(worker_data_node.user_id)
            assert response_kwargs["user_id"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get compensation_effective_date from response XML
        try:
            response_kwargs["compensation_effective_date"] = str(
                worker_data_node.compensation_data.compensation_effective_date
            )
            assert response_kwargs["compensation_effective_date"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        try:
            annualized_summary_data_node: api.CompensatableSummaryAmountAnnualizedDataType = (
                worker_data_node.compensation_data.employee_compensation_summary_data.annualized_summary_data
            )
        except AttributeError as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")
        # get total_base_pay from response XML
        try:
            response_kwargs["total_base_pay"] = str(annualized_summary_data_node.total_base_pay)
            assert response_kwargs["total_base_pay"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get total_salary_and_allowances from response XML
        try:
            response_kwargs["total_salary_and_allowances"] = str(
                annualized_summary_data_node.total_salary_and_allowances
            )
            assert response_kwargs["total_salary_and_allowances"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get primary_compensation_basis from response XML
        try:
            response_kwargs["primary_compensation_basis"] = str(
                annualized_summary_data_node.primary_compensation_basis
            )
            assert response_kwargs["primary_compensation_basis"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get currency_reference from response XML
        try:
            for cid in annualized_summary_data_node.currency_reference.id:
                if cid.type_value == "Currency_ID":
                    response_kwargs["currency"] = str(cid.value)
            assert response_kwargs["currency"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        # get frequency_reference from response XML
        try:
            for fid in annualized_summary_data_node.frequency_reference.id:
                if fid.type_value == "Frequency_ID":
                    response_kwargs["frequency"] = str(fid.value)
            assert response_kwargs["frequency"]
        except (AttributeError, AssertionError) as e:
            raise ValueError(f"unexpected GetWorkersOutput format: {e}\nraw output:\n{output}")

        return CompensationResponse(**response_kwargs)

    return xml_to_internal_response(xml_response)
