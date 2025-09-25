from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from xsdata.models.datatype import XmlDateTime


@dataclass
class Currency:
    """
    Currency details of the purchase order line item.

    Attributes:
        unique_name: Type of currency (Eg: USD)
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    unique_name: Optional[str] = field(
        default=None,
        metadata={"name": "UniqueName", "type": "Element"},
    )


@dataclass
class UnitOfMeasure:
    """
    Unit of measure of the purchase order line item.

    Attributes:
        unique_name: Represents unit (Eg: EA)
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    unique_name: Optional[str] = field(
        default=None,
        metadata={"name": "UniqueName", "type": "Element"},
    )


@dataclass
class Price:
    """
    Price of the purchase order line item.

    Attributes:
        amount: Represents amount in decimal
        currency: represents currency of transaction
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    amount: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Amount",
            "type": "Element",
            "min_inclusive": Decimal("0"),
            "total_digits": 21,
            "fraction_digits": 6,
        },
    )
    currency: Optional[Currency] = field(
        default=None,
        metadata={"name": "Currency", "type": "Element"},
    )


@dataclass
class Description:
    """
    Description details of the each item from the Line Item.

    Attributes:
        description: details of the item
        price: unit price of the item
        unit_of_measure: how the item is measured, eg units, kg,litre etc
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    description: Optional[str] = field(
        default=None,
        metadata={"name": "Description", "type": "Element"},
    )
    price: Optional[Price] = field(
        default=None,
        metadata={"name": "Price", "type": "Element"},
    )
    unit_of_measure: Optional[UnitOfMeasure] = field(
        default=None,
        metadata={"name": "UnitOfMeasure", "type": "Element"},
    )


@dataclass
class LineItem:
    """
    LineItem details and its different elements.

    Attributes:
        description: details of the line item
        number_in_collection: integer number denoting the position of the line in the requisition or
            purchase order
        originating_system_line_number: The line's identifier in the original external system.
        quantity: The number of units requested for this line item
        imported_deliver_to_staging: Imported “deliver to” destination temporarily stored during
            staging
        imported_line_comment_staging: captures the line-level comment from your external system,
            exactly as it was in the import feed
        imported_line_external_comment_staging: Boolean Value indicating if comment is visible to
            suppliers or not:
        ImportedNeedByStaging: Imported “need-by” future date kept for staging or validation,
            defaults to present if no future date available
    """

    class Meta:
        """
        Attributes:
            name: used to map to correct xml tag
            namespace: namespace information for parsing/serialization etc.
        """

        name = "item"
        namespace = "urn:Ariba:Buyer:vrealm_3841"

    description: Optional[Description] = field(
        default=None,
        metadata={"name": "Description", "type": "Element"},
    )
    number_in_collection: Optional[int] = field(
        default=None,
        metadata={"name": "NumberInCollection", "type": "Element"},
    )
    originating_system_line_number: Optional[int] = field(
        default=None,
        metadata={"name": "OriginatingSystemLineNumber", "type": "Element"},
    )
    quantity: Optional[int] = field(
        default=None,
        metadata={"name": "Quantity", "type": "Element"},
    )
    imported_deliver_to_staging: Optional[int] = field(
        default=None,
        metadata={"name": "ImportedDeliverToStaging", "type": "Element"},
    )
    imported_line_comment_staging: Optional[str] = field(
        default=None,
        metadata={"name": "ImportedLineCommentStaging", "type": "Element"},
    )
    imported_line_external_comment_staging: Optional[bool] = field(
        default=None,
        metadata={"name": "ImportedLineExternalCommentStaging", "type": "Element"},
    )
    imported_need_by_staging: Optional[XmlDateTime] = field(
        default=None,
        metadata={"name": "ImportedNeedByStaging", "type": "Element"},
    )


@dataclass
class LineItems:
    """
    Class LineItems denoting list of all individual LineItems.

    Attributes:
        item: List of LineItems with each LineItem having own elements
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    item: List[LineItem] = field(
        default_factory=list,
        metadata={"type": "Element"},
    )


@dataclass
class Requester:
    """
    Details about the user who submits the requisition or item.

    Attributes:
        unique_name: user’s internal Ariba username/ID, which Ariba uses to track who originated the
            request.Also called "preparer" or "submitter"
        password_adapter: Ariba uses this value to determine how the user logs in or connects,
            especially in API or external approval contexts.
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    unique_name: Optional[str] = field(
        default=None, metadata={"name": "UniqueName", "type": "Element"}
    )
    password_adapter: Optional[str] = field(
        default=None,
        metadata={"name": "PasswordAdapter", "type": "Element"},
    )


@dataclass
class AribaItem:
    """
    :ivar: line_items:Maps to the LineItems XML element, containing one or more LineItem entries.

    Attributes:
        name: descriptive title for the AribaItem, such as an ERP requisition number or user-
            provided label
        originating_system: external system name from which the requisition originates (e.g., your
            ERP system)
        originating_system_reference_id: system-generated ID (like a requisition or restock number)
            from the external system
        requester: information about who submitted the requisition or item in Ariba (see earlier
            details
        unique_name: is used to match and update the same object across multiple imports or workflow
            events.
    """

    class Meta:
        """
        Attributes:
            name: used to map to correct xml tag
            namespace: namespace information for parsing/serialization etc.
        """

        name = "item"
        namespace = "urn:Ariba:Buyer:vrealm_3841"

    line_items: Optional[LineItems] = field(
        default=None,
        metadata={"name": "LineItems", "type": "Element"},
    )
    name: Optional[str] = field(
        default=None,
        metadata={"name": "Name", "type": "Element"},
    )
    originating_system: Optional[str] = field(
        default=None,
        metadata={"name": "OriginatingSystem", "type": "Element"},
    )
    originating_system_reference_id: Optional[str] = field(  # earlier Optional[int]
        default=None,
        metadata={"name": "OriginatingSystemReferenceID", "type": "Element"},
    )
    requester: Optional[Requester] = field(
        default=None,
        metadata={"name": "Requester", "type": "Element"},
    )
    unique_name: Optional[int] = field(
        default=None,
        metadata={"name": "UniqueName", "type": "Element"},
    )


@dataclass
class RequisitionRequisitionImportPullItem:
    """
    Describes the XML payload,and which class corresponds to the
    Requisition_RequisitionImportPull_Item element.

    Attributes:
        item: holds a list of AribaItem objects, each representing one requisition to be imported or
            updated.
    """

    class Meta:
        """
        Attributes:
            name: used to map to correct xml tag
            namespace: namespace information for parsing/serialization etc.
        """

        name = "Requisition_RequisitionImportPull_Item"
        namespace = "urn:Ariba:Buyer:vrealm_3841"

    item: List[AribaItem] = field(
        default_factory=list,
        metadata={"type": "Element"},
    )


@dataclass
class RequisitionImportPullRequest:
    """
    These are key identifiers for your Ariba realm and site context.

    Attributes:
        partition: key identifier for your Ariba realm and site context.
        variant: key identifier for your Ariba realm and site context.
        requisition_requisition_import_pull_item: container holding one or more AribaItem objects to
            import.
    """

    class Meta:
        """
        Attributes:
            name: used to map to correct xml tag
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "urn:Ariba:Buyer:vrealm_3841"

    partition: Optional[str] = field(
        default=None,
        metadata={"type": "Attribute"},
    )
    variant: Optional[str] = field(
        default=None,
        metadata={"type": "Attribute"},
    )
    requisition_requisition_import_pull_item: Optional[RequisitionRequisitionImportPullItem] = (
        field(
            default=None,
            metadata={"name": "Requisition_RequisitionImportPull_Item", "type": "Element"},
        )
    )


@dataclass
class Body:
    """
    Body of the Envelop Class.

    Attributes:
        requisition_import_pull_request: Root of the import operation, defines Ariba realm context
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    requisition_import_pull_request: Optional[RequisitionImportPullRequest] = field(
        default=None,
        metadata={
            "name": "RequisitionImportPullRequest",
            "type": "Element",
            "namespace": "urn:Ariba:Buyer:vrealm_3841",
        },
    )


@dataclass
class Envelope:
    """
    Attributes:
        body: Body containing main Object-requisition_import_pull_request
    """

    class Meta:
        """
        Attributes:
            namespace: namespace information for parsing/serialization etc.
        """

        namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    body: Optional[Body] = field(
        default=None,
        metadata={"name": "Body", "type": "Element"},
    )
