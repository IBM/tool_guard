from datetime import datetime
from decimal import Decimal
from typing import Any, Dict
import uuid

from ibm_watsonx_orchestrate.agent_builder.tools import tool
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from xsdata.models.datatype import XmlDateTime

# Request formation dataclasses
from agent_ready_tools.apis.ariba_soap_services.api import (
    AribaItem,
    Body,
    Currency,
    Description,
    Envelope,
    LineItem,
    LineItems,
    Price,
    Requester,
    RequisitionImportPullRequest,
    RequisitionRequisitionImportPullItem,
    UnitOfMeasure,
)
from agent_ready_tools.clients.ariba_soap_client import get_ariba_soap_client

# Response formation dataclasses
from agent_ready_tools.tools.procurement.purchase_support.sap_ariba.purchase_support_dataclasses import (
    AribaRequisitionImportPullReply,
    ResponseItem,
    ResponseRequisitionItems,
)
from agent_ready_tools.utils.date_conversion import iso_8601_datetime_convert_to_date as to_std_date

# from agent_ready_tools.utils.systems import Systems
from agent_ready_tools.utils.tool_credentials import ARIBA_SOAP_CONNECTIONS


def _get_payload(
    description: str,
    currency: str,
    imported_deliver_to_staging: int,
    need_by_date: datetime,
    item_name: str,
    originating_system: str,
    imported_line_comment_staging: str,
    unique_name_val: int,
    quantity: int,
    price: Decimal,
    requester_uniq_name: str,
    requester_pass: str,
    unit_of_measure: str,
) -> bytes:
    """
    Returns an XML payload object of type utf-encoded.

    Args:
        description: Description of the item to be added to the requisition.
        currency: Currency for the price of the item of the requisition item.
        imported_deliver_to_staging: Delivery code to be added, Integer
        need_by_date: The date by which the item is needed, in ISO format.
        item_name: Line Item product name.
        originating_system: Originating system.
        imported_line_comment_staging: Comment to be added.
        unique_name_val: Code containing the address for the requisition item.
        quantity: Quantity of the requisition item.
        price: Price of each unit of the requisition item.
        requester_uniq_name: Unique name of the requester.
        requester_pass: Password adapter for requester
        unit_of_measure: The unit of measure for the requisition item (e.g., "EA").

    Returns:
        Byte data containing the XML payload to be submitted to the requisition request.
    """
    if isinstance(need_by_date, datetime):
        need_by_date = need_by_date if need_by_date > datetime.now() else datetime.now()
    else:
        raise ValueError(f"Unsupported date format")

    # Forming a single line item
    line_item = LineItem(
        description=Description(
            description=description,
            price=Price(amount=price, currency=Currency(unique_name=currency)),
            unit_of_measure=UnitOfMeasure(unique_name=unit_of_measure),
        ),
        number_in_collection=1,
        originating_system_line_number=1,
        quantity=quantity,
        imported_deliver_to_staging=imported_deliver_to_staging,
        imported_line_comment_staging=imported_line_comment_staging,
        imported_line_external_comment_staging=True,
        imported_need_by_staging=XmlDateTime.from_datetime(need_by_date),
    )

    # Top-level item
    item = AribaItem(
        line_items=LineItems(item=[line_item]),
        name=item_name,
        originating_system=originating_system,
        originating_system_reference_id=str(uuid.uuid4()),  # uuid-generated unique field
        requester=Requester(
            unique_name=requester_uniq_name,
            password_adapter=requester_pass,  # credentials[CredentialKeys.REQUESTER_PASSWORD]
        ),
        unique_name=unique_name_val,
    )

    requisition_item = RequisitionRequisitionImportPullItem(item=[item])
    requisition_request = RequisitionImportPullRequest(
        partition="prealm_3841",
        variant="vrealm_3841",
        requisition_requisition_import_pull_item=requisition_item,
    )

    # Form  dataclass envelop for Request
    envelope = Envelope(body=Body(requisition_import_pull_request=requisition_request))

    # Serialize object payload to XML form
    serializer = XmlSerializer(config=SerializerConfig(pretty_print=True, xml_declaration=True))
    xml_payload = serializer.render(envelope).encode("utf-8")
    return xml_payload


# response formation helper function
def build_ariba_requisition_items(
    requisition_items: Dict[str, Any],
) -> ResponseRequisitionItems:
    """
    Helper function for building requisition items from SOAP response.

    Args:
        requisition_items: The dict containing the item of requisition fields from Ariba.

    Returns:
        A structured requistion detail dictionary containing transformed data
    from the original API response.
    """
    item_detail = requisition_items["item"]
    return ResponseRequisitionItems(
        item=ResponseItem(
            originating_system=item_detail["originating_system"],
            originating_system_reference_id=item_detail["originating_system_reference_id"],
            status_string=item_detail["status_string"],
            unique_name=item_detail["unique_name"],
        )
    )


# response formation function
def build_ariba_requisition_info_from_response(
    requisition_detail: Dict[str, Any],
) -> AribaRequisitionImportPullReply | None:
    """
    Processes and wraps purchase requisition API response.

    Args:
        requisition_detail: Create purchase requisition API response

    Returns:
        A structured purchase requisition info dictionary containing transformed data
    from the original API response.
    """
    return AribaRequisitionImportPullReply(
        partition=requisition_detail.get("partition", ""),
        variant=requisition_detail.get("variant", ""),
        requisition_items=build_ariba_requisition_items(
            requisition_detail.get("requisition_items", "")
        ),
    )


def parse_date(date_input: str) -> datetime:
    """
    Parse the input date in iso format/ other allowed string/s to datetime format needed for
    payload.

    Args:
        date_input: Input date in isoformat -ISO 8601

    Returns:
        Return the date constructed from a string to datetime format
    """
    try:
        return datetime.fromisoformat(date_input)
    except ValueError:
        pass
    # user inputs some other acceptable str formats
    if isinstance(date_input, str):
        time_formats = [
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%d-%m-%Y %H:%M",
            "%m-%d-%Y %H:%M",
            "%Y-%m-%d",
            "%d-%m-%y",
            "%m-%d-%y",
            "%d-%b-%Y",
            "%d-%b-%y",
            "%d-%B-%Y",
            "%d-%B-%y",
        ]
        for fmt in time_formats:
            try:
                return datetime.strptime(date_input, fmt)
            except ValueError:
                continue

    # Fallback: current datetime
    return datetime.now()


# Main tool function
@tool(expected_credentials=ARIBA_SOAP_CONNECTIONS)
def ariba_create_requisition(
    description: str,
    currency: str,
    item_name: str,
    requester_uniq_name: str,
    price: float = 12.0,
    imported_deliver_to_staging: int = 3000,  # default
    need_by_date: str = to_std_date("2025-06-24T00:00:00+00:00Z"),  # default iso-input accepted
    originating_system: str = "Imported",  # default
    quantity: int = 1,
    unique_name_val: int = 4545,  # default
    unit_of_measure: str = "EA",  # default
) -> AribaRequisitionImportPullReply | None:
    """
    Creates an sample requisition for the soap api user in Ariba.

    Args:
        description: Description of the item to be added to the requisition.
        currency: Currency for the price of the item of the requisition item.
        item_name: Line Item product name.
        requester_uniq_name: Unique name of the requester as in ARIBA system
        price: Price of each unit of the requisition item.
        imported_deliver_to_staging: Delivery code to be added.
        need_by_date: The date by which the item is needed, in ISO format or valid string format
        originating_system: Originating system, like "SAP ECC", "HANA Cloud" i.e. the external
            system from which  importing the requisition
        quantity: Quantity of the requisition item. (changes line type to RequisitionQuantityLine
            automatically
        unique_name_val: Code containing the integer address for the requisition item.
        unit_of_measure: The unit of measure for the requisition item (e.g., "EA").

    Returns:
        The result dataclass object on submitting the requisition request.
    """
    client = get_ariba_soap_client()  # create client object
    endpoint = f"Buyer/soap/{client.realm}/RequisitionImportPull"
    # parsing input date string to suitable form
    parsed_need_by_date = parse_date(need_by_date)
    xml_payload = _get_payload(
        description=description,
        currency=currency,
        imported_deliver_to_staging=imported_deliver_to_staging,
        need_by_date=parsed_need_by_date,  # modified to datetime fmt
        item_name=item_name,
        originating_system=originating_system,
        imported_line_comment_staging="create_requisition_PR",  # sample staging comment
        unique_name_val=unique_name_val,
        quantity=quantity,
        price=Decimal(str(price)),  # convert user input to Decimal
        requester_uniq_name=requester_uniq_name,
        requester_pass=client.requester_password,
        unit_of_measure=unit_of_measure,
    )

    # Send SOAP request to Ariba
    json_response = client.create_purchase_requisition(endpoint=endpoint, payload=xml_payload)
    req_response_details = None
    requisition_detail = json_response.get("requisition_import_pull_reply", None)

    # Build the response as object now
    if requisition_detail:
        req_response_details = build_ariba_requisition_info_from_response(requisition_detail)

    return req_response_details
