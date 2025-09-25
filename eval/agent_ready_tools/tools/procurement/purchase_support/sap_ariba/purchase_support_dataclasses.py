from dataclasses import dataclass, field
from typing import Optional  # #Type,ClassVar


@dataclass
class ResponseItem:
    """Represents the list of fields from Ariba, after creating the requisition."""

    originating_system: str
    originating_system_reference_id: str
    status_string: str
    unique_name: str


@dataclass
class ResponseRequisitionItems:
    """Represents the item, after creating the requisition in Ariba."""

    item: ResponseItem


@dataclass
class AribaRequisitionImportPullReply:
    """Represents the list of vital fields that are part of SOAP requisition response in SAP
    Ariba."""

    partition: str
    variant: str
    requisition_items: ResponseRequisitionItems


#
@dataclass
class RequisitionItemInfo:
    """Represents originating system details in requisitions in SAP Ariba."""

    originating_system: Optional[str] = field(
        default=None, metadata={"name": "OriginatingSystem", "type": "Element"}
    )
    originating_system_reference_id: Optional[str] = field(
        default=None,
        metadata={"name": "OriginatingSystemReferenceID", "type": "Element"},
    )
    status_string: Optional[str] = field(
        default=None, metadata={"name": "StatusString", "type": "Element"}
    )
    unique_name: Optional[str] = field(
        default=None, metadata={"name": "UniqueName", "type": "Element"}
    )


@dataclass
class RequisitionRequisitionIdExportItem:
    """Represents item details in requisitions in SAP Ariba."""

    item: Optional[RequisitionItemInfo] = field(
        default=None, metadata={"name": "item", "type": "Element"}
    )


@dataclass
class RequisitionImportPullReply:
    """Represents requisition details in SAP Ariba."""

    class Meta:
        """Metadata configuration for the schema with name of the schema and XML namespace
        associated with the schema."""

        name = "RequisitionImportPullReply"
        namespace = "urn:Ariba:Buyer:vrealm_3841"

    partition: Optional[str] = field(default=None, metadata={"type": "Attribute"})
    variant: Optional[str] = field(default=None, metadata={"type": "Attribute"})

    requisition_items: Optional[RequisitionRequisitionIdExportItem] = field(
        default=None,
        metadata={"name": "Requisition_RequisitionIdExport_Item", "type": "Element"},
    )


@dataclass
class HeadersData:
    """Represents RequisitionImportPullRequest attributes in SAP Ariba create requisition."""

    variant: Optional[str] = field(default=None, metadata={"name": "variant", "type": "Element"})
    partition: Optional[str] = field(
        default=None, metadata={"name": "partition", "type": "Element"}
    )

    class Meta:
        """Metadata configuration for the schema with name of the schema."""

        namespace = "urn:Ariba:Buyer:vrealm_3841"


@dataclass
class Header:
    """Represents Header in Envelope of SAP Ariba create requisition."""

    class Meta:
        """Metadata configuration for the schema with name of the schema."""

        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    headers: Optional[HeadersData] = field(
        default=None,
        metadata={
            "name": "Headers",
            "type": "Element",
            "namespace": "urn:Ariba:Buyer:vrealm_3841",
        },
    )


@dataclass
class BodyResponse:
    """Represents root element in SAP Ariba create requisition response."""

    class Meta:
        """Metadata configuration for the schema with name of the schema."""

        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    requisition_import_pull_reply: Optional[RequisitionImportPullReply] = field(
        default=None,
        metadata={
            "name": "RequisitionImportPullReply",
            "type": "Element",
            "namespace": "urn:Ariba:Buyer:vrealm_3841",
        },
    )


@dataclass
class EnvelopeResponse:
    """Represents header and body elements of Envelope in SAP Ariba create requisition response."""

    class Meta:
        """Metadata configuration for the schema with name of the schema."""

        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    header: Optional[Header] = field(default=None, metadata={"name": "Header", "type": "Element"})
    body: Optional[BodyResponse] = field(default=None, metadata={"name": "Body", "type": "Element"})
