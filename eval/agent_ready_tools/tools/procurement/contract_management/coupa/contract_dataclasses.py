from enum import StrEnum
from typing import Optional

from pydantic.dataclasses import dataclass

from agent_ready_tools.tools.procurement.invoice_management.coupa.common_classes_invoice_management import (
    CoupaInvoicePaymentTerm,
)
from agent_ready_tools.tools.procurement.purchase_support.coupa.purchase_support_dataclasses import (
    CoupaDepartment,
)
from agent_ready_tools.tools.procurement.supplier_management.coupa.supplier_dataclasses import (
    CoupaSupplierDetails,
)


@dataclass
class CoupaContractRenewalLengthUnit(StrEnum):
    """The contract's renewal length unit."""

    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"
    NULL = ""


@dataclass
class CoupaContract:
    """Represents a contract in Coupa."""

    contract_id: int
    name: str
    no_of_renewals: Optional[int]
    number: str
    reason_insight_events: Optional[list]
    renewal_length_unit: Optional[CoupaContractRenewalLengthUnit]
    renewal_length_value: Optional[int]
    status: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    supplier: Optional[CoupaSupplierDetails]
    payment_term: Optional[CoupaInvoicePaymentTerm]
    department: Optional[CoupaDepartment]

    @classmethod
    def from_fields(
        cls,
        contract_id: int,
        name: str,
        no_of_renewals: int,
        number: str,
        reason_insight_events: Optional[list],
        renewal_length_unit: CoupaContractRenewalLengthUnit,
        renewal_length_value: int,
        status: str,
        start_date: str,
        end_date: str,
        supplier_id: Optional[int],
        supplier_name: str,
        supplier_number: str,
        supplier_status: str,
        supplier_contact_email: str,
        payment_term_id: Optional[int],
        payment_term_code: str,
        coupa_contract_department_id: Optional[int],
        coupa_contract_department_name: str,
        coupa_contract_department_status: bool,
    ) -> "CoupaContract":
        """
        Initializer for Coupa contract dataclass.

        Args:
            contract_id: Contract ID.
            name: Name of contract
            no_of_renewals: Number of renewals
            number: Contract number
            reason_insight_events: Reason insight events
            renewal_length_unit: Renewal length unit (days/months/years)
            renewal_length_value: Renewal length value (1..100)
            status: Contract status
            start_date: Contract start date
            end_date: Contract end date
            supplier_id: Supplier ID
            supplier_name: Supplier name
            supplier_number: Supplier number
            supplier_status: Supplier status
            supplier_contact_email: Supplier contact email
            payment_term_id: Payment Term ID
            payment_term_code: Payment Code Term
            coupa_contract_department_id: The ID of the Department assigned to the contract
            coupa_contract_department_name: The name of the Department assigned to the contract
            coupa_contract_department_status: The status of the Department assigned to the contract

        Returns:
            A contract in Coupa.
        """

        return CoupaContract(
            contract_id=contract_id,
            name=name,
            no_of_renewals=no_of_renewals,
            number=number,
            reason_insight_events=reason_insight_events,
            renewal_length_unit=renewal_length_unit,
            renewal_length_value=renewal_length_value,
            status=status,
            start_date=start_date,
            end_date=end_date,
            supplier=(
                CoupaSupplierDetails(
                    id=supplier_id,
                    name=supplier_name,
                    number=supplier_number,
                    status=supplier_status,
                    contact_email=supplier_contact_email,
                )
                if supplier_id is not None
                else None
            ),
            payment_term=(
                CoupaInvoicePaymentTerm(
                    id=payment_term_id,
                    code=payment_term_code,
                )
                if payment_term_id is not None
                else None
            ),
            department=(
                CoupaDepartment(
                    department_id=coupa_contract_department_id,
                    department_name=coupa_contract_department_name,
                    active_status=coupa_contract_department_status,
                )
                if coupa_contract_department_id is not None
                else None
            ),
        )
