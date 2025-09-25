from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlTime


@dataclass
class AbstractExternalParameterObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Abstract_External_ParameterObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ActionEventObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Action_EventObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class AmazonSimpleStorageServiceEibDeliveryProtocolDataType:
    """
    AWS S3 Delivery Protocol Data.

    Attributes:
        bucket: S3 Bucket Identifier for delivery
        bucket_region: Region ID for AS3
        access_key_id: AWS Access Key ID for delivery
        secret_access_key: AWS Secret Access Key for delivery
    """

    class Meta:
        name = "Amazon_Simple_Storage_Service_EIB_Delivery_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    bucket: Optional[str] = field(
        default=None,
        metadata={
            "name": "Bucket",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    bucket_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "Bucket_Region",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    access_key_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Access_Key_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    secret_access_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Secret_Access_Key",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class AmazonSimpleStorageServiceEibRetrievalProtocolDataType:
    """
    AWS S3 Retrieval Protocol Data.

    Attributes:
        bucket: S3 Bucket Identifier
        bucket_region: Region ID for AS3
        access_key_id: AWS Access Key ID
        secret_access_key: AWS Secret Access Key
    """

    class Meta:
        name = "Amazon_Simple_Storage_Service_EIB_Retrieval_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    bucket: Optional[str] = field(
        default=None,
        metadata={
            "name": "Bucket",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    bucket_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "Bucket_Region",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    access_key_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Access_Key_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    secret_access_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Secret_Access_Key",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class AttachmentDataWwstype:
    """
    The details of a resume (resume, name, comments).

    Attributes:
        file_id: The Reference ID for the resume.
        file: A comment about the resume.
        file_name: The name of the resume.
        comments: The resume that was attached for the applicant.
    """

    class Meta:
        name = "Attachment_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    file_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "File_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    file: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "File",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "format": "base64",
        },
    )
    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 255,
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class AuthenticationFaultType:
    class Meta:
        name = "Authentication_FaultType"
        target_namespace = "urn:com.workday/bsvc"

    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class BackgroundProcessMessageDataWstype:
    """
    Message.

    Attributes:
        timestamp: Timestamp
        severity: Message Severity Level
        message_summary: The text contents of the message
        line_number: Line Number
        line_identifier: Line Identifier
        code: Error Code
    """

    class Meta:
        name = "Background_Process_Message_Data_WSType"
        target_namespace = "urn:com.workday/bsvc"

    timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Timestamp",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    severity: Optional[str] = field(
        default=None,
        metadata={
            "name": "Severity",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    message_summary: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message_Summary",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    line_number: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Line_Number",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    line_identifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "Line_Identifier",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class BackgroundProcessMessageSeverityLevelObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Background_Process_Message_Severity_LevelObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class BackgroundProcessRuntimeStatusObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Background_Process_Runtime_StatusObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class BusinessObjectObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Business_ObjectObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class BusinessProcessDataType:
    """
    Element containing the data for the Denial (Comment)

    Attributes:
        comment: Captures the Comment for the Business Process.
    """

    class Meta:
        name = "Business_Process_DataType"
        target_namespace = "urn:com.workday/bsvc"

    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class BusinessProcessTypeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Business_Process_TypeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CancelBusinessProcessDataType:
    """
    Provide additional details for the Business Process cancelation.

    Attributes:
        comment: Comment
        suppress_notifications: Suppress Notifications
    """

    class Meta:
        name = "Cancel_Business_Process_DataType"
        target_namespace = "urn:com.workday/bsvc"

    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    suppress_notifications: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Suppress_Notifications",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ChecklistObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "ChecklistObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CloudCollectionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Cloud_CollectionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CommentObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "CommentObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ConditionRuleObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Condition_RuleObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CurrencyObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "CurrencyObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CustomBusinessFormLayoutObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Custom_Business_Form_LayoutObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CustomObjectObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Custom_ObjectObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class CustomReportDefinitionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Custom_Report_DefinitionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CustomReportTransformationObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Custom_Report_TransformationObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class DateIntervalObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Date_IntervalObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class DeliveredBusinessFormLayoutObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Delivered_Business_Form_LayoutObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class DisplayOptionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Display_OptionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class DocumentTagObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Document_TagObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class DocumentTypeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Document_TypeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class EmailTransportProtocolDataType:
    """
    Email Transport Protocol Data element.

    Attributes:
        to_email_address: Email Address
        cc_internet_email_address: Carbon Copy Email Address
        bcc_internet_email_address: Blind Carbon Copy Email Address
        from_internet_email_address: From Email Address
        email_subject: Email Subject line
        email_text: Email Body
    """

    class Meta:
        name = "Email_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    to_email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "To_Email_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    cc_internet_email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "Cc_Internet_Email_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    bcc_internet_email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "Bcc_Internet_Email_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    from_internet_email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "From_Internet_Email_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    email_subject: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email_Subject",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    email_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email_Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "EventObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class EventClassificationSubcategoryObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Event_Classification_SubcategoryObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class EventRecordActionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Event_Record_ActionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class EventRequestCriteriaType:
    """
    This element contains request criteria to exclude Process History and Remaining Process Data.

    Attributes:
        exclude_process_history_data: This boolean flag determines whether to exclude Process
            History Data.
        exclude_remaining_step_data: This boolean flag determines whether to exclude Remaining Step
            Data.
    """

    class Meta:
        name = "Event_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    exclude_process_history_data: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Exclude_Process_History_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    exclude_remaining_step_data: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Exclude_Remaining_Step_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventServiceObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Event_ServiceObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class EventTargetObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Event_TargetObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExceptionDataType:
    """
    Exception (Errors and Warning) associated with the transaction.

    Attributes:
        classification: Exception Classification (Error or Warning)
        message: Exception Detail
    """

    class Meta:
        name = "Exception_DataType"
        target_namespace = "urn:com.workday/bsvc"

    classification: Optional[str] = field(
        default=None,
        metadata={
            "name": "Classification",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalFieldObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "External_FieldObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ExternalInstanceIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        parent_id: Contains a unique identifier for an instance of a parent object
        parent_type: The unique identifier type of a parent object
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".
    """

    class Meta:
        name = "External_Instance_IDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalPromptableObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "External_PromptableObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class FtpsTransportProtocolDataType:
    """
    FTPS Transport Protocol Data element.

    Attributes:
        ftps_address: FTPS Address
        directory: Directory
        use_passive_mode: Use Passive Mode
        user_id: Text attribute identifying User Name.
        password: Text attribute identifying Password.
        use_temp_file: Allow the file to be overwritten only when it is finished uploading to
            external site. Avoids the external system from attempting to read file before it has
            been fully uploaded.
    """

    class Meta:
        name = "FTPS_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    ftps_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "FTPS_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    directory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Directory",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    use_passive_mode: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Passive_Mode",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    user_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "User_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    use_temp_file: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Temp_File",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class FtpTransportProtocolDataType:
    """
    FTP Transport Protocol Data element.

    Attributes:
        ftp_address: FTP Address
        directory: Directory
        use_passive_mode: Use Passive Mode
        user_id: Text attribute identifying User Name.
        password: Text attribute identifying Password.
        use_temp_file: Allow the file to be overwritten only when it is finished uploading to
            external site. Avoids the external system from attempting to read file before it has
            been fully uploaded.
    """

    class Meta:
        name = "FTP_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    ftp_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "FTP_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    directory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Directory",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    use_passive_mode: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Passive_Mode",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    user_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "User_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    use_temp_file: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Temp_File",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GenericDocumentBuilderAuditedObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Generic_Document_Builder__Audited_ObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class GetEventDocumentsDataType:
    """
    Get Event Documents Data.

    Attributes:
        collection_id: Get Event Documents Collection ID
        reference_id: Get Event Documents Reference ID
    """

    class Meta:
        name = "Get_Event_Documents_DataType"
        target_namespace = "urn:com.workday/bsvc"

    collection_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Collection_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    reference_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reference_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetReferencesRequestCriteriaType:
    """
    Contains additional criteria for identifying specific Staffing Field Defaults instances.

    Attributes:
        reference_id_type: The "Reference ID Type" is the name of the index for a business object in
            Workday. For example, the Location business object in Workday has a "Reference ID Type"
            of Location_ID.
        include_defaulted_values_only: Include only Reference IDs that match the default Reference
            ID format.
    """

    class Meta:
        name = "Get_References_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    reference_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Type",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "max_length": 128,
        },
    )
    include_defaulted_values_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Include_Defaulted_Values_Only",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GoogleDriveEibTransportProtocolDataType:
    """
    Google Drive EIB Transport Protocol Data element.

    Attributes:
        directory: Google Drive Directory path
    """

    class Meta:
        name = "Google_Drive_EIB_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    directory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Directory",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HttpHeaderType:
    """
    HTTP Header.

    Attributes:
        header_value: Header Value
        header_name: Header Name
    """

    class Meta:
        name = "HTTP_HeaderType"
        target_namespace = "urn:com.workday/bsvc"

    header_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Header_Value",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    header_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Header_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HideWorkdayDeliveredReportRequestCriteriaType:
    """Contains additional criteria for identifying hidden Workday delivered reports."""

    class Meta:
        name = "Hide_Workday_Delivered_Report_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"


@dataclass
class HideWorkdayDeliveredReportResponseGroupType:
    """
    Contains criteria for identifying whether a reference is included.

    Attributes:
        include_reference: Include reference flag
    """

    class Meta:
        name = "Hide_Workday_Delivered_Report_Response_GroupType"
        target_namespace = "urn:com.workday/bsvc"

    include_reference: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Include_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class InstanceIdtype:
    class Meta:
        name = "Instance_IDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegratableObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "IntegratableObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAttributeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Integration_AttributeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationConnectorConfigurationDataType:
    """
    Connector Configuration.

    Attributes:
        local_in_endpoint: Address of the local-in component used to invoke a connector sub-assembly
    """

    class Meta:
        name = "Integration_Connector_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    local_in_endpoint: Optional[str] = field(
        default=None,
        metadata={
            "name": "Local-In_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDeliveryConfigurationDataType:
    """Integration Delivery Configuration Data element."""

    class Meta:
        name = "Integration_Delivery_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationDocumentFieldObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Integration_Document_FieldObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDocumentOptionValueObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Integration_Document_Option_ValueObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEsbInvocationAbstractObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_ESB_Invocation__Abstract_ObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationEnterpriseEventRecordsDataType:
    """
    Element containing records counts for the Integration Enterprise Event.

    Attributes:
        total_records: Total Records
        total_records_uploaded: Total Records Uploaded
        total_failed_records: Total Failed Records
    """

    class Meta:
        name = "Integration_Enterprise_Event_Records_DataType"
        target_namespace = "urn:com.workday/bsvc"

    total_records: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Total_Records",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 6,
            "fraction_digits": 0,
        },
    )
    total_records_uploaded: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Total_Records_Uploaded",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 6,
            "fraction_digits": 0,
        },
    )
    total_failed_records: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Total_Failed_Records",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 6,
            "fraction_digits": 0,
        },
    )


@dataclass
class IntegrationEnumerationObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Integration_EnumerationObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEnumerationDefinitionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_Enumeration_DefinitionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationEventAbstractObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_Event__Abstract_ObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationLaunchOptionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_Launch_OptionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationRepositoryDocumentObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_Repository_DocumentObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationRetrievalConfigurationDataType:
    """Integration Retrieval Configuration Data element."""

    class Meta:
        name = "Integration_Retrieval_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationSequenceGeneratorServiceObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_Sequence_Generator_ServiceObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationSequencerObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Integration_SequencerObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationServiceObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_ServiceObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationSystemObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_SystemObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationSystemIdentifierObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Integration_System_IdentifierObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemResponseGroupType:
    """
    The response groups allows for the amount of data contained within the response to be tailored
    to only included elements that the user is looking for.

    If no response group is provided in the request, then ONLY the payee
    references will be returned. If no response group is provided AND
    the Page and Count parameters within the Response Filter element are
    also omitted, then ALL of the payee references will be returned in
    your response (no paging is performed).

    Attributes:
        include_reference: Indicates if the Reference element for the Integration System is included
            in the response.
        show_values_for_all_environments: Indicates if the values that may be Restricted to
            Environment should be filtered to only the value for the current environment.  If TRUE,
            then all values are included within the response.
        exclude_wid: If Excluded WID is enabled then "External Instance Object [EL], 6$42871" will
            only serialize Reference Index, otherwise Reference Index plus WID will be serialized
    """

    class Meta:
        name = "Integration_System_Response_GroupType"
        target_namespace = "urn:com.workday/bsvc"

    include_reference: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Include_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    show_values_for_all_environments: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Show_Values_For_All_Environments",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    exclude_wid: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Exclude_WID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemAuditedObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_System__Audited_ObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationTagObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_TagObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationTemplateObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_TemplateObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationTemplateAbstractObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Integration_Template__Abstract_ObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class InternetEmailAddressDataForNotificationsType:
    """
    Wraps notification email addresses.

    Attributes:
        email_address: Email Address
    """

    class Meta:
        name = "Internet_Email_Address_Data_for_NotificationsType"
        target_namespace = "urn:com.workday/bsvc"

    email_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class InvalidReferenceIdDataType:
    """
    Represents a reference ID that was submitted with data not found in Workday.

    Attributes:
        invalid_reference_id: Invalid Reference ID
        invalid_reference_id_type: Invalid Reference ID Type
    """

    class Meta:
        name = "Invalid_Reference_ID_DataType"
        target_namespace = "urn:com.workday/bsvc"

    invalid_reference_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Invalid_Reference_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    invalid_reference_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Invalid_Reference_ID_Type",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 128,
        },
    )


@dataclass
class LaunchParameterObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Launch_ParameterObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class MimeTypeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Mime_TypeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class Oauth20DataType:
    """
    OAuth 2.0 Data.

    Attributes:
        access_token: Access Token
        refresh_token: Refresh Token
        refresh_token_url: Refresh Token URL
        client_id: Client ID
        client_secret: Client Secret
    """

    class Meta:
        name = "OAuth_2.0_DataType"
        target_namespace = "urn:com.workday/bsvc"

    access_token: Optional[str] = field(
        default=None,
        metadata={
            "name": "Access_Token",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    refresh_token: Optional[str] = field(
        default=None,
        metadata={
            "name": "Refresh_Token",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    refresh_token_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "Refresh_Token_URL",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    client_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Client_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    client_secret: Optional[str] = field(
        default=None,
        metadata={
            "name": "Client_Secret",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class OmsEnvironmentObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "OMS_EnvironmentObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class PgpPrivateKeyPairObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "PGP_Private_Key_PairObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class PgpPublicKeyObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "PGP_Public_KeyObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ParameterInitializationOperatorObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Parameter_Initialization_OperatorObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class PartitionedBackgroundProcessObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Partitioned_Background_ProcessObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ProcessingFaultType:
    class Meta:
        name = "Processing_FaultType"
        target_namespace = "urn:com.workday/bsvc"

    detail_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Detail_Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class RestEndpointDataSourceObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "REST_Endpoint_Data_SourceObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class RestEndpointDataSourceDataType:
    """
    REST Endpoint Data Source Data element.

    Attributes:
        rest_endpoint: REST URL
        user_id: User Name
        password: Text attribute identifying Password.
        is_internal_url: REST Endpoint is internal to Workday
    """

    class Meta:
        name = "REST_Endpoint_Data_Source_DataType"
        target_namespace = "urn:com.workday/bsvc"

    rest_endpoint: Optional[str] = field(
        default=None,
        metadata={
            "name": "REST_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    user_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "User_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    is_internal_url: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isInternalURL",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferenceIdobjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Reference_IDObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferenceIdDataType:
    """
    Element containing reference ID and type data.

    Attributes:
        id: The Reference ID for the business object.
        new_id: A new Reference ID for the business object, used when updating Reference IDs.
        reference_id_type: The type of the Reference ID (e.g. Location_ID)
        referenced_object_descriptor: The descriptor for the business object.
    """

    class Meta:
        name = "Reference_ID_DataType"
        target_namespace = "urn:com.workday/bsvc"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    new_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "New_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    reference_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Type",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "max_length": 128,
        },
    )
    referenced_object_descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Referenced_Object_Descriptor",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferenceIndexObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
        parent_id: For types that require a parent reference, contains a unique identifier for an
            instance of a parent object.
        parent_type: For types that require a parent reference, the unique identifier type of a
            parent object.
    """

    class Meta:
        name = "Reference_IndexObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parent_id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_type: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferencedTaskObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Referenced_TaskObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ReportGroupObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Report_GroupObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ReportTagObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Report_TagObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class RepositoryDocumentAbstractObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Repository_Document__Abstract_ObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class RescindBusinessProcessDataType:
    """
    Provide additional details for the Business Process rescind.

    Attributes:
        comment: Comment
        suppress_notifications: Suppress Notifications
    """

    class Meta:
        name = "Rescind_Business_Process_DataType"
        target_namespace = "urn:com.workday/bsvc"

    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    suppress_notifications: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Suppress_Notifications",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ResponseFilterType:
    """
    Parameters that let you filter the data returned in the response.

    You can filter returned data by dates and page attributes.

    Attributes:
        as_of_effective_date: Indicates the date when application data, such as benefits and
            compensation, become effective (Also referred to as the Effective Moment). If you don't
            specify a date, this date defaults to today.{+4}
        as_of_entry_date_time: The date and time the data was entered into the system. (This field
            is also referred to as the Entry Moment). If the date isn't specified, the default date
            is the current date and time.
        page: The numbered page of data Workday returns in the response. The default page is the
            first page(Page = 1). For responses that contain more than one page of data, use this
            parameter to retrieve the additional pages of data. For example, set Page = 2 to
            retrieve the second page of data. Note: If you set the page parameter, you must also
            specify the "As_Of_Entry_Date" to ensure that the result set remains the same between
            your requests.
        count: Sets the number of objects to return within each response page. Set a value between 1
            and 999. The default value is 100.
    """

    class Meta:
        name = "Response_FilterType"
        target_namespace = "urn:com.workday/bsvc"

    as_of_effective_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "As_Of_Effective_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    as_of_entry_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "As_Of_Entry_DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    page: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Page",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    count: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 3,
            "fraction_digits": 0,
        },
    )


@dataclass
class ResponseFilterNoEntryMomentType:
    """
    Parameters that let you filter the data returned in the response.

    You can filter returned data by dates and page attributes.

    Attributes:
        as_of_effective_date: Indicates the date when application data, such as benefits and
            compensation, become effective (Also referred to as the Effective Moment). If you don't
            specify a date, this date defaults to today.{+4}
        as_of_entry_date_time: The date and time the data was entered into the system. (This field
            is also referred to as the Entry Moment). If the date isn't specified, the default date
            is the current date and time.
        page: The numbered page of data Workday returns in the response. The default page is the
            first page(Page = 1). For responses that contain more than one page of data, use this
            parameter to retrieve the additional pages of data. For example, set Page = 2 to
            retrieve the second page of data. Note: If you set the page parameter, you must also
            specify the "As_Of_Entry_Date" to ensure that the result set remains the same between
            your requests.
        count: Sets the number of objects to return within each response page. Set a value between 1
            and 999. The default value is 100.
    """

    class Meta:
        name = "Response_Filter__No_Entry_Moment_Type"
        target_namespace = "urn:com.workday/bsvc"

    as_of_effective_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "As_Of_Effective_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    as_of_entry_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "As_Of_Entry_DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    page: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Page",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    count: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 3,
            "fraction_digits": 0,
        },
    )


@dataclass
class ResponseResultsType:
    """
    The "Response_Results" element contains summary information about the data that has been
    returned from your request including "Total_Results", "Total_Pages", and the current "Page"
    returned.

    Attributes:
        total_results: The total number of results that your request returned.
        total_pages: The total number of pages requested. A page of data in a WWS has a 100 entry
            maximum.
        page_results: The number of results in the current page.
        page: The page number of the data the WWS returned for your request.
    """

    class Meta:
        name = "Response_ResultsType"
        target_namespace = "urn:com.workday/bsvc"

    total_results: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Total_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    total_pages: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Total_Pages",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    page_results: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Page_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    page: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Page",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )


@dataclass
class RoleObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "RoleObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SecurityGroupObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Security_GroupObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SendBackBusinessProcessDataType:
    """
    Element containing the data for the send back.

    Attributes:
        business_process_step_id: Specify the Reference ID for the business process step to which
            the business process will send back to.
        business_process_step_description: Workday won't save this data in any Workday fields. You
            can use this field to copy the business process step name and identify which business
            process step you list in the Business Process Step ID field.
        comment: Specify a comment to indicate why the business process is being send back.
    """

    class Meta:
        name = "Send_Back_Business_Process_DataType"
        target_namespace = "urn:com.workday/bsvc"

    business_process_step_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Business_Process_Step_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    business_process_step_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Business_Process_Step_Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comment",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SequenceGeneratorObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Sequence_GeneratorObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SequenceGeneratorLimitOverflowBehaviorObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Sequence_Generator_Limit_Overflow_BehaviorObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SimpleWorkDataRuntimeParameterNameType:
    """
    Parameter Name.

    Attributes:
        value
        label: Label
    """

    class Meta:
        name = "Simple_Work_Data_Runtime_Parameter_NameType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "name": "Label",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SubscriberObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "SubscriberObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SystemAccountObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "System_AccountObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SystemUserObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "System_UserObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class TemplateModelObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Template_ModelObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class TextAttributeType:
    """
    Text.

    Attributes:
        value
        sensitive: Sensitive
    """

    class Meta:
        name = "Text_AttributeType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    sensitive: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Sensitive",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class TimeZoneObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Time_ZoneObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ToDoObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "To_DoObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class TransactionLogTypeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Transaction_Log_TypeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class UniqueIdentifierObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Unique_IdentifierObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ValidationErrorType:
    class Meta:
        name = "Validation_ErrorType"
        target_namespace = "urn:com.workday/bsvc"

    message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    detail_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Detail_Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    xpath: Optional[str] = field(
        default=None,
        metadata={
            "name": "Xpath",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WebServiceApiVersionObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Web_Service_API_VersionObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WebServiceBackgroundProcessRuntimeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Web_Service_Background_Process_RuntimeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WebServiceDataSourceObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Web_Service_Data_SourceObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WebServiceInvocationTypeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Web_Service_Invocation_TypeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WebServiceOperationObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Web_Service_OperationObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WebServiceOperationReferenceDataType:
    """
    Reference element representing a unique instance of Web Service Operation.

    Attributes:
        web_service_name: Text attribute representing Name of a Web Service.
        web_service_operation_name: Text attribute representing Name of a Web Service Operation.
    """

    class Meta:
        name = "Web_Service_Operation_Reference_DataType"
        target_namespace = "urn:com.workday/bsvc"

    web_service_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Web_Service_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    web_service_operation_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Web_Service_Operation_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WorkdayAttachmentTransportProtocolDataType:
    """
    Workday Attachment Transport Protocol Data element.

    Attributes:
        attach_to_workday: Attach back to Workday
    """

    class Meta:
        name = "Workday_Attachment_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    attach_to_workday: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Attach_To_Workday",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WorkdayCommonHeaderType:
    class Meta:
        name = "Workday_Common_HeaderType"
        target_namespace = "urn:com.workday/bsvc"

    include_reference_descriptors_in_response: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Include_Reference_Descriptors_In_Response",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkerObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "WorkerObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WorkflowProcessParticipantObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Workflow_Process_ParticipantObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WorkflowStepObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Workflow_StepObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WorkflowStepTypeObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "Workflow_Step_TypeObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class XsltAttachmentTransformationObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "XSLT_Attachment_TransformationObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class X509PrivateKeyPairObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "x509_Private_Key_PairObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class X509PublicKeyObjectIdtype:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        value
        type_value: The unique identifier type. Each "ID" for an instance of an object contains a
            type and a value. A single instance of an object can have multiple "ID" but only a
            single "ID" per "type".  Some "types" require a reference to a parent instance.
    """

    class Meta:
        name = "x509_Public_KeyObjectIDType"
        target_namespace = "urn:com.workday/bsvc"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class AbstractExternalParameterObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Abstract_External_ParameterObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[AbstractExternalParameterObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ActionEventObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Action_EventObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ActionEventObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ApplicationInstanceExceptionsDataType:
    """
    Element containing application related exceptions data.

    Attributes:
        exception_data: Exception Data
    """

    class Meta:
        name = "Application_Instance_Exceptions_DataType"
        target_namespace = "urn:com.workday/bsvc"

    exception_data: list[ExceptionDataType] = field(
        default_factory=list,
        metadata={
            "name": "Exception_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class AuthenticationFault(AuthenticationFaultType):
    class Meta:
        name = "Authentication_Fault"
        namespace = "urn:com.workday/bsvc"


@dataclass
class BackgroundProcessMessageSeverityLevelObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Background_Process_Message_Severity_LevelObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[BackgroundProcessMessageSeverityLevelObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class BackgroundProcessRuntimeStatusObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Background_Process_Runtime_StatusObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[BackgroundProcessRuntimeStatusObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class BusinessObjectObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Business_ObjectObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[BusinessObjectObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class BusinessProcessTypeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Business_Process_TypeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[BusinessProcessTypeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ChecklistObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[ChecklistObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CloudCollectionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Cloud_CollectionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[CloudCollectionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CommentObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[CommentObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ConditionRuleObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Condition_RuleObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ConditionRuleObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CurrencyObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[CurrencyObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CustomBusinessFormLayoutObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Custom_Business_Form_LayoutObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[CustomBusinessFormLayoutObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CustomObjectObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Custom_ObjectObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[CustomObjectObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CustomReportDefinitionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Custom_Report_DefinitionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[CustomReportDefinitionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CustomReportTransformationObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Custom_Report_TransformationObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[CustomReportTransformationObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DateIntervalObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Date_IntervalObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[DateIntervalObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DeliveredBusinessFormLayoutObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Delivered_Business_Form_LayoutObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[DeliveredBusinessFormLayoutObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DisplayOptionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Display_OptionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[DisplayOptionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DocumentTagObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Document_TagObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[DocumentTagObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DocumentTypeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Document_TypeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[DocumentTypeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[EventObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventClassificationSubcategoryObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Event_Classification_SubcategoryObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[EventClassificationSubcategoryObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventInitializationDocumentsDataType:
    """
    Event Initialization Documents Data.

    Attributes:
        get_event_documents_document_id: Get Event Documents Document ID
        get_event_documents_data
        get_event_configurations_document_id: Get Event Configurations Document ID
        get_integration_systems_document_id: Get Integration Systems Document ID
    """

    class Meta:
        name = "Event_Initialization_Documents_DataType"
        target_namespace = "urn:com.workday/bsvc"

    get_event_documents_document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Get_Event_Documents_Document_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    get_event_documents_data: list[GetEventDocumentsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Get_Event_Documents_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    get_event_configurations_document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Get_Event_Configurations_Document_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    get_integration_systems_document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Get_Integration_Systems_Document_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventRecordActionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Event_Record_ActionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[EventRecordActionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventServiceObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Event_ServiceObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[EventServiceObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventTargetObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Event_TargetObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[EventTargetObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalFieldObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "External_FieldObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ExternalFieldObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalInstanceObjectType:
    """
    Contains a unique identifier for an instance of an object.

    Attributes:
        id
        descriptor: The "Descriptor" provides a human-readable, descriptive name for the business
            object. This "Descriptor" attribute should only be used as an informational description
            and not as data, an index or an identifier for integrations since descriptors can change
            from time to time in both format and value
    """

    class Meta:
        name = "External_Instance_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ExternalInstanceIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalPromptableObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "External_PromptableObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ExternalPromptableObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GenericDocumentBuilderAuditedObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Generic_Document_Builder__Audited_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[GenericDocumentBuilderAuditedObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HttpHeaderDataType:
    """HTTP Header Data."""

    class Meta:
        name = "HTTP_Header_DataType"
        target_namespace = "urn:com.workday/bsvc"

    http_header: list[HttpHeaderType] = field(
        default_factory=list,
        metadata={
            "name": "HTTP_Header",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class InstanceObjectType:
    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[InstanceIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegratableObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegratableObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAttachmentConfigurationDataType:
    """Integration Attachment Configuration Data Element."""

    class Meta:
        name = "Integration_Attachment_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    attachment_data: list[AttachmentDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Attachment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAttributeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_AttributeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationAttributeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDocumentFieldObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Document_FieldObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationDocumentFieldObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDocumentOptionValueObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Document_Option_ValueObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationDocumentOptionValueObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEsbInvocationAbstractObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_ESB_Invocation__Abstract_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationEsbInvocationAbstractObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEnumerationObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_EnumerationObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationEnumerationObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEnumerationDefinitionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Enumeration_DefinitionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationEnumerationDefinitionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEventAbstractObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Event__Abstract_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationEventAbstractObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationLaunchOptionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Launch_OptionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationLaunchOptionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationRepositoryDocumentObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Repository_DocumentObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationRepositoryDocumentObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSequenceGeneratorServiceObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Sequence_Generator_ServiceObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationSequenceGeneratorServiceObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSequencerObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_SequencerObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationSequencerObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationServiceObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_ServiceObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationServiceObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_SystemObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationSystemObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemIdentifierObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_System_IdentifierObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationSystemIdentifierObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemAuditedObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_System__Audited_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationSystemAuditedObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationTagObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_TagObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationTagObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationTemplateObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_TemplateObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationTemplateObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationTemplateAbstractObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Integration_Template__Abstract_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[IntegrationTemplateAbstractObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class InvalidReferenceIdResponseType:
    """
    Invalid Reference ID Response.

    Attributes:
        invalid_reference: Invalid Reference ID Data
    """

    class Meta:
        name = "Invalid_Reference_ID_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    invalid_reference: list[InvalidReferenceIdDataType] = field(
        default_factory=list,
        metadata={
            "name": "Invalid_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchParameterObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Launch_ParameterObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[LaunchParameterObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class MimeTypeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Mime_TypeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[MimeTypeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class OmsEnvironmentObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "OMS_EnvironmentObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[OmsEnvironmentObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PgpPrivateKeyPairObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "PGP_Private_Key_PairObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[PgpPrivateKeyPairObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PgpPublicKeyObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "PGP_Public_KeyObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[PgpPublicKeyObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ParameterInitializationOperatorObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Parameter_Initialization_OperatorObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ParameterInitializationOperatorObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PartitionedBackgroundProcessObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Partitioned_Background_ProcessObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[PartitionedBackgroundProcessObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ProcessingFault(ProcessingFaultType):
    class Meta:
        name = "Processing_Fault"
        namespace = "urn:com.workday/bsvc"


@dataclass
class RestEndpointDataSourceObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "REST_Endpoint_Data_SourceObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[RestEndpointDataSourceObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferenceIdobjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Reference_IDObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ReferenceIdobjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferenceIndexObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Reference_IndexObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ReferenceIndexObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferencedTaskObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Referenced_TaskObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ReferencedTaskObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReportGroupObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Report_GroupObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ReportGroupObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReportTagObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Report_TagObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ReportTagObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class RepositoryDocumentAbstractObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Repository_Document__Abstract_ObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[RepositoryDocumentAbstractObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class RoleObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[RoleObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SecurityGroupObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Security_GroupObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[SecurityGroupObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SequenceGeneratorObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Sequence_GeneratorObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[SequenceGeneratorObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SequenceGeneratorLimitOverflowBehaviorObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Sequence_Generator_Limit_Overflow_BehaviorObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[SequenceGeneratorLimitOverflowBehaviorObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SubscriberObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[SubscriberObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SystemAccountObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "System_AccountObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[SystemAccountObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SystemUserObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "System_UserObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[SystemUserObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class TemplateModelObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Template_ModelObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[TemplateModelObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class TimeZoneObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Time_ZoneObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[TimeZoneObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ToDoObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "To_DoObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[ToDoObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class TransactionLogTypeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Transaction_Log_TypeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[TransactionLogTypeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class UniqueIdentifierObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Unique_IdentifierObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[UniqueIdentifierObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ValidationFaultType:
    class Meta:
        name = "Validation_FaultType"
        target_namespace = "urn:com.workday/bsvc"

    validation_error: list[ValidationErrorType] = field(
        default_factory=list,
        metadata={
            "name": "Validation_Error",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WebServiceApiVersionObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Web_Service_API_VersionObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WebServiceApiVersionObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WebServiceBackgroundProcessRuntimeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Web_Service_Background_Process_RuntimeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WebServiceBackgroundProcessRuntimeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WebServiceDataSourceObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Web_Service_Data_SourceObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WebServiceDataSourceObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WebServiceInvocationTypeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Web_Service_Invocation_TypeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WebServiceInvocationTypeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WebServiceOperationObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Web_Service_OperationObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WebServiceOperationObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkdayCommonHeader(WorkdayCommonHeaderType):
    class Meta:
        name = "Workday_Common_Header"
        namespace = "urn:com.workday/bsvc"


@dataclass
class WorkdayWebServiceTransportProtocolDataType:
    """Workday Web Service Transport Protocol Data element."""

    class Meta:
        name = "Workday_Web_Service_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    web_service_operation_reference_data: Optional[WebServiceOperationReferenceDataType] = field(
        default=None,
        metadata={
            "name": "Web_Service_Operation_Reference_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class WorkerObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    id: list[WorkerObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkflowProcessParticipantObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Workflow_Process_ParticipantObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WorkflowProcessParticipantObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkflowStepObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Workflow_StepObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WorkflowStepObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkflowStepTypeObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "Workflow_Step_TypeObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[WorkflowStepTypeObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class XsltAttachmentTransformationObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "XSLT_Attachment_TransformationObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[XsltAttachmentTransformationObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class X509PrivateKeyPairObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "x509_Private_Key_PairObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[X509PrivateKeyPairObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class X509PublicKeyObjectType:
    """
    Attributes:
        id
        descriptor: Display information used to describe an instance of an object. This 'optional'
            information is for outbound descriptive purposes only and is not processed on inbound
            Workday Web Services requests.
    """

    class Meta:
        name = "x509_Public_KeyObjectType"
        target_namespace = "urn:com.workday/bsvc"

    id: list[X509PublicKeyObjectIdtype] = field(
        default_factory=list,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class As2SettingsDataType:
    """
    AS2 Settings Data.

    Attributes:
        as2_from_id: From ID
        as2_id: AS2 ID
        public_key_for_encryption_reference: Encryption Certificate based on x509 specification
        private_key_pair_for_signing_reference: Certificate for digital signature
        public_key_for_ssl_reference: Certificate reference for SSH Authentication
        public_key_for_ssl_accept_reference: Certificate reference for accept SSL
    """

    class Meta:
        name = "AS2_Settings_DataType"
        target_namespace = "urn:com.workday/bsvc"

    as2_from_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AS2_From_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    as2_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AS2_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    public_key_for_encryption_reference: Optional[X509PublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Public_Key_for_Encryption_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    private_key_pair_for_signing_reference: Optional[X509PrivateKeyPairObjectType] = field(
        default=None,
        metadata={
            "name": "Private_Key_Pair_for_Signing_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    public_key_for_ssl_reference: Optional[X509PublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Public_Key_for_SSL_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    public_key_for_ssl_accept_reference: Optional[X509PublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Public_Key_for_SSL_Accept_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class AbstractSequenceGeneratorDataType:
    """
    Sequence Generator Data.

    Attributes:
        sequence_id: Sequence Generator Reference ID.
        sequence_name: Sequence Name
        start_number: Start Number
        increment_by: Increment By
        restart_date_interval_reference: Restart Date Interval Reference
        use_time_zone_reference: Use Time Zone Reference
        last_number_used: Last Number Used
        last_date_time_used: Last DateTime Used
        padding_with_zero: Padding With Zero
        format: Format
        low_volume: Low Volume. Ignore for gapless.
        id_limit_overflow_behavior_reference: ID Limit Overflow Behavior with the options to
            Automatically Ignore Padding, Allow Overflow with Truncated Sequences or Stop
            Processing.
        overflow_notification_group_reference: Sequence Generator Owner to be notified when there is
            an upcoming sequence generator overflow.
    """

    class Meta:
        name = "Abstract_Sequence_Generator_DataType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sequence_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sequence_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sequence_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    start_number: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Start_Number",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    increment_by: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Increment_By",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    restart_date_interval_reference: Optional[DateIntervalObjectType] = field(
        default=None,
        metadata={
            "name": "Restart_Date_Interval_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    use_time_zone_reference: Optional[TimeZoneObjectType] = field(
        default=None,
        metadata={
            "name": "Use_Time_Zone_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    last_number_used: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Last_Number_Used",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    last_date_time_used: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Last_DateTime_Used",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    padding_with_zero: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Padding_With_Zero",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 2,
            "fraction_digits": 0,
        },
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "name": "Format",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    low_volume: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Low_Volume",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    id_limit_overflow_behavior_reference: Optional[
        SequenceGeneratorLimitOverflowBehaviorObjectType
    ] = field(
        default=None,
        metadata={
            "name": "ID_Limit_Overflow_Behavior_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    overflow_notification_group_reference: list[SecurityGroupObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Overflow_Notification_Group_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ApplicationInstanceRelatedExceptionsDataType:
    """
    Element containing Exceptions Data.

    Attributes:
        exceptions_data: Exceptions Data
    """

    class Meta:
        name = "Application_Instance_Related_Exceptions_DataType"
        target_namespace = "urn:com.workday/bsvc"

    exceptions_data: list[ApplicationInstanceExceptionsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Exceptions_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ApproveBusinessProcessRequestType:
    """
    Top-level request element for the Approve Business Process operation.

    Attributes:
        event_reference: A reference to a business process event. The reference can come from a
            Reference ID or Workday ID.
        approve_business_process_data: Element containing the data for the Approval (Comment)
        version
    """

    class Meta:
        name = "Approve_Business_Process_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    approve_business_process_data: Optional[BusinessProcessDataType] = field(
        default=None,
        metadata={
            "name": "Approve_Business_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ApproveBusinessProcessResponseType:
    """
    Wrapper that contains all sub response elements.

    Attributes:
        event_reference: A reference to a business process event. The reference can come from a
            Reference ID or Workday ID.
        version
    """

    class Meta:
        name = "Approve_Business_Process_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class AwaitingTaskDataType:
    """
    This element is wrapper for Event data.

    Attributes:
        task_reference: The reference information for this task.
        comment_reference: The references to the comments for this task.
        task_status_reference: The reference information for the status of this task.
        assignment_date: The assignment date for this task.
        due_date: The due date for the task.
        awaiting_person_reference: The reference(s) to the person awaiting this task.
    """

    class Meta:
        name = "Awaiting_Task_DataType"
        target_namespace = "urn:com.workday/bsvc"

    task_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Task_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    comment_reference: list[CommentObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Comment_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    task_status_reference: Optional[EventRecordActionObjectType] = field(
        default=None,
        metadata={
            "name": "Task_Status_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    assignment_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Assignment_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    due_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Due_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    awaiting_person_reference: list[UniqueIdentifierObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Awaiting_Person_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CancelBusinessProcessRequestType:
    """
    Cancel Business Process Request.

    Attributes:
        event_reference: Event Reference
        cancel_business_process_data: Cancel Business Process Data
        version
    """

    class Meta:
        name = "Cancel_Business_Process_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    cancel_business_process_data: Optional[CancelBusinessProcessDataType] = field(
        default=None,
        metadata={
            "name": "Cancel_Business_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CancelBusinessProcessResponseType:
    """
    Cancel Business Process Response.

    Attributes:
        event_reference: Event Reference
        version
    """

    class Meta:
        name = "Cancel_Business_Process_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CancelIntegrationEventRequestType:
    """
    Cancel Integration Event Request.

    Attributes:
        integration_event_reference: Reference element representing a unique instance of Integration
            Event.
        version
    """

    class Meta:
        name = "Cancel_Integration_Event_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CancelIntegrationEventResponseType:
    """
    Cancel Integration Event Response.

    Attributes:
        integration_event_reference: Reference element representing a unique instance of Integration
            Event.
        version
    """

    class Meta:
        name = "Cancel_Integration_Event_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CopyOfIntegrationAbstractValueDataType:
    """
    Container element for an Abstract Value.

    Attributes:
        text: Text
        date: Date
        date_time: DateTime
        numeric: Numeric
        boolean: Boolean
        instance_reference: Instance Reference
    """

    class Meta:
        name = "Copy_of_Integration_Abstract_Value_DataType"
        target_namespace = "urn:com.workday/bsvc"

    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class CustomReportTransformationDataType:
    """
    Custom Report Transformation Data element.

    Attributes:
        custom_report_transformation_reference: Represents a unique reference to a custom report
            transformation.
    """

    class Meta:
        name = "Custom_Report_Transformation_DataType"
        target_namespace = "urn:com.workday/bsvc"

    custom_report_transformation_reference: Optional[CustomReportTransformationObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Report_Transformation_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DeleteIntegrationSystemRequestType:
    """
    Delete Integration System Request.

    Attributes:
        integration_system_reference: Integration System Delete Integration System Request
        version
    """

    class Meta:
        name = "Delete_Integration_System_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DeleteIntegrationSystemResponseType:
    """
    Delete Integration System Response.

    Attributes:
        integration_system_reference: Integration System (Audited)
        version
    """

    class Meta:
        name = "Delete_Integration_System_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DeliveredTransformationDataType:
    """
    Delivered Transformation Data element.

    Attributes:
        workday_transformation_reference: Represents a unique reference to a Workday delivered
            transformation.
        template_model_reference: Represents a unique reference to a Template Model. Template Models
            are used in conjunction with Workday delivered transformations to modify the layout of
            the uploaded templates.
        custom_object_reference: Custom Object Reference
    """

    class Meta:
        name = "Delivered_Transformation_DataType"
        target_namespace = "urn:com.workday/bsvc"

    workday_transformation_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Workday_Transformation_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    template_model_reference: Optional[TemplateModelObjectType] = field(
        default=None,
        metadata={
            "name": "Template_Model_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_object_reference: Optional[CustomObjectObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DenyBusinessProcessRequestType:
    """
    Top-level request element for the Deny Business Process operation.

    Attributes:
        event_reference: A reference to a business process event. The reference can come from a
            Reference ID or Workday ID.
        deny_business_process_data: Element containing the data for the Denial (Comment)
        version
    """

    class Meta:
        name = "Deny_Business_Process_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    deny_business_process_data: Optional[BusinessProcessDataType] = field(
        default=None,
        metadata={
            "name": "Deny_Business_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DenyBusinessProcessResponseType:
    """
    Wrapper that contains all sub response elements.

    Attributes:
        event_reference: A reference to a business process event. The reference can come from a
            Reference ID or Workday ID.
        version
    """

    class Meta:
        name = "Deny_Business_Process_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EibAttachmentDataSourceDataType:
    """
    Attachment Data Source Data element.

    Attributes:
        load_from_attachment: Load From Attachment
        web_service_operation_reference: Web Service Operation Reference
        custom_object_reference: Custom Object Reference
    """

    class Meta:
        name = "EIB_Attachment_Data_Source_DataType"
        target_namespace = "urn:com.workday/bsvc"

    load_from_attachment: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Load_From_Attachment",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    web_service_operation_reference: Optional[WebServiceOperationObjectType] = field(
        default=None,
        metadata={
            "name": "Web_Service_Operation_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_object_reference: Optional[CustomObjectObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EibExtensibilityApiTransportProtocolDataType:
    """
    Extensibility API Transport Protocol Data element.

    Attributes:
        custom_object_reference: Custom Object Reference
    """

    class Meta:
        name = "EIB_Extensibility_API_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    custom_object_reference: Optional[CustomObjectObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventRequestReferencesType:
    """
    This element contains references to Event for data retrieval.

    Attributes:
        event_reference: This element contains references to Event for data retrieval.
    """

    class Meta:
        name = "Event_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: list[ActionEventObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class EventWwstype:
    """
    This element is wrapper for Event data.

    Attributes:
        event_reference: This is the Reference Element containing all Integration IDs (Workday ID
            and Reference IDs) for the Event.
        event_detail_data: This element is wrapper for Event data.
    """

    class Meta:
        name = "Event_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_detail_data: Optional["EventDetailDataType"] = field(
        default=None,
        metadata={
            "name": "Event_Detail_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalEndpointDataType:
    """
    Endpoint Info Data element.

    Attributes:
        web_service_api_version_reference: Version Reference
        use_deployed_service_endpoint: Use the endpoint defined by the Integration
        subscriber_url: Use this specific endpoint
        subscription_user_name: Text attribute identifying User Name.
        subscription_password: Text attribute identifying Password.
        disable_endpoint: Use to disable sending notifications to the external system.
        oms_environment_reference: Unique identifier for an OMS Environment reference
    """

    class Meta:
        name = "External_Endpoint_DataType"
        target_namespace = "urn:com.workday/bsvc"

    web_service_api_version_reference: Optional[WebServiceApiVersionObjectType] = field(
        default=None,
        metadata={
            "name": "Web_Service_API_Version_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    use_deployed_service_endpoint: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Deployed_Service_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscriber_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "Subscriber_URL",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_user_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Subscription_User_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Subscription_Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    disable_endpoint: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Disable_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    oms_environment_reference: list[OmsEnvironmentObjectType] = field(
        default_factory=list,
        metadata={
            "name": "OMS_Environment_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExternalFieldAddOrReferenceType:
    """
    Container element for External Field definition.

    Attributes:
        class_report_field_reference: Unique reference to Class Report Field (if known).
        calculated_field_class_name: For Calculated Fields (not Class Report Fields), Class Name.
        calculated_field_reference_id: Calculated Field Reference ID
        calculated_field_name: For Calculated Fields (not Class Report Fields), Name.
        business_object_reference: For Calculated Fields and Custom Fields (not Class Report
            Fields), Business Object Reference.
    """

    class Meta:
        name = "External_Field_Add_or_ReferenceType"
        target_namespace = "urn:com.workday/bsvc"

    class_report_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Class_Report_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    calculated_field_class_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Calculated_Field_Class_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    calculated_field_reference_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Calculated_Field_Reference_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    calculated_field_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Calculated_Field_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    business_object_reference: Optional[BusinessObjectObjectType] = field(
        default=None,
        metadata={
            "name": "Business_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetIntegrationSystemsCriteriaType:
    """
    Criteria for filtering the Integration Systems that get returned in the response.

    Attributes:
        integration_template_reference: Integration Template Reference
        workday_account_reference: Workday Account Reference
        cloud_collection_reference: Cloud Collection Reference
    """

    class Meta:
        name = "Get_Integration_Systems_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    integration_template_reference: Optional[IntegrationTemplateAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Template_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workday_account_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "Workday_Account_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    cloud_collection_reference: Optional[CloudCollectionObjectType] = field(
        default=None,
        metadata={
            "name": "Cloud_Collection_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HttpTransportProtocolDataType:
    """
    HTTP Transport Protocol Data element.

    Attributes:
        http_address: HTTP Address
        http_delivery_method_reference: HTTP Method Type
        web_service_invocation_type_reference: Reference element representing a unique instance of
            Web Service Invocation Type.
        http_header_data
        user_id: Text attribute identifying User Name.
        password: Text attribute identifying Password.
        oauth_2_0_data
    """

    class Meta:
        name = "HTTP_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    http_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "HTTP_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    http_delivery_method_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "HTTP_Delivery_Method_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    web_service_invocation_type_reference: Optional[WebServiceInvocationTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Web_Service_Invocation_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    http_header_data: Optional[HttpHeaderDataType] = field(
        default=None,
        metadata={
            "name": "HTTP_Header_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    user_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "User_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    oauth_2_0_data: Optional[Oauth20DataType] = field(
        default=None,
        metadata={
            "name": "OAuth_2.0_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HideWorkdayDeliveredReportDataType:
    """
    Defines the data used for processing.

    Attributes:
        workday_delivered_report_reference: Contains references to the Workday delivered reports to
            hide
    """

    class Meta:
        name = "Hide_Workday_Delivered_Report_DataType"
        target_namespace = "urn:com.workday/bsvc"

    workday_delivered_report_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Workday_Delivered_Report_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HideWorkdayDeliveredReportRequestReferencesType:
    """
    Contains references that identify hidden Workday delivered reports.

    Attributes:
        hide_workday_delivered_report_reference: Contains references that identify hidden Workday
            delivered reports.
    """

    class Meta:
        name = "Hide_Workday_Delivered_Report_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    hide_workday_delivered_report_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Hide_Workday_Delivered_Report_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ImportProcessDataType:
    """
    Import Process Data.

    Attributes:
        process_description: Description of the Import Process event
        percent_complete: Percent Complete of the job
        process_completed_date_time: Date/Time representing the moment the job completed
        import_header_reference: Header instance associated to Import Process
        status_reference: Returns status associated to Import Process
        has_messages: Indicated whether Import Process Event has messages associated with it
        validate_only: Indicates if this process was started with the "validate-only" option.
    """

    class Meta:
        name = "Import_Process_DataType"
        target_namespace = "urn:com.workday/bsvc"

    process_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Process_Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    percent_complete: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Percent_Complete",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 7,
            "fraction_digits": 4,
        },
    )
    process_completed_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Process_Completed_DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    import_header_reference: Optional[InstanceObjectType] = field(
        default=None,
        metadata={
            "name": "Import_Header_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    status_reference: Optional[BackgroundProcessRuntimeStatusObjectType] = field(
        default=None,
        metadata={
            "name": "Status_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    has_messages: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Has_Messages",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    validate_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Validate_Only",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ImportProcessMessageType:
    """
    Message.

    Attributes:
        import_process_message_reference: Message Reference
        import_process_message_data: Message Data
    """

    class Meta:
        name = "Import_Process_MessageType"
        target_namespace = "urn:com.workday/bsvc"

    import_process_message_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Import_Process_Message_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    import_process_message_data: Optional[BackgroundProcessMessageDataWstype] = field(
        default=None,
        metadata={
            "name": "Import_Process_Message_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ImportProcessMessagesRequestCriteriaType:
    """
    Request Criteria.

    Attributes:
        import_process_reference: Import Process Reference
    """

    class Meta:
        name = "Import_Process_Messages_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    import_process_reference: Optional[WebServiceBackgroundProcessRuntimeObjectType] = field(
        default=None,
        metadata={
            "name": "Import_Process_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ImportProcessRequestReferencesType:
    """
    Import Process Request References.

    Attributes:
        import_process_reference: Internal method binding only..  This is a reference to the job
            that was created as the result of a Import Process Document load.
    """

    class Meta:
        name = "Import_Process_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    import_process_reference: Optional[WebServiceBackgroundProcessRuntimeObjectType] = field(
        default=None,
        metadata={
            "name": "Import_Process_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IncrementSequenceGeneratorRequestType:
    """
    Request element for Increment of Sequence Generator.

    Attributes:
        sequence_generator_reference: Sequence Generator Reference
        version
    """

    class Meta:
        name = "Increment_Sequence_Generator_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator_reference: Optional[SequenceGeneratorObjectType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IncrementSequenceGeneratorResponseType:
    """
    Response element for Increment of Sequence Generator.

    Attributes:
        sequence_generator_reference: Sequence Generator Reference
        sequenced_value: Sequenced Value
        version
    """

    class Meta:
        name = "Increment_Sequence_Generator_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator_reference: Optional[SequenceGeneratorObjectType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sequenced_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sequenced_Value",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAbstractValueDataType:
    """
    Container element for an Abstract Value.

    Attributes:
        text: Text
        date: Date
        date_time: DateTime
        numeric: Numeric
        boolean: Boolean
        instance_reference: Instance Reference
    """

    class Meta:
        name = "Integration_Abstract_Value_DataType"
        target_namespace = "urn:com.workday/bsvc"

    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAttachmentDataType:
    """
    Encapsulating element containing all Integration Attachment data.

    Attributes:
        file_id: Text attribute identifying a unique ID for Attachment.
        file_content: File content in binary format.
        content_type_reference: Reference element identifying a unique instance of Content Type of
            the Attachment.
        comments: Comment
        content_type: Text attribute identifying Content Type of the Attachment.
        filename: Text attribute identifying Filename of the Attachment.
        encoding: Text attribute identifying Encoding of the Attachment.
        compressed: Boolean attribute identifying whether the Attachment is compressed.
    """

    class Meta:
        name = "Integration_Attachment_DataType"
        target_namespace = "urn:com.workday/bsvc"

    file_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "File_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    file_content: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "File_Content",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "format": "base64",
        },
    )
    content_type_reference: Optional[MimeTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Content_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Content_Type",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 80,
        },
    )
    filename: Optional[str] = field(
        default=None,
        metadata={
            "name": "Filename",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 255,
        },
    )
    encoding: Optional[str] = field(
        default=None,
        metadata={
            "name": "Encoding",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    compressed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Compressed",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAttributeDataType:
    """
    Container element for definitions of custom Integration Attributes associated to this System.

    Attributes:
        order: Order
        name: Attribute Name
        description: Description
        data_type_external_field_reference: Data Type defining Attribute
        data_type_enumeration_definition_reference: Data Type of Attribute (e.g. structure) defined
            by an Integration Enumeration Definition.
        multi_select: This option allows enumerations to have multiple instances associated with it.
            It only works for enumeration data types.
        display_option_reference: Display Option Reference
    """

    class Meta:
        name = "Integration_Attribute_DataType"
        target_namespace = "urn:com.workday/bsvc"

    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "max_length": 6,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    data_type_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Data_Type_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    data_type_enumeration_definition_reference: Optional[
        IntegrationEnumerationDefinitionObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Data_Type_Enumeration_Definition_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    multi_select: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Multi-Select",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    display_option_reference: list[DisplayOptionObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Display_Option_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationAttributeValueDataWwstype:
    """
    Contains Integration Attributes Value and OMS Environment restriction for above Attribute and
    Integration System.

    Attributes:
        text: If Attribute is defined as a Text attribute, this will contain the Value assigned to
            it for appropriate Integration System.
        date: If Attribute is defined as a Date attribute, this will contain the Value assigned to
            it for appropriate Integration System.
        date_time: If Attribute is defined as a DateTime attribute, this will contain the Value
            assigned to it for appropriate Integration System.
        numeric: If Attribute is defined as a Numeric or Currency attribute, this will contain the
            Value assigned to it for appropriate Integration System.
        boolean: If Attribute is defined as a Boolean attribute, this will contain the Value
            assigned to it for appropriate Integration System.
        instance_reference: If Attribute is defined as an Instance Set, this will contain the
            Instance assigned to it for appropriate Integration System.
        environment_reference: Unique identifier for an OMS Environment reference
    """

    class Meta:
        name = "Integration_Attribute_Value_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    environment_reference: list[OmsEnvironmentObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Environment_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationCustomObjectAliasConfigurationDataType:
    """
    Integration Custom Object Field Configuration Data.

    Attributes:
        custom_object_alias_reference: Field Extension Alias Reference
        custom_object_reference: Custom Field Reference
        capture_multiple_values: Capture Multiple Values
        custom_object_rest_url: Custom Object REST URL Endpoint
        multiple_custom_object_rest_url: Multiple Custom Object REST URL Endpoint
    """

    class Meta:
        name = "Integration_Custom_Object_Alias_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    custom_object_alias_reference: Optional[IntegrationDocumentFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Object_Alias_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    custom_object_reference: Optional[CustomObjectObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    capture_multiple_values: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Capture_Multiple_Values",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_object_rest_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "Custom_Object_REST_URL",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    multiple_custom_object_rest_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "Multiple_Custom_Object_REST_URL",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDataChangeConfigurationDataType:
    """
    Container element for data related to a Data Change Service and its use within an Integration
    System.

    Attributes:
        external_field_reference: The External Fields (e.g. Calculated Field or Class Report Field)
            that are needed to determine if a Data Change has occurred.
    """

    class Meta:
        name = "Integration_Data_Change_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    external_field_reference: list[ExternalFieldObjectType] = field(
        default_factory=list,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDocumentFieldOptionsType:
    """
    Integration Document Field Options.

    Attributes:
        integration_document_option_value_reference: Integration Document Field Option Values
    """

    class Meta:
        name = "Integration_Document_Field_OptionsType"
        target_namespace = "urn:com.workday/bsvc"

    integration_document_option_value_reference: list[IntegrationDocumentOptionValueObjectType] = (
        field(
            default_factory=list,
            metadata={
                "name": "Integration_Document_Option_Value_Reference",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )


@dataclass
class IntegrationDocumentStackDataType:
    """
    Integration Document Stacks for Integration Document Field Configuration Data.

    Attributes:
        stack_level: This represents the depth for this Integration Document Stack
        integration_document_field_reference: This represents the field that is directly above the
            current field
    """

    class Meta:
        name = "Integration_Document_Stack_DataType"
        target_namespace = "urn:com.workday/bsvc"

    stack_level: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Stack_Level",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    integration_document_field_reference: Optional[IntegrationDocumentFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Document_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationEventRequestCriteriaType:
    """
    Criteria for filtering the Integration Events that get returned in the response.

    Attributes:
        integration_system_reference: Integration System Reference
        integration_event_status_reference: Integration Event Status Reference (e.g. Completed,
            Failed, etc.)
        sent_after: Sent After (DateTime)
        sent_before: Sent Before (DateTime)
    """

    class Meta:
        name = "Integration_Event_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_event_status_reference: list[BackgroundProcessRuntimeStatusObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Event_Status_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sent_after: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Sent_After",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sent_before: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Sent_Before",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEventRequestReferencesType:
    """
    Integration Event Request References.

    Attributes:
        integration_event_reference: Integration Event Reference
        ignore_invalid_references
    """

    class Meta:
        name = "Integration_Event_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: list[IntegrationEsbInvocationAbstractObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )
    ignore_invalid_references: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Ignore_Invalid_References",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationMapDataType:
    """
    Container element for definitions of custom Integration Maps associated to this System.

    Attributes:
        order: Order
        name: Map Name
        description: Description
        internal_value_data_type_external_field_reference: Data Type defining Internal Value
        internal_value_data_type_integration_enumeration_reference: Data Type defining Internal
            Value
        internal_value_display_option_reference: Display Option Reference
        external_value_data_type_external_field_reference: Data Type defining External Value
        external_value_data_type_integration_enumeration_reference: Data Type defining External
            Value
        external_value_display_option_reference: Display Option Reference
    """

    class Meta:
        name = "Integration_Map_DataType"
        target_namespace = "urn:com.workday/bsvc"

    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "max_length": 6,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    internal_value_data_type_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Internal_Value_Data_Type_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    internal_value_data_type_integration_enumeration_reference: Optional[
        IntegrationEnumerationDefinitionObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Internal_Value_Data_Type_Integration_Enumeration_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    internal_value_display_option_reference: list[DisplayOptionObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Internal_Value_Display_Option_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_value_data_type_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Value_Data_Type_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_value_data_type_integration_enumeration_reference: Optional[
        IntegrationEnumerationDefinitionObjectType
    ] = field(
        default=None,
        metadata={
            "name": "External_Value_Data_Type_Integration_Enumeration_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_value_display_option_reference: list[DisplayOptionObjectType] = field(
        default_factory=list,
        metadata={
            "name": "External_Value_Display_Option_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationMessageDetailDataType:
    """
    Element for Messages related to Background Process Instances.

    Attributes:
        timestamp: Timestamp of Message
        severity_level_reference: Reference element representing a unique instance of Integration
            Message Severity Level.
        message_summary: Text attribute identifying the Summary of the Integration Message.
        message_detail: Text attribute identifying the Detail of the Integration Message.
        message_target_reference: A Reference to an instance within the Workday system that is
            related to this message.
    """

    class Meta:
        name = "Integration_Message_Detail_DataType"
        target_namespace = "urn:com.workday/bsvc"

    timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Timestamp",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    severity_level_reference: Optional[BackgroundProcessMessageSeverityLevelObjectType] = field(
        default=None,
        metadata={
            "name": "Severity_Level_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    message_summary: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message_Summary",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    message_detail: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message_Detail",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    message_target_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Message_Target_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationNotificationIntegrationConditionDataType:
    """
    Element containing the conditions to be evaluated for a Notification.

    Attributes:
        condition_rule_reference: Condition Rule Reference
    """

    class Meta:
        name = "Integration_Notification_Integration_Condition_DataType"
        target_namespace = "urn:com.workday/bsvc"

    condition_rule_reference: Optional[ConditionRuleObjectType] = field(
        default=None,
        metadata={
            "name": "Condition_Rule_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationReportFieldConfigurationDataType:
    """
    Integration Report Field Configuration Data.

    Attributes:
        report_alias_reference: Document Field Reference
        custom_report_definition_reference: Custom Report Definition to assign to Report Service
            Configuration
        rest_endpoint: Base REST Endpoint for Custom Report.  This attribute is for view purposes
            only based on the Custom Report Definition.
    """

    class Meta:
        name = "Integration_Report_Field_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    report_alias_reference: Optional[IntegrationDocumentFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Report_Alias_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    custom_report_definition_reference: Optional[CustomReportDefinitionObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Report_Definition_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    rest_endpoint: Optional[str] = field(
        default=None,
        metadata={
            "name": "REST_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationRepositoryDocumentDataType:
    """
    Encapsulating element containing all Integration Repository Document data.

    Attributes:
        file_size: Numeric attribute representing the Size (in Bytes) of the Repository document.
        content_type_reference: Reference element identifying a unique instance of Content Type of
            the Attachment.
        content_type: The Content Type of the document.  Valid values defined in RFC 822, including
            type, subtype, and parameter.
        document_type_reference: Reference element identifying a unique instance of Document Type of
            the Repository document.
        expiration_timestamp: DateTime attribute representing the Expiration Timestamp of the
            Repository document.
        owner_reference: Unique identifier for a System User reference
        document_tag_reference: Document Tag(s) associated with Repository Document
        custom_document_tag: Custom Document Tag
        secured_instance_reference: For Documents attached to an Integration Template utilizing
            Document Security, this Instance Reference identifies the secured instace(s) to be
            evaluated against the Document Security task.
        document_id: A unique ID for Repository document.
        file_name: Text attribute for Repository document.
    """

    class Meta:
        name = "Integration_Repository_Document_DataType"
        target_namespace = "urn:com.workday/bsvc"

    file_size: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "File_Size",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    content_type_reference: Optional[MimeTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Content_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Content_Type",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 80,
        },
    )
    document_type_reference: Optional[DocumentTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Document_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    expiration_timestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Expiration_Timestamp",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    owner_reference: Optional[SystemAccountObjectType] = field(
        default=None,
        metadata={
            "name": "Owner_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    document_tag_reference: list[DocumentTagObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Document_Tag_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_document_tag: list[str] = field(
        default_factory=list,
        metadata={
            "name": "Custom_Document_Tag",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    secured_instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Secured_Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Document_ID",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 513,
        },
    )
    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "File_Name",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationRuntimeParameterDataType:
    """
    Integration Runtime Parameter Data.

    Attributes:
        launch_configurable_name: Launch Configurable Name
        parameter_name
        text
        date: Date
        boolean: Boolean
        instance_set_reference: Instance Set Reference
    """

    class Meta:
        name = "Integration_Runtime_Parameter_DataType"
        target_namespace = "urn:com.workday/bsvc"

    launch_configurable_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Launch_Configurable_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_name: list[SimpleWorkDataRuntimeParameterNameType] = field(
        default_factory=list,
        metadata={
            "name": "Parameter_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    text: list[TextAttributeType] = field(
        default_factory=list,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    instance_set_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Instance_Set_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSequenceGeneratorConfigurationDataType:
    """
    Container element for data related to a Sequence Generator Service and its use within an
    Integration System.

    Attributes:
        integration_sequencer_reference: Integration Sequencer reference.
        sequence_generator_reference: Sequence Generator reference.
        oms_environment_reference: Environment Reference
    """

    class Meta:
        name = "Integration_Sequence_Generator_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_sequencer_reference: Optional[IntegrationSequencerObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Sequencer_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    sequence_generator_reference: Optional[SequenceGeneratorObjectType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    oms_environment_reference: list[OmsEnvironmentObjectType] = field(
        default_factory=list,
        metadata={
            "name": "OMS_Environment_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSequencerGeneratedSequenceDataType:
    """
    Integration Sequencer Generated Sequence Data.

    Attributes:
        integration_sequencer_reference: Integration Sequencer Reference
        sequenced_value: Sequenced Value
    """

    class Meta:
        name = "Integration_Sequencer_Generated_Sequence_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_sequencer_reference: Optional[IntegrationSequencerObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Sequencer_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sequenced_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sequenced_Value",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemContactDataWwstype:
    """
    Element containing data for Contacts related to the Integration System.

    Attributes:
        integration_system_contact_reference: Integration System Contact instance for Integration
            System (Audited)
        description: Text Attribute representing the description of the Contact for the Integration
            System Contact instance for Integration System (Audited)
        contact_reference: Worker instance representing the Contact for the Integration System
            Contact instance on Integration System (Audited)
    """

    class Meta:
        name = "Integration_System_Contact_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_contact_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Contact_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    contact_reference: Optional[WorkerObjectType] = field(
        default=None,
        metadata={
            "name": "Contact_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemRepositoryDocumentWwstype:
    """
    Repository Documents Data.

    Attributes:
        integration_repository_document_reference: Repository Document
    """

    class Meta:
        name = "Integration_System_Repository_Document_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_repository_document_reference: list[RepositoryDocumentAbstractObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Repository_Document_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class IntegrationSystemRequestCriteriaType:
    """
    Pass in a request criteria.

    Attributes:
        system_user_reference: Pass in a system user reference
    """

    class Meta:
        name = "Integration_System_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    system_user_reference: list[SystemUserObjectType] = field(
        default_factory=list,
        metadata={
            "name": "System_User_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemRequestReferencesType:
    """
    Utilize the Request References element to retrieve a specific instance(s) of Integration System
    and its associated data.

    Attributes:
        integration_system_reference: Unique identifier for an Integration System reference
    """

    class Meta:
        name = "Integration_System_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: list[IntegrationSystemAuditedObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class IntegrationTagForIntegrationSystemWwsDataType:
    """
    Integration Tag Data.

    Attributes:
        integration_tag_reference: Integration Tag Reference
    """

    class Meta:
        name = "Integration_Tag_for_Integration_System_WWS_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_tag_reference: list[IntegrationTagObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Tag_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationTransactionLogConfigurationDataType:
    """
    Container element for data related to a Transaction Log Service and its use within an
    Integration System.

    Attributes:
        all_business_processes: Subscribe to all Business Processes
        excluded_business_process_type_reference: Subscribe to all Business Processes except for the
            specified Business Processes
        all_transaction_types: Subscribe to all Transaction Types (e.g. both Business Processes and
            Event Lites)
        excluded_transaction_log_type_reference: Subscribe to all Transaction Types except for the
            specified Transaction Types
        included_transaction_log_type_reference: Subscribe to specific Transaction Log Type
    """

    class Meta:
        name = "Integration_Transaction_Log_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    all_business_processes: Optional[bool] = field(
        default=None,
        metadata={
            "name": "All_Business_Processes",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    excluded_business_process_type_reference: list[BusinessProcessTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Excluded_Business_Process_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    all_transaction_types: Optional[bool] = field(
        default=None,
        metadata={
            "name": "All_Transaction_Types",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    excluded_transaction_log_type_reference: list[TransactionLogTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Excluded_Transaction_Log_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    included_transaction_log_type_reference: list[TransactionLogTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Included_Transaction_Log_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchParameterDefaultDataType:
    """
    Element to define Default processing for Launch Parameter.

    Attributes:
        value_type_reference: Unique reference to Value Type (Parameter Initialization Operator).
        external_field_reference: When specifying a Value Type of "Determine Value at Runtime", an
            External Field must be provided.
        boolean: Boolean value.
        currency: Currency value.
        currency_reference: Currency Reference
        date: Date value.
        date_time: DateTime value.
        numeric: Numeric value.
        text: Text value.
        instance_reference: Unique reference to specific instance that matches Launch Parameter data
            type.
        enumeration_reference: Unique reference to specific instance of an Enumeration defined by
            the Launch Parameter.
    """

    class Meta:
        name = "Launch_Parameter_Default_DataType"
        target_namespace = "urn:com.workday/bsvc"

    value_type_reference: Optional[ParameterInitializationOperatorObjectType] = field(
        default=None,
        metadata={
            "name": "Value_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Currency",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    currency_reference: Optional[CurrencyObjectType] = field(
        default=None,
        metadata={
            "name": "Currency_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    enumeration_reference: Optional[IntegrationEnumerationObjectType] = field(
        default=None,
        metadata={
            "name": "Enumeration_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class NotificationAttachmentDataType:
    """
    Notification Attachment Data.

    Attributes:
        attachment_external_field_reference: Attachment External Field Reference defines a list of
            Attachments within the Workday system that may be included within the Notification.
    """

    class Meta:
        name = "Notification_Attachment_DataType"
        target_namespace = "urn:com.workday/bsvc"

    attachment_external_field_reference: list[ExternalFieldObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Attachment_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class NotificationMessageComponentDataType:
    """
    Element defining a component to be used in composing a message.

    Attributes:
        order: Order
        text: Static Text
        external_field_reference: Dynamic content from External Field
    """

    class Meta:
        name = "Notification_Message_Component_DataType"
        target_namespace = "urn:com.workday/bsvc"

    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "max_length": 6,
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class NotificationNotifiesDataType:
    """
    Notification Notifies Data.

    Attributes:
        notifies_recipient_external_field_reference: Notifies Person External Field Reference
            defines a list of Persons within the Workday system.
    """

    class Meta:
        name = "Notification_Notifies_DataType"
        target_namespace = "urn:com.workday/bsvc"

    notifies_recipient_external_field_reference: list[ExternalFieldObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Notifies_Recipient_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class PgpDecryptionSettingsDataType:
    """
    PGP Decryption Settings Data.

    Attributes:
        decrypt_key_pair_reference: Decrypt files with PGP Private Key Pair
        containing_integrity_check: Containing Integrity Check
        digital_signature_validation_reference: Digital Signature Validation Reference
    """

    class Meta:
        name = "PGP_Decryption_Settings_DataType"
        target_namespace = "urn:com.workday/bsvc"

    decrypt_key_pair_reference: Optional[PgpPrivateKeyPairObjectType] = field(
        default=None,
        metadata={
            "name": "Decrypt_Key_Pair_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    containing_integrity_check: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Containing_Integrity_Check",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    digital_signature_validation_reference: Optional[PgpPublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Digital_Signature_Validation_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PgpEncryptionSettingsDataType:
    """
    PGP Encryption Settings Data element.

    Attributes:
        certificate_reference: Certificate Reference
        text_mode: Text Mode
        ascii_armored: Ascii Armored
        containing_integrity_check: Containing Integrity Check
        decrypted_filename: Decrypted Filename
        pgp_2_6x_compatible: PGP 2.6x Compatible
        digitally_sign_key_pair_reference: Digitally Sign file
    """

    class Meta:
        name = "PGP_Encryption_Settings_DataType"
        target_namespace = "urn:com.workday/bsvc"

    certificate_reference: Optional[PgpPublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Certificate_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    text_mode: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Text_Mode",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    ascii_armored: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Ascii_Armored",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    containing_integrity_check: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Containing_Integrity_Check",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    decrypted_filename: Optional[str] = field(
        default=None,
        metadata={
            "name": "Decrypted_Filename",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    pgp_2_6x_compatible: Optional[bool] = field(
        default=None,
        metadata={
            "name": "PGP_2.6x_Compatible",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    digitally_sign_key_pair_reference: Optional[PgpPrivateKeyPairObjectType] = field(
        default=None,
        metadata={
            "name": "Digitally_Sign_Key_Pair_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ParameterExceptionDataType:
    """
    Element to define Parameters Exception to not fire Events in Concurrency.

    Attributes:
        launch_parameter_reference: Launch Parameter Reference
        simple_work_data_reference: Simple Work Data Reference
        xml_name: XML Name
    """

    class Meta:
        name = "Parameter_Exception_DataType"
        target_namespace = "urn:com.workday/bsvc"

    launch_parameter_reference: Optional[LaunchParameterObjectType] = field(
        default=None,
        metadata={
            "name": "Launch_Parameter_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    simple_work_data_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Simple_Work_Data_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    xml_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "XML_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutHideWorkdayDeliveredReportResponseType:
    """
    Contains reference to the hidden task restriction.

    Attributes:
        hide_workday_delivered_report_reference: Reference to the hidden task restriction
        version
    """

    class Meta:
        name = "Put_Hide_Workday_Delivered_Report_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    hide_workday_delivered_report_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Hide_Workday_Delivered_Report_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationEventResponseType:
    """
    Integration Event response element.

    Attributes:
        integration_event_reference: Reference element representing a unique instance of Integration
            Event.
        version
    """

    class Meta:
        name = "Put_Integration_Event_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationMessageResponseType:
    """
    Integration Message response element.

    Attributes:
        integration_message_reference: Reference element representing a unique instance of
            Integration Message.
        version
    """

    class Meta:
        name = "Put_Integration_Message_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_message_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Message_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationSystemUserResponseType:
    """
    Put Integration System User Response element.

    Attributes:
        integration_system_reference: Integration System Reference
        integration_system_user_reference: Integration System User Reference
        version
    """

    class Meta:
        name = "Put_Integration_System_User_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_user_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_User_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutReferenceRequestType:
    """
    Request element for Put Reference.

    Attributes:
        reference_id_reference: A reference the the business object to be updated.
        reference_id_data
        version
    """

    class Meta:
        name = "Put_Reference_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    reference_id_reference: Optional[ReferenceIdobjectType] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    reference_id_data: Optional[ReferenceIdDataType] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutReferenceResponseType:
    """
    Response element for Put Reference.

    Attributes:
        reference_id_reference: The updated reference.
        version
    """

    class Meta:
        name = "Put_Reference_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    reference_id_reference: Optional[ReferenceIdobjectType] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSequenceGeneratorResponseType:
    """
    Sequence Generator Response element.

    Attributes:
        sequence_generator_reference: Sequence Generator Reference
        version
    """

    class Meta:
        name = "Put_Sequence_Generator_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator_reference: Optional[SequenceGeneratorObjectType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSubscriptionResponseType:
    """
    Put Subscription Response.

    Attributes:
        subscription_reference: Subscription Reference
        version
    """

    class Meta:
        name = "Put_Subscription_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    subscription_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Subscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReassignBusinessProcessStepDataType:
    """
    Element containing the data for the reassignment.

    Attributes:
        reassign_to_reference: Specify a reference to the new Assignee for the business process
            step. The reference by default comes from Employee ID but can also be configured to
            accept Workday ID or Academic Affiliate ID when applicable.
        reassign_from_reference: Specify a reference to one of the current Assignee of the business
            process step. By default the reference comes from Employee ID but it can also be
            configure to accept Workday ID or Academic Affiliate ID when applicable.
        reason: Reassignment reasson
    """

    class Meta:
        name = "Reassign_Business_Process_Step_DataType"
        target_namespace = "urn:com.workday/bsvc"

    reassign_to_reference: Optional[RoleObjectType] = field(
        default=None,
        metadata={
            "name": "Reassign_To_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    reassign_from_reference: Optional[RoleObjectType] = field(
        default=None,
        metadata={
            "name": "Reassign_From_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reason",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReassignBusinessProcessStepResponseType:
    """
    Reference to business process event record processed.

    Attributes:
        event_record_reference: A reference to a business process event record. The reference can
            come from a Workday ID.
        version
    """

    class Meta:
        name = "Reassign_Business_Process_Step_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    event_record_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Record_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferenceIdtype:
    """
    The "Business Object" element contains object instances along with their corresponding Reference
    and Workday IDs.

    Attributes:
        reference_id_reference: The "Reference ID Reference" provides the Workday and Reference IDs
            (lookup IDs) for the instance of a business object in Workday.
        reference_id_data: Element containing reference ID and type data.
        descriptor: The "Descriptor" provides a human-readable, descriptive name for the business
            object. This "Descriptor" attribute should only be used as an informational description
            and not as data, an index or an identifier for integrations since descriptors can change
            from time to time in both format and value
    """

    class Meta:
        name = "Reference_IDType"
        target_namespace = "urn:com.workday/bsvc"

    reference_id_reference: Optional[ReferenceIndexObjectType] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    reference_id_data: Optional[ReferenceIdDataType] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descriptor: Optional[str] = field(
        default=None,
        metadata={
            "name": "Descriptor",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReferencesRequestReferencesType:
    """
    Wrapper element containing references to specific Reference IDs.

    Attributes:
        reference_id_reference: Reference to a specific reference ID for a business object.
    """

    class Meta:
        name = "References_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    reference_id_reference: list[ReferenceIndexObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Reference_ID_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReportBackgroundFutureProcessAsCustomReportDataType:
    """
    Report Background Future Process as Custom Report Data element.

    Attributes:
        custom_report_definition_reference: Custom Report Definition
        output_format_reference: Formatted Report URL of the Custom Report
        run_as_system_user_reference: System User for the Custom Report
    """

    class Meta:
        name = "Report_Background_Future_Process_as_Custom_Report_DataType"
        target_namespace = "urn:com.workday/bsvc"

    custom_report_definition_reference: Optional[CustomReportDefinitionObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Report_Definition_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    output_format_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Output_Format_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    run_as_system_user_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "Run_As_System_User_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class RescindBusinessProcessRequestType:
    """
    Rescind Business Process Request.

    Attributes:
        event_reference: Event Reference
        rescind_business_process_data: Rescind Business Process Data
        version
    """

    class Meta:
        name = "Rescind_Business_Process_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    rescind_business_process_data: Optional[RescindBusinessProcessDataType] = field(
        default=None,
        metadata={
            "name": "Rescind_Business_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class RescindBusinessProcessResponseType:
    """
    Rescind Business Process Response.

    Attributes:
        event_reference: Event Reference
        version
    """

    class Meta:
        name = "Rescind_Business_Process_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SftpTransportProtocolDataWithDualAuthenticationType:
    """
    SFTP Transport Protocol Data element.

    Attributes:
        sftp_address: SFTP Address
        directory: Directory
        dual_authentication: Dual Authentication
        user_id: Text attribute identifying User Name.
        password: Text attribute identifying Password.
        ssh_authentication_reference: Certificate reference for SSH Authentication
        use_temp_file: Allow the file to be overwritten only when it is finished uploading to
            external site. Avoids the external system from attempting to read file before it has
            been fully uploaded.
        block_size: The block size to set when using SFTP
        block_size_name: The more human-readable label for SFTP Block Size (i.e. 32k for 32768)
        host_key_fingerprint: Host Key Fingerprint for SFTP Servers
    """

    class Meta:
        name = "SFTP_Transport_Protocol_Data_with_Dual_AuthenticationType"
        target_namespace = "urn:com.workday/bsvc"

    sftp_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "SFTP_Address",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    directory: Optional[str] = field(
        default=None,
        metadata={
            "name": "Directory",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    dual_authentication: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Dual_Authentication",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    user_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "User_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    ssh_authentication_reference: Optional[X509PrivateKeyPairObjectType] = field(
        default=None,
        metadata={
            "name": "SSH_Authentication_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    use_temp_file: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Temp_File",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    block_size: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Block_Size",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    block_size_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Block_Size_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    host_key_fingerprint: Optional[str] = field(
        default=None,
        metadata={
            "name": "Host_Key_Fingerprint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SendBackBusinessProcessRequestType:
    """
    Top-level request element for the Send Back Business Process operation.

    Attributes:
        event_reference: A reference to a business process event. The reference can come from
            Workday ID.
        event_description: Workday won't save this data in any Workday fields. You can use this
            field to copy the event name and identify which event you list in the Event Reference
            field.
        send_back_business_process_data: Element containing the data for the send back.
        version
    """

    class Meta:
        name = "Send_Back_Business_Process_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    event_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Event_Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    send_back_business_process_data: Optional[SendBackBusinessProcessDataType] = field(
        default=None,
        metadata={
            "name": "Send_Back_Business_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SendBackBusinessProcessResponseType:
    """
    Reference to the business process event sent back.

    Attributes:
        event_reference: A reference to a business process event. The reference can come from
            Workday ID.
        version
    """

    class Meta:
        name = "Send_Back_Business_Process_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SequenceGeneratorRequestReferencesType:
    """
    Sequence Generator Request References.

    Attributes:
        sequence_generator_reference: Sequence Generator Reference
    """

    class Meta:
        name = "Sequence_Generator_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator_reference: list[SequenceGeneratorObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class SubscriptionConditionDataType:
    """
    Subscription Condition Data Element.

    Attributes:
        condition_rule_reference: Condition Rule Reference
    """

    class Meta:
        name = "Subscription_Condition_DataType"
        target_namespace = "urn:com.workday/bsvc"

    condition_rule_reference: Optional[ConditionRuleObjectType] = field(
        default=None,
        metadata={
            "name": "Condition_Rule_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class SubscriptionRequestCriteriaType:
    """
    Criteria for filtering the Subscriptions that get returned in the response.

    Attributes:
        integration_system_reference: Integration System Reference
    """

    class Meta:
        name = "Subscription_Request_CriteriaType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SubscriptionRequestReferencesType:
    """
    Subscription Request References element.

    Attributes:
        subscription_reference: Subscription Reference
    """

    class Meta:
        name = "Subscription_Request_ReferencesType"
        target_namespace = "urn:com.workday/bsvc"

    subscription_reference: list[UniqueIdentifierObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Subscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class ValidationFault(ValidationFaultType):
    class Meta:
        name = "Validation_Fault"
        namespace = "urn:com.workday/bsvc"


@dataclass
class WebServiceOperationDataWwstype:
    """
    Container element for definitions of Web Service Operations associated to Studio integrations.

    Attributes:
        order: Order
        web_service_operation_reference: Web Service Operation
        web_service_operation_connector_wid: Web Service Operation Connector
    """

    class Meta:
        name = "Web_Service_Operation_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "max_length": 6,
        },
    )
    web_service_operation_reference: Optional[WebServiceOperationObjectType] = field(
        default=None,
        metadata={
            "name": "Web_Service_Operation_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    web_service_operation_connector_wid: Optional[str] = field(
        default=None,
        metadata={
            "name": "Web_Service_Operation_Connector_WID",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 36,
        },
    )


@dataclass
class WebServiceSecurityConfigurationDataType:
    """
    A valid instance of Web Service Security Configuration.

    Attributes:
        enable_x509_token_authentication: Indicates if WS-Security x509 Certificate Token Profile
            authentication is enabled.
        x509_public_key_reference: x509 Encryption Certificate used to sign requests
        enable_saml_authentication: Indicates if WS-Security SAML Token Profile authentication is
            enabled.
        saml_issuer: Unique identifier of the SAML identity provider.
        identity_provider_public_key_reference: x509 Encryption Certificate of the SAML identity
            provider.
        holder_of_key_public_key_reference: x509 Encryption Certificate of the holder-of-key. This
            key is used to verify the signature of the inbound SOAP message.
    """

    class Meta:
        name = "Web_Service_Security_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    enable_x509_token_authentication: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Enable_x509_Token_Authentication",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    x509_public_key_reference: Optional[X509PublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "X509_Public_Key_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    enable_saml_authentication: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Enable_SAML_Authentication",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    saml_issuer: Optional[str] = field(
        default=None,
        metadata={
            "name": "SAML_Issuer",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    identity_provider_public_key_reference: Optional[X509PublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Identity_Provider_Public_Key_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    holder_of_key_public_key_reference: Optional[X509PublicKeyObjectType] = field(
        default=None,
        metadata={
            "name": "Holder-of-Key_Public_Key_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class As2TransportProtocolDataType:
    """
    AS2 Transport Protocol Data element.

    Attributes:
        as2_endpoint: AS2 Address
        as2_settings_data
    """

    class Meta:
        name = "AS2_Transport_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    as2_endpoint: Optional[str] = field(
        default=None,
        metadata={
            "name": "AS2_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    as2_settings_data: Optional[As2SettingsDataType] = field(
        default=None,
        metadata={
            "name": "AS2_Settings_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class ApproveBusinessProcessRequest(ApproveBusinessProcessRequestType):
    class Meta:
        name = "Approve_Business_Process_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class ApproveBusinessProcessResponse(ApproveBusinessProcessResponseType):
    class Meta:
        name = "Approve_Business_Process_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class CancelBusinessProcessRequest(CancelBusinessProcessRequestType):
    class Meta:
        name = "Cancel_Business_Process_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class CancelBusinessProcessResponse(CancelBusinessProcessResponseType):
    class Meta:
        name = "Cancel_Business_Process_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class CancelIntegrationEventRequest(CancelIntegrationEventRequestType):
    class Meta:
        name = "Cancel_Integration_Event_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class CancelIntegrationEventResponse(CancelIntegrationEventResponseType):
    class Meta:
        name = "Cancel_Integration_Event_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class ConcurrencyConfigurationDataType:
    """
    Element to configure Concurrency on Integration Background Future Process.

    Attributes:
        concurrency_option: Concurrency Option
        parameter_exception_data: Parameters Exception Data
    """

    class Meta:
        name = "Concurrency_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    concurrency_option: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Concurrency_Option",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_exception_data: list[ParameterExceptionDataType] = field(
        default_factory=list,
        metadata={
            "name": "Parameter_Exception_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class DeleteIntegrationSystemRequest(DeleteIntegrationSystemRequestType):
    class Meta:
        name = "Delete_Integration_System_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class DeleteIntegrationSystemResponse(DeleteIntegrationSystemResponseType):
    class Meta:
        name = "Delete_Integration_System_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class DenyBusinessProcessRequest(DenyBusinessProcessRequestType):
    class Meta:
        name = "Deny_Business_Process_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class DenyBusinessProcessResponse(DenyBusinessProcessResponseType):
    class Meta:
        name = "Deny_Business_Process_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class EibIntegrationTransportProtocolDataWwstype:
    """
    Integration Transport Protocol Data element.

    Attributes:
        id: Unique identifier
        ftps_transport_protocol_data
        sftp_transport_protocol_data
        amazon_simple_storage_service_protocol_data: Amazon Simple Storage Service Protocol Data for
            EIB
        google_drive_transport_protocol_data
    """

    class Meta:
        name = "EIB_Integration_Transport_Protocol_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    ftps_transport_protocol_data: Optional[FtpsTransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "FTPS_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sftp_transport_protocol_data: Optional[SftpTransportProtocolDataWithDualAuthenticationType] = (
        field(
            default=None,
            metadata={
                "name": "SFTP_Transport_Protocol_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    amazon_simple_storage_service_protocol_data: Optional[
        AmazonSimpleStorageServiceEibRetrievalProtocolDataType
    ] = field(
        default=None,
        metadata={
            "name": "Amazon_Simple_Storage_Service_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    google_drive_transport_protocol_data: Optional[GoogleDriveEibTransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "Google_Drive_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventResponseDataType:
    """Element containing the response data with event details."""

    class Meta:
        name = "Event_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    event: list[EventWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Event",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDetailsRequestType:
    """
    Get_Event_Details request element.

    Attributes:
        request_references: This element contains references to the events that you wish to get the
            details for. Enter in a Workday ID or Reference ID for the events that you wish to get
            back details for.
        request_criteria: This element contains request criteria to exclude Process History and
            Remaining Process Data.
        response_filter
        version
    """

    class Meta:
        name = "Get_Event_Details_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[EventRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    request_criteria: Optional[EventRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDocumentsRequestType:
    """Get Event Documents Request element."""

    class Meta:
        name = "Get_Event_Documents_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationEventRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    response_filter: Optional[ResponseFilterNoEntryMomentType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetHideWorkdayDeliveredReportRequestType:
    """Retrieves hidden Workday delivered reports and their associated data."""

    class Meta:
        name = "Get_Hide_Workday_Delivered_Report_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[HideWorkdayDeliveredReportRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[HideWorkdayDeliveredReportRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_group: Optional[HideWorkdayDeliveredReportResponseGroupType] = field(
        default=None,
        metadata={
            "name": "Response_Group",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetImportProcessMessagesRequestType:
    """
    Incoming request element.

    Attributes:
        request_criteria: Required for specifying an Import Process event reference
        response_filter: Response Filter
        version
    """

    class Meta:
        name = "Get_Import_Process_Messages_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_criteria: Optional[ImportProcessMessagesRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetImportProcessesRequestType:
    """
    Incoming element for Get Import Processes.

    Attributes:
        request_references: Import Process Request References
        response_filter: Parameters that let you filter the data returned in the response. You can
            filter returned data by dates and page attributes.
        version
    """

    class Meta:
        name = "Get_Import_Processes_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[ImportProcessRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetIntegrationEventsRequestType:
    """
    Request element for the Get Integration Events operation.

    Attributes:
        request_references: Request References
        request_criteria: Request Criteria
        response_filter: Response Filter
        version
    """

    class Meta:
        name = "Get_Integration_Events_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationEventRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[IntegrationEventRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterNoEntryMomentType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetIntegrationSystemUsersRequestType:
    """Get Integration System Users Request element."""

    class Meta:
        name = "Get_Integration_System_Users_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationSystemRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_request_criteria: Optional[IntegrationSystemRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetIntegrationSystemsRequestType:
    """Request element used to find and get Integration Systems and their associated data."""

    class Meta:
        name = "Get_Integration_Systems_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationSystemRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[GetIntegrationSystemsCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_group: Optional[IntegrationSystemResponseGroupType] = field(
        default=None,
        metadata={
            "name": "Response_Group",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetReferencesRequestType:
    """
    Root request element for the operation.

    Attributes:
        request_references: Wrapper element containing references to specific business objects.
        request_criteria: Contains additional criteria for identifying specific Staffing Field
            Defaults instances.
        response_filter
        version
    """

    class Meta:
        name = "Get_References_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[ReferencesRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[GetReferencesRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetReferencesResponseDataType:
    """
    The "Response Data" element contains the core data results based on the inbound request that was
    processed.

    Attributes:
        reference_id: The "Business Object" element contains object instances along with their
            corresponding Reference and Workday IDs.
    """

    class Meta:
        name = "Get_References_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    reference_id: list[ReferenceIdtype] = field(
        default_factory=list,
        metadata={
            "name": "Reference_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetSequenceGeneratorsRequestType:
    """Sequence Generator request element."""

    class Meta:
        name = "Get_Sequence_Generators_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[SequenceGeneratorRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetSubscriptionsRequestType:
    """Get Subscriptions Request."""

    class Meta:
        name = "Get_Subscriptions_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[SubscriptionRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[SubscriptionRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class HideWorkdayDeliveredReportResponseDataType:
    """Contains the list of references that identify hidden Workday delivered reports."""

    class Meta:
        name = "Hide_Workday_Delivered_Report_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    hide_workday_delivered_report: list[HideWorkdayDeliveredReportDataType] = field(
        default_factory=list,
        metadata={
            "name": "Hide_Workday_Delivered_Report",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ImportProcessType:
    """
    Import Process.

    Attributes:
        import_process_reference: Import Process Instance
        import_process_data: Import Process Data
    """

    class Meta:
        name = "Import_ProcessType"
        target_namespace = "urn:com.workday/bsvc"

    import_process_reference: Optional[WebServiceBackgroundProcessRuntimeObjectType] = field(
        default=None,
        metadata={
            "name": "Import_Process_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    import_process_data: Optional[ImportProcessDataType] = field(
        default=None,
        metadata={
            "name": "Import_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ImportProcessMessageResponseDataType:
    """
    Response Data.

    Attributes:
        import_process_message: Import Process Message
    """

    class Meta:
        name = "Import_Process_Message_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    import_process_message: list[ImportProcessMessageType] = field(
        default_factory=list,
        metadata={
            "name": "Import_Process_Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IncrementSequenceGeneratorRequest(IncrementSequenceGeneratorRequestType):
    class Meta:
        name = "Increment_Sequence_Generator_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class IncrementSequenceGeneratorResponse(IncrementSequenceGeneratorResponseType):
    class Meta:
        name = "Increment_Sequence_Generator_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationAttributeIntegrationAttributeValueDataWwstype:
    """
    Contains Integration Attributes Name and Values associated to above Attributable instance.

    Attributes:
        integration_attribute_reference: Unique identifier for an Integration Constant (e.g.
            Attribute) reference
        integration_attribute_name: Constant Name
        integration_attribute_value_data
    """

    class Meta:
        name = "Integration_Attribute_Integration_Attribute_Value_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_attribute_reference: Optional[ExternalInstanceObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Attribute_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attribute_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_Attribute_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attribute_value_data: list[IntegrationAttributeValueDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Attribute_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationCustomObjectConfigurationDataType:
    """Integration Custom Object Configuration Data."""

    class Meta:
        name = "Integration_Custom_Object_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_custom_object_alias_configuration_data: list[
        IntegrationCustomObjectAliasConfigurationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Custom_Object_Alias_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class IntegrationFieldAttributesFieldConfigurationDataType:
    """
    Integration Field Attributes Field Configuration Data.

    Attributes:
        field_reference: Document Field Reference
        web_service_alias: Web Service Alias for Field
        include_in_output: Denotes whether this field should be included within the Output document.
        required_field: If this field is to be included in the Output document, denotes whether
            there must be a value supplied for this field.  If there is not a value, then error
            handling should occur.
        maximum_length: If this field is to be included in the Output document, denotes whether
            there should be a maximum length enforced for this field.  If the value, exceeds the
            maximum length then special handling should occur.
        integration_document_field_options
        integration_field_attributes_field_configuration_data
    """

    class Meta:
        name = "Integration_Field_Attributes_Field_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    field_reference: Optional[IntegrationDocumentFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    web_service_alias: Optional[str] = field(
        default=None,
        metadata={
            "name": "Web_Service_Alias",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    include_in_output: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Include_in_Output",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    required_field: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Required_Field",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    maximum_length: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Maximum_Length",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 6,
            "fraction_digits": 0,
        },
    )
    integration_document_field_options: list[IntegrationDocumentFieldOptionsType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Field_Options",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_field_attributes_field_configuration_data: list[
        "IntegrationFieldAttributesFieldConfigurationDataType"
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Attributes_Field_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationLaunchParameterDataType:
    """
    Integration Launch Parameter Data.

    Attributes:
        launch_parameter_reference: Launch Parameter Reference
        launch_parameter_value_data: Launch Parameter Value Data
    """

    class Meta:
        name = "Integration_Launch_Parameter_DataType"
        target_namespace = "urn:com.workday/bsvc"

    launch_parameter_reference: Optional[LaunchParameterObjectType] = field(
        default=None,
        metadata={
            "name": "Launch_Parameter_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    launch_parameter_value_data: Optional[IntegrationAbstractValueDataType] = field(
        default=None,
        metadata={
            "name": "Launch_Parameter_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationMapValueDataWwstype:
    """
    Container element for each row of data within an Integration Map value.

    Attributes:
        internal_value_data: Internal Value
        external_value_data: External Value
    """

    class Meta:
        name = "Integration_Map_Value_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    internal_value_data: Optional[IntegrationAbstractValueDataType] = field(
        default=None,
        metadata={
            "name": "Internal_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_value_data: Optional[CopyOfIntegrationAbstractValueDataType] = field(
        default=None,
        metadata={
            "name": "External_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationMessageDataType:
    """
    Encapsulating element containing all Integration Message data.

    Attributes:
        integration_event_reference: Reference element representing a unique instance of Integration
            Event.
        integration_system_reference: Reference element representing a unique instance of
            Integration System.
        message_summary: Text attribute identifying the Summary of the Integration Message.
        message_detail: Text attribute identifying the Detail of the Integration Message.
        severity_level_reference: Reference element representing a unique instance of Integration
            Message Severity Level.
        message_target_reference: A Reference to an instance within the Workday system that is
            related to this message.
        integration_attachment_data: Integration Attachment Data
        repository_document_data: Repository Document Data
        enqueue_notification_message: Add Inbox Notification to the Processing User
    """

    class Meta:
        name = "Integration_Message_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    message_summary: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message_Summary",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    message_detail: Optional[str] = field(
        default=None,
        metadata={
            "name": "Message_Detail",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    severity_level_reference: Optional[BackgroundProcessMessageSeverityLevelObjectType] = field(
        default=None,
        metadata={
            "name": "Severity_Level_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    message_target_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Message_Target_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attachment_data: list[IntegrationAttachmentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Attachment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    repository_document_data: list[IntegrationRepositoryDocumentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Repository_Document_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    enqueue_notification_message: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Enqueue_Notification_Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationParameterReferenceType:
    """
    Integration Parameter Reference.

    Attributes:
        global_value: Context of Integration Event.  If FALSE, then takes the Context of the level
            within the Document.
        integration_parameter_name: Integration Parameter Name
        integration_document_stack_data
    """

    class Meta:
        name = "Integration_Parameter_ReferenceType"
        target_namespace = "urn:com.workday/bsvc"

    global_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Global",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_parameter_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_Parameter_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_document_stack_data: list[IntegrationDocumentStackDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Stack_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationPayloadDataType:
    """
    Integration Payload Data element.

    Attributes:
        pgp_encryption_settings_data
        compressed: Indicates if the payload is expected to be compressed.
        use_improved_compression: Indicates if the payload should use improved compression.
        encrypt_using_aws_kms_key: Amazon Key Management Service (KMS) Key Alias to use to encrypt.
        kms_region: The region where the KMS Key to be used to encrypt is located.
        storage_class: Amazon Simple Storage Service (S3) Storage Class to use when storing the
            object in the bucket.
        transfer_acceleration_enabled: Enable Transfer Acceleration when delivering the file to an
            Amazon S3 bucket.
    """

    class Meta:
        name = "Integration_Payload_DataType"
        target_namespace = "urn:com.workday/bsvc"

    pgp_encryption_settings_data: Optional[PgpEncryptionSettingsDataType] = field(
        default=None,
        metadata={
            "name": "PGP_Encryption_Settings_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    compressed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Compressed",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    use_improved_compression: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Use_Improved_Compression",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    encrypt_using_aws_kms_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Encrypt_using_AWS_KMS_Key",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    kms_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "KMS_Region",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    storage_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "Storage_Class",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    transfer_acceleration_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Transfer_Acceleration_Enabled",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationReportServiceConfigurationDataType:
    """Integration Report Service Configuration Data."""

    class Meta:
        name = "Integration_Report_Service_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_report_field_configuration_data: list[
        IntegrationReportFieldConfigurationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Report_Field_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class IntegrationRepositoryDocumentType:
    """
    Integration Repository Document.

    Attributes:
        integration_repository_document_reference: Integration Repository Document Reference
        integration_repository_document_data
    """

    class Meta:
        name = "Integration_Repository_DocumentType"
        target_namespace = "urn:com.workday/bsvc"

    integration_repository_document_reference: Optional[IntegrationRepositoryDocumentObjectType] = (
        field(
            default=None,
            metadata={
                "name": "Integration_Repository_Document_Reference",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    integration_repository_document_data: Optional[IntegrationRepositoryDocumentDataType] = field(
        default=None,
        metadata={
            "name": "Integration_Repository_Document_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationServiceComponentFieldOverrideDataType:
    """
    Service Component Field Override Data element.

    Attributes:
        field_name: The Name of the Field for corresponding Service Component.  This will be a
            unique identifier for looking up the appropriate Field.
        specify_value_data: To specify a specific value, populate this element.
        attachment_data: To create and assign an Attachment to the Field, populate this element.
        external_field_reference: To determine a value using an External Field, populate this
            element.
    """

    class Meta:
        name = "Integration_Service_Component_Field_Override_DataType"
        target_namespace = "urn:com.workday/bsvc"

    field_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Field_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    specify_value_data: Optional[IntegrationAbstractValueDataType] = field(
        default=None,
        metadata={
            "name": "Specify_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    attachment_data: Optional[IntegrationAttachmentDataType] = field(
        default=None,
        metadata={
            "name": "Attachment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationServiceGeneratedSequenceDataType:
    """
    Integration Service Generated Sequence Data.

    Attributes:
        integration_service_reference: Integration Service Reference
        integration_sequencer_generated_sequence_data
    """

    class Meta:
        name = "Integration_Service_Generated_Sequence_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_service_reference: Optional[IntegrationSequenceGeneratorServiceObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Service_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_sequencer_generated_sequence_data: list[
        IntegrationSequencerGeneratedSequenceDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Sequencer_Generated_Sequence_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationSystemUserDataType:
    """
    Integration System User Data element.

    Attributes:
        integration_system_reference: Integration System Reference
        user_name: User Name
        password: Text attribute identifying Password.
        generate_random_password: The system should generate a random password for the user.
        require_new_password_at_next_sign_in: The user will be required to change their password
            upon initial sign on.
        session_timeout_minutes: The amount of time after which an unused session will expire.
            Session Timeout Minutes defaults to the value configured in the Password Rules unless
            set to a non- zero value.
        do_not_allow_ui_sessions: This field allows restricting integration system user accounts
            from signing in to Workday in the user interface (UI). Integration system accounts
            should only be used for web service integrations. If the field is true, the integration
            system user will not be able to sign in to the UI, but will still be able to make web
            service requests. If the field is false, the integration system user will be able to
            sign in from both the UI and through web services.
        web_service_security_configuration_data
    """

    class Meta:
        name = "Integration_System_User_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    user_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "User_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "name": "Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    generate_random_password: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Generate_Random_Password",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    require_new_password_at_next_sign_in: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Require_New_Password_At_Next_Sign_In",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    session_timeout_minutes: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Session_Timeout_Minutes",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 3,
            "fraction_digits": 0,
        },
    )
    do_not_allow_ui_sessions: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Do_Not_Allow_UI_Sessions",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    web_service_security_configuration_data: list[WebServiceSecurityConfigurationDataType] = field(
        default_factory=list,
        metadata={
            "name": "Web_Service_Security_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationTransformationDataWwstype:
    """
    Integration Transformation Data element.

    Attributes:
        name: Name
        delivered_transformation_data
        xslt_attachment_transformation_reference: Reference to an XSLT Attachment Transformation
        custom_report_transformation_data
    """

    class Meta:
        name = "Integration_Transformation_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    delivered_transformation_data: Optional[DeliveredTransformationDataType] = field(
        default=None,
        metadata={
            "name": "Delivered_Transformation_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    xslt_attachment_transformation_reference: Optional[XsltAttachmentTransformationObjectType] = (
        field(
            default=None,
            metadata={
                "name": "XSLT_Attachment_Transformation_Reference",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    custom_report_transformation_data: Optional[CustomReportTransformationDataType] = field(
        default=None,
        metadata={
            "name": "Custom_Report_Transformation_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchParameterDataType:
    """
    Container element for all the Integration Launch Parameters for this Integration System.

    Attributes:
        order: Order Priority
        name: Launch Parameter Name
        description: Launch Parameter Description
        data_type_enumeration_definition_reference: Data Type of Launch Parameter (e.g. structure)
            defined by an Integration Enumeration Definition.
        data_type_external_field_reference: Data Type of Launch Parameter (e.g. structure) defined
            by an External Field.
        launch_option_reference: Unique reference to Launch Options
        launch_parameter_default_data
    """

    class Meta:
        name = "Launch_Parameter_DataType"
        target_namespace = "urn:com.workday/bsvc"

    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    data_type_enumeration_definition_reference: Optional[
        IntegrationEnumerationDefinitionObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Data_Type_Enumeration_Definition_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    data_type_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Data_Type_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    launch_option_reference: list[IntegrationLaunchOptionObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Launch_Option_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    launch_parameter_default_data: Optional[LaunchParameterDefaultDataType] = field(
        default=None,
        metadata={
            "name": "Launch_Parameter_Default_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class NotificationBodyDataType:
    """
    Element containing the components that make up the Body of the email message.

    Attributes:
        notification_body_data: Notification Body Data
    """

    class Meta:
        name = "Notification_Body_DataType"
        target_namespace = "urn:com.workday/bsvc"

    notification_body_data: list[NotificationMessageComponentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Notification_Body_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class NotificationSubjectDataType:
    """
    Element containing the components that make up the Subject of the email message.

    Attributes:
        notification_message_component_data: Notification Message Component Data
    """

    class Meta:
        name = "Notification_Subject_DataType"
        target_namespace = "urn:com.workday/bsvc"

    notification_message_component_data: list[NotificationMessageComponentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Notification_Message_Component_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ParameterInitializationDataType:
    """
    Defines the value to be used for parameter assignment.

    Attributes:
        boolean: Boolean
        currency: Currency
        date: Date
        date_time: DateTime
        numeric: Numeric
        text: Text
        business_object_instance_reference: Business Object Instance Reference
        external_field_content: External Field Content
        parameter_initialization_operator_reference: Parameter Initialization Operator Reference
        currency_reference: Currency Reference
    """

    class Meta:
        name = "Parameter_Initialization_DataType"
        target_namespace = "urn:com.workday/bsvc"

    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Currency",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    business_object_instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Business_Object_Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_content: Optional[ExternalFieldAddOrReferenceType] = field(
        default=None,
        metadata={
            "name": "External_Field_Content",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_initialization_operator_reference: Optional[
        ParameterInitializationOperatorObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Operator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    currency_reference: Optional[CurrencyObjectType] = field(
        default=None,
        metadata={
            "name": "Currency_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutHideWorkdayDeliveredReportRequestType:
    """Contains data for creating and updating hidden Workday delivered reports."""

    class Meta:
        name = "Put_Hide_Workday_Delivered_Report_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    hide_workday_delivered_report_data: list[HideWorkdayDeliveredReportDataType] = field(
        default_factory=list,
        metadata={
            "name": "Hide_Workday_Delivered_Report_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutHideWorkdayDeliveredReportResponse(PutHideWorkdayDeliveredReportResponseType):
    class Meta:
        name = "Put_Hide_Workday_Delivered_Report_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationEventResponse(PutIntegrationEventResponseType):
    class Meta:
        name = "Put_Integration_Event_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationMessageResponse(PutIntegrationMessageResponseType):
    class Meta:
        name = "Put_Integration_Message_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationSystemResponseType:
    """
    Integration System Response element.

    Attributes:
        integration_system_reference: Integration System Reference
        exceptions_response_data
        version
    """

    class Meta:
        name = "Put_Integration_System_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    exceptions_response_data: list[ApplicationInstanceRelatedExceptionsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Exceptions_Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationSystemUserResponse(PutIntegrationSystemUserResponseType):
    class Meta:
        name = "Put_Integration_System_User_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutReferenceRequest(PutReferenceRequestType):
    class Meta:
        name = "Put_Reference_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutReferenceResponse(PutReferenceResponseType):
    class Meta:
        name = "Put_Reference_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutSequenceGeneratorRequestType:
    """
    Sequence Generator Request element.

    Attributes:
        sequence_generator_reference: Sequence Generator Reference
        sequence_generator_data
        add_only: Add only
        version
    """

    class Meta:
        name = "Put_Sequence_Generator_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator_reference: Optional[SequenceGeneratorObjectType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sequence_generator_data: Optional[AbstractSequenceGeneratorDataType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    add_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Add_Only",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSequenceGeneratorResponse(PutSequenceGeneratorResponseType):
    class Meta:
        name = "Put_Sequence_Generator_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutSubscriptionResponse(PutSubscriptionResponseType):
    class Meta:
        name = "Put_Subscription_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class ReassignBusinessProcessStepRequestType:
    """
    Top-level request element for the Reassign Business Process Step operation.

    Attributes:
        event_record_reference: A reference to a business process event record. The reference can
            come from a Workday ID.
        reassign_business_process_step_data: Element containing the data for the reassignment.
        version
    """

    class Meta:
        name = "Reassign_Business_Process_Step_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    event_record_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Record_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    reassign_business_process_step_data: Optional[ReassignBusinessProcessStepDataType] = field(
        default=None,
        metadata={
            "name": "Reassign_Business_Process_Step_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ReassignBusinessProcessStepResponse(ReassignBusinessProcessStepResponseType):
    class Meta:
        name = "Reassign_Business_Process_Step_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class RepositoryDocumentSummaryDataType:
    """
    Summary of Repository Document.

    Attributes:
        repository_document_reference: Reference to a Repository Document
        repository_document_data: Document Tag reference
    """

    class Meta:
        name = "Repository_Document_Summary_DataType"
        target_namespace = "urn:com.workday/bsvc"

    repository_document_reference: Optional[RepositoryDocumentAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Repository_Document_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    repository_document_data: list[IntegrationRepositoryDocumentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Repository_Document_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class RescindBusinessProcessRequest(RescindBusinessProcessRequestType):
    class Meta:
        name = "Rescind_Business_Process_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class RescindBusinessProcessResponse(RescindBusinessProcessResponseType):
    class Meta:
        name = "Rescind_Business_Process_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class SendBackBusinessProcessRequest(SendBackBusinessProcessRequestType):
    class Meta:
        name = "Send_Back_Business_Process_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class SendBackBusinessProcessResponse(SendBackBusinessProcessResponseType):
    class Meta:
        name = "Send_Back_Business_Process_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class SequenceGeneratorType:
    """
    Sequence Generator.

    Attributes:
        sequence_generator_reference: Sequence Generator Reference
        sequence_generator_data
        sequenced_value: Sequenced Value
    """

    class Meta:
        name = "Sequence_GeneratorType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator_reference: Optional[SequenceGeneratorObjectType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sequence_generator_data: Optional[AbstractSequenceGeneratorDataType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sequenced_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Sequenced_Value",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ApproveBusinessProcessInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["ApproveBusinessProcessInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["ApproveBusinessProcessInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        approve_business_process_request: Optional[ApproveBusinessProcessRequest] = field(
            default=None,
            metadata={
                "name": "Approve_Business_Process_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class ApproveBusinessProcessOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["ApproveBusinessProcessOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        approve_business_process_response: Optional[ApproveBusinessProcessResponse] = field(
            default=None,
            metadata={
                "name": "Approve_Business_Process_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["ApproveBusinessProcessOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["ApproveBusinessProcessOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class CancelBusinessProcessInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["CancelBusinessProcessInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["CancelBusinessProcessInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        cancel_business_process_request: Optional[CancelBusinessProcessRequest] = field(
            default=None,
            metadata={
                "name": "Cancel_Business_Process_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class CancelBusinessProcessOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["CancelBusinessProcessOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        cancel_business_process_response: Optional[CancelBusinessProcessResponse] = field(
            default=None,
            metadata={
                "name": "Cancel_Business_Process_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["CancelBusinessProcessOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["CancelBusinessProcessOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class CancelIntegrationEventInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["CancelIntegrationEventInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["CancelIntegrationEventInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        cancel_integration_event_request: Optional[CancelIntegrationEventRequest] = field(
            default=None,
            metadata={
                "name": "Cancel_Integration_Event_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class CancelIntegrationEventOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["CancelIntegrationEventOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        cancel_integration_event_response: Optional[CancelIntegrationEventResponse] = field(
            default=None,
            metadata={
                "name": "Cancel_Integration_Event_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["CancelIntegrationEventOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["CancelIntegrationEventOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class DeleteIntegrationSystemInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["DeleteIntegrationSystemInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["DeleteIntegrationSystemInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        delete_integration_system_request: Optional[DeleteIntegrationSystemRequest] = field(
            default=None,
            metadata={
                "name": "Delete_Integration_System_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class DeleteIntegrationSystemOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["DeleteIntegrationSystemOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        delete_integration_system_response: Optional[DeleteIntegrationSystemResponse] = field(
            default=None,
            metadata={
                "name": "Delete_Integration_System_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["DeleteIntegrationSystemOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["DeleteIntegrationSystemOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class DenyBusinessProcessInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["DenyBusinessProcessInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["DenyBusinessProcessInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        deny_business_process_request: Optional[DenyBusinessProcessRequest] = field(
            default=None,
            metadata={
                "name": "Deny_Business_Process_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class DenyBusinessProcessOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["DenyBusinessProcessOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        deny_business_process_response: Optional[DenyBusinessProcessResponse] = field(
            default=None,
            metadata={
                "name": "Deny_Business_Process_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["DenyBusinessProcessOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["DenyBusinessProcessOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class IncrementSequenceGeneratorInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["IncrementSequenceGeneratorInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["IncrementSequenceGeneratorInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        increment_sequence_generator_request: Optional[IncrementSequenceGeneratorRequest] = field(
            default=None,
            metadata={
                "name": "Increment_Sequence_Generator_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class IncrementSequenceGeneratorOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["IncrementSequenceGeneratorOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        increment_sequence_generator_response: Optional[IncrementSequenceGeneratorResponse] = field(
            default=None,
            metadata={
                "name": "Increment_Sequence_Generator_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["IncrementSequenceGeneratorOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["IncrementSequenceGeneratorOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutHideWorkdayDeliveredReportOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutHideWorkdayDeliveredReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_hide_workday_delivered_report_response: Optional[
            PutHideWorkdayDeliveredReportResponse
        ] = field(
            default=None,
            metadata={
                "name": "Put_Hide_Workday_Delivered_Report_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutHideWorkdayDeliveredReportOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutHideWorkdayDeliveredReportOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutIntegrationEventOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationEventOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_event_response: Optional[PutIntegrationEventResponse] = field(
            default=None,
            metadata={
                "name": "Put_Integration_Event_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutIntegrationEventOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutIntegrationEventOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutIntegrationMessageOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationMessageOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_message_response: Optional[PutIntegrationMessageResponse] = field(
            default=None,
            metadata={
                "name": "Put_Integration_Message_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutIntegrationMessageOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutIntegrationMessageOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutIntegrationSystemUserOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationSystemUserOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_system_user_response: Optional[PutIntegrationSystemUserResponse] = field(
            default=None,
            metadata={
                "name": "Put_Integration_System_User_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutIntegrationSystemUserOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutIntegrationSystemUserOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutReferenceInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutReferenceInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutReferenceInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_reference_request: Optional[PutReferenceRequest] = field(
            default=None,
            metadata={
                "name": "Put_Reference_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class PutReferenceOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutReferenceOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_reference_response: Optional[PutReferenceResponse] = field(
            default=None,
            metadata={
                "name": "Put_Reference_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutReferenceOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutReferenceOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutSequenceGeneratorOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutSequenceGeneratorOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_sequence_generator_response: Optional[PutSequenceGeneratorResponse] = field(
            default=None,
            metadata={
                "name": "Put_Sequence_Generator_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutSequenceGeneratorOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutSequenceGeneratorOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class PutSubscriptionOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutSubscriptionOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_subscription_response: Optional[PutSubscriptionResponse] = field(
            default=None,
            metadata={
                "name": "Put_Subscription_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutSubscriptionOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutSubscriptionOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class ReassignBusinessProcessStepOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["ReassignBusinessProcessStepOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        reassign_business_process_step_response: Optional[ReassignBusinessProcessStepResponse] = (
            field(
                default=None,
                metadata={
                    "name": "Reassign_Business_Process_Step_Response",
                    "type": "Element",
                    "namespace": "urn:com.workday/bsvc",
                },
            )
        )
        fault: Optional["ReassignBusinessProcessStepOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["ReassignBusinessProcessStepOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class RescindBusinessProcessInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["RescindBusinessProcessInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["RescindBusinessProcessInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        rescind_business_process_request: Optional[RescindBusinessProcessRequest] = field(
            default=None,
            metadata={
                "name": "Rescind_Business_Process_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class RescindBusinessProcessOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["RescindBusinessProcessOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        rescind_business_process_response: Optional[RescindBusinessProcessResponse] = field(
            default=None,
            metadata={
                "name": "Rescind_Business_Process_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["RescindBusinessProcessOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["RescindBusinessProcessOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class SendBackBusinessProcessInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["SendBackBusinessProcessInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["SendBackBusinessProcessInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        send_back_business_process_request: Optional[SendBackBusinessProcessRequest] = field(
            default=None,
            metadata={
                "name": "Send_Back_Business_Process_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class SendBackBusinessProcessOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["SendBackBusinessProcessOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        send_back_business_process_response: Optional[SendBackBusinessProcessResponse] = field(
            default=None,
            metadata={
                "name": "Send_Back_Business_Process_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["SendBackBusinessProcessOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["SendBackBusinessProcessOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class EibExternalFileDataSourceDataType:
    """
    External File Data Source Data element.

    Attributes:
        integration_transport_protocol_data: Integration Transport Protocol Data element
        web_service_operation_reference: Web Service Operation Reference
        custom_object_reference: Custom Object Reference
    """

    class Meta:
        name = "EIB_External_File_Data_Source_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_transport_protocol_data: Optional[EibIntegrationTransportProtocolDataWwstype] = (
        field(
            default=None,
            metadata={
                "name": "Integration_Transport_Protocol_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
                "required": True,
            },
        )
    )
    web_service_operation_reference: Optional[WebServiceOperationObjectType] = field(
        default=None,
        metadata={
            "name": "Web_Service_Operation_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_object_reference: Optional[CustomObjectObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventDocumentsType:
    """
    For each Integration Event, this element contains all the available Documents.

    Attributes:
        integration_event_reference: Integration Event Reference
        repository_document
    """

    class Meta:
        name = "Event_DocumentsType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEventAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    repository_document: list[RepositoryDocumentSummaryDataType] = field(
        default_factory=list,
        metadata={
            "name": "Repository_Document",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDetailsRequest(GetEventDetailsRequestType):
    class Meta:
        name = "Get_Event_Details_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetEventDetailsResponseType:
    """
    Get_Event_Details response element.

    Attributes:
        request_references: This element contains the Event References submitted in the request.
        response_filter
        response_results
        response_data: This element contains the Event Details information.
        version
    """

    class Meta:
        name = "Get_Event_Details_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[EventRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[EventResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDocumentsRequest(GetEventDocumentsRequestType):
    class Meta:
        name = "Get_Event_Documents_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetHideWorkdayDeliveredReportRequest(GetHideWorkdayDeliveredReportRequestType):
    class Meta:
        name = "Get_Hide_Workday_Delivered_Report_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetHideWorkdayDeliveredReportResponseType:
    """Contains the response identifying the hidden Workday delivered reports."""

    class Meta:
        name = "Get_Hide_Workday_Delivered_Report_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[HideWorkdayDeliveredReportRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[HideWorkdayDeliveredReportResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetImportProcessMessagesRequest(GetImportProcessMessagesRequestType):
    class Meta:
        name = "Get_Import_Process_Messages_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetImportProcessMessagesResponseType:
    """
    Response.

    Attributes:
        request_criteria: Request Criteria
        response_filter: Response Filter
        response_results: Response Results
        response_data: Response Data
        version
    """

    class Meta:
        name = "Get_Import_Process_Messages_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_criteria: list[ImportProcessMessagesRequestCriteriaType] = field(
        default_factory=list,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: list[ResponseFilterType] = field(
        default_factory=list,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: list[ResponseResultsType] = field(
        default_factory=list,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: list[ImportProcessMessageResponseDataType] = field(
        default_factory=list,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetImportProcessesRequest(GetImportProcessesRequestType):
    class Meta:
        name = "Get_Import_Processes_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetIntegrationEventsRequest(GetIntegrationEventsRequestType):
    class Meta:
        name = "Get_Integration_Events_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetIntegrationSystemUsersRequest(GetIntegrationSystemUsersRequestType):
    class Meta:
        name = "Get_Integration_System_Users_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetIntegrationSystemsRequest(GetIntegrationSystemsRequestType):
    class Meta:
        name = "Get_Integration_Systems_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetReferencesRequest(GetReferencesRequestType):
    class Meta:
        name = "Get_References_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetReferencesResponseType:
    """Nature of Actions Request References Element."""

    class Meta:
        name = "Get_References_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_criteria: Optional[GetReferencesRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[GetReferencesResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetSequenceGeneratorsRequest(GetSequenceGeneratorsRequestType):
    class Meta:
        name = "Get_Sequence_Generators_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetSubscriptionsRequest(GetSubscriptionsRequestType):
    class Meta:
        name = "Get_Subscriptions_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class ImportProcessResponseDataType:
    """
    Import Process Response Data.

    Attributes:
        import_process: Import Process
    """

    class Meta:
        name = "Import_Process_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    import_process: list[ImportProcessType] = field(
        default_factory=list,
        metadata={
            "name": "Import_Process",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEventDataWwstype:
    """
    Encapsulating element containing all Integration Event data.

    Attributes:
        integration_system_reference: Reference element representing a unique instance of
            Integration System.
        process_description: Text attribute identifying the Summary of the Integration Event.
        initiated_date_time: A date/time representing the moment the Integration Event was Initiated
            (e.g. Launched).
        integration_response_message: Text attribute identifying the most recent message associated
            with the Integration Event.
        completed_date_time: A date/time representing the moment that the Integration Event
            completed.
        integration_event_member_reference: A unique reference for each member of this Integration
            Event.  This can be a valid instance for any subclass of Integratable (e.g. Employee,
            Organization, etc.).  Note that the references listed here will replace those already
            persisted on the Integration Event.
        initiated_by_system_account_reference: System Account Reference for the User that Initiated
            the process.
        percent_complete: Only use for Integrations that allow for a manual update of Percent
            Complete.
        integration_runtime_parameter_data: Integration Runtime Parameter Data
        integration_service_generated_sequence_data: Integration Service Generated Sequence Data
        integration_enterprise_event_records_data: Integration Enterprise Event Records Data
    """

    class Meta:
        name = "Integration_Event_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    process_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Process_Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    initiated_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Initiated_DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_response_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_Response_Message",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    completed_date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Completed_DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_event_member_reference: list[IntegratableObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Event_Member_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    initiated_by_system_account_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "Initiated_By_System_Account_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    percent_complete: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Percent_Complete",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 7,
            "fraction_digits": 4,
        },
    )
    integration_runtime_parameter_data: list[IntegrationRuntimeParameterDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Runtime_Parameter_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_service_generated_sequence_data: list[
        IntegrationServiceGeneratedSequenceDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Service_Generated_Sequence_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_enterprise_event_records_data: list[IntegrationEnterpriseEventRecordsDataType] = (
        field(
            default_factory=list,
            metadata={
                "name": "Integration_Enterprise_Event_Records_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )


@dataclass
class IntegrationEventReportingDetailsDataType:
    """
    Element for derived information regarding a Background Process Instance.

    Attributes:
        background_process_instance_status_reference: Background Process Instance Status
        parent_event_reference: This Integration Event is part of a parent Business Process event.
        background_process_message_data
        output_document_data
        consolidated_report_reference: Consolidated Report from ESB Server
        log_file_reference: Log File from ESB Server
    """

    class Meta:
        name = "Integration_Event_Reporting_Details_DataType"
        target_namespace = "urn:com.workday/bsvc"

    background_process_instance_status_reference: Optional[
        BackgroundProcessRuntimeStatusObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Background_Process_Instance_Status_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Parent_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    background_process_message_data: list[IntegrationMessageDetailDataType] = field(
        default_factory=list,
        metadata={
            "name": "Background_Process_Message_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    output_document_data: list[IntegrationRepositoryDocumentType] = field(
        default_factory=list,
        metadata={
            "name": "Output_Document_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    consolidated_report_reference: Optional[RepositoryDocumentAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Consolidated_Report_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    log_file_reference: list[RepositoryDocumentAbstractObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Log_File_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationFieldAttributesConfigurationDataType:
    """
    Integration Field Attributes Configuration Data.

    Attributes:
        integration_field_attributes_field_configuration_data: Integration Field Attributes Field
            Configuration Data
    """

    class Meta:
        name = "Integration_Field_Attributes_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_field_attributes_field_configuration_data: list[
        IntegrationFieldAttributesFieldConfigurationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Attributes_Field_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class IntegrationMapIntegrationMapValueDataWwstype:
    """
    Container element for Integration Map value.

    Attributes:
        integration_map_reference: Unique identifier for an Integration Map reference
        integration_map_name: Map Name
        default_value_data: Default Value
        integration_map_value_data
    """

    class Meta:
        name = "Integration_Map_Integration_Map_Value_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_map_reference: Optional[ExternalInstanceObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Map_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_map_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_Map_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    default_value_data: Optional[IntegrationAbstractValueDataType] = field(
        default=None,
        metadata={
            "name": "Default_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_map_value_data: list[IntegrationMapValueDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Map_Value_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationNotificationDataType:
    """
    Element containing configuration of Notifications.

    Attributes:
        trigger_on_launch: Trigger on Launch
        trigger_on_status_reference: Trigger on Status Reference (e.g. Completed, Failed)
        notification_condition_data: Notification Condition Data
        loops_on_external_field_reference: Loops On External Field Reference defines 1 or more
            related instances to iterate over before creating context for the Notification.
        notification_notifies_data
        security_group_reference: Security Group Reference that defines a list of users within the
            Workday system.
        email_address_data
        notification_subject_data: Workflow Notification Subject Data
        notification_body_data: Workflow Notification Body Data
        notification_attachment_data
    """

    class Meta:
        name = "Integration_Notification_DataType"
        target_namespace = "urn:com.workday/bsvc"

    trigger_on_launch: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Trigger_on_Launch",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    trigger_on_status_reference: list[BackgroundProcessRuntimeStatusObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Trigger_on_Status_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    notification_condition_data: list[IntegrationNotificationIntegrationConditionDataType] = field(
        default_factory=list,
        metadata={
            "name": "Notification_Condition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    loops_on_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Loops_On_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    notification_notifies_data: Optional[NotificationNotifiesDataType] = field(
        default=None,
        metadata={
            "name": "Notification_Notifies_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    security_group_reference: list[SecurityGroupObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Security_Group_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    email_address_data: list[InternetEmailAddressDataForNotificationsType] = field(
        default_factory=list,
        metadata={
            "name": "Email_Address_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    notification_subject_data: Optional[NotificationSubjectDataType] = field(
        default=None,
        metadata={
            "name": "Notification_Subject_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    notification_body_data: Optional[NotificationBodyDataType] = field(
        default=None,
        metadata={
            "name": "Notification_Body_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    notification_attachment_data: Optional[NotificationAttachmentDataType] = field(
        default=None,
        metadata={
            "name": "Notification_Attachment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationServiceComponentOverrideDataType:
    """
    Integration Service Component Override Data element.

    Attributes:
        data_source: If the Override Fields below pertain to the EIB's Data Source, mark this
            boolean TRUE.
        transformation: If the Override Fields below pertain to the EIB's Transformation, mark this
            boolean TRUE.
        file_utility: If the Override Fields below pertain to the EIB's File Utility (e.g. transport
            Payload), mark this boolean TRUE.
        transport_protocol: If the Override Fields below pertain to the EIB's Transport Protocol,
            mark this boolean TRUE.
        field_override_data
    """

    class Meta:
        name = "Integration_Service_Component_Override_DataType"
        target_namespace = "urn:com.workday/bsvc"

    data_source: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Data_Source",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    transformation: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Transformation",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    file_utility: Optional[bool] = field(
        default=None,
        metadata={
            "name": "File_Utility",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    transport_protocol: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Transport_Protocol",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    field_override_data: list[IntegrationServiceComponentFieldOverrideDataType] = field(
        default_factory=list,
        metadata={
            "name": "Field_Override_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class IntegrationSystemUserType:
    """
    Integration System User element.

    Attributes:
        integration_system_reference: Integration System Reference
        integration_system_user_data: Integration System User Data element
    """

    class Meta:
        name = "Integration_System_UserType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_system_user_data: Optional[IntegrationSystemUserDataType] = field(
        default=None,
        metadata={
            "name": "Integration_System_User_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationToolProviderIntegrationAttributeValuesDataWwstype:
    """
    Container element for all the Integration Attributes associated with a specific Attributable
    instance (e.g. Integration Template, Integration Service).

    Attributes:
        integration_attribute_provider_reference: Unique identifier for an Integration Attribute
            Provider reference
        integration_attribute_data
    """

    class Meta:
        name = "Integration_Tool_Provider_Integration_Attribute_Values_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_attribute_provider_reference: Optional[ExternalInstanceObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Attribute_Provider_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attribute_data: list[IntegrationAttributeIntegrationAttributeValueDataWwstype] = (
        field(
            default_factory=list,
            metadata={
                "name": "Integration_Attribute_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
                "min_occurs": 1,
            },
        )
    )


@dataclass
class IntegrationTransportProtocolDataWwstype:
    """Integration Transport Protocol Data element."""

    class Meta:
        name = "Integration_Transport_Protocol_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    email_transport_protocol_data: Optional[EmailTransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "Email_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    ftps_transport_protocol_data: Optional[FtpsTransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "FTPS_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    ftp_transport_protocol_data: Optional[FtpTransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "FTP_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    http_transport_protocol_data: Optional[HttpTransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "HTTP_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sftp_transport_protocol_data: Optional[SftpTransportProtocolDataWithDualAuthenticationType] = (
        field(
            default=None,
            metadata={
                "name": "SFTP_Transport_Protocol_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    workday_attachment_transport_protocol_data: Optional[
        WorkdayAttachmentTransportProtocolDataType
    ] = field(
        default=None,
        metadata={
            "name": "Workday_Attachment_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workday_web_service_transport_protocol_data: Optional[
        WorkdayWebServiceTransportProtocolDataType
    ] = field(
        default=None,
        metadata={
            "name": "Workday_Web_Service_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    as2_transport_protocol_data: Optional[As2TransportProtocolDataType] = field(
        default=None,
        metadata={
            "name": "AS2_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    extensibility_api_transport_protocol_data: Optional[
        EibExtensibilityApiTransportProtocolDataType
    ] = field(
        default=None,
        metadata={
            "name": "Extensibility_API_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    amazon_simple_storage_service_protocol_data: Optional[
        AmazonSimpleStorageServiceEibDeliveryProtocolDataType
    ] = field(
        default=None,
        metadata={
            "name": "Amazon_Simple_Storage_Service_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class JobIntegrationTransformationConfigurationDataType:
    """
    Transformation Configuration element.

    Attributes:
        integration_transformation_data: Integration Transformation Data element
    """

    class Meta:
        name = "Job_Integration_Transformation_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_transformation_data: list[IntegrationTransformationDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Transformation_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchIntegrationEventDataType:
    """
    Launch Integration Event Data.

    Attributes:
        integration_event_reference: Integration Event Reference
        integration_system_reference: Integration System Reference
        integration_service_endpoint: Integration Service Endpoint for Asynch consumption
        document_id: Document ID (Entry ID) from Repository Document
        event_initialization_document_id: Document ID (Entry ID) for Repository Document
            representing Event Initialization
        event_initialization_documents_data
        integration_template_reference: Integration Template Reference
        sent_on: Sent On
        system_user_reference: System User Reference
        resend_from_integration_event_reference: Resend from Integration Event Reference
        integration_runtime_parameter_data
        integration_service_generated_sequence_data
        parent_event_reference: This Integration Event is part of a parent Business Process event.
        win_integration: WIN Integration that runs on the Cloud ESB server
    """

    class Meta:
        name = "Launch_Integration_Event_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_reference: Optional[IntegrationSystemObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_service_endpoint: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_Service_Endpoint",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Document_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_initialization_document_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Event_Initialization_Document_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_initialization_documents_data: list[EventInitializationDocumentsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Event_Initialization_Documents_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_template_reference: Optional[IntegrationTemplateObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Template_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sent_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Sent_On",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    system_user_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "System_User_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    resend_from_integration_event_reference: Optional[IntegrationEventAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Resend_from_Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_runtime_parameter_data: list[IntegrationRuntimeParameterDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Runtime_Parameter_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_service_generated_sequence_data: list[
        IntegrationServiceGeneratedSequenceDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Service_Generated_Sequence_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parent_event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Parent_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    win_integration: Optional[bool] = field(
        default=None,
        metadata={
            "name": "WIN_Integration",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchIntegrationEventRequestType:
    """
    Launch Integration Event Request.

    Attributes:
        integration_system_reference: Integration System Reference
        integration_launch_parameter_data: Integration Launch Parameter Data
        listener_document_data: If Listener Service is enabled for this Integration, there may be
            documents added to the Event at Launch using this element.
        debug_mode: Launch in Debug mode only.  This means that the Integration Event will be
            created in the system, but the integration will not be run.  It will be the
            responsibility of the caller to utilize the runtime parameters within the response
            element to execute the integration.
        version
    """

    class Meta:
        name = "Launch_Integration_Event_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_launch_parameter_data: list[IntegrationLaunchParameterDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Launch_Parameter_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    listener_document_data: list[IntegrationRepositoryDocumentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Listener_Document_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    debug_mode: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Debug_Mode",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ParameterInitializationWwsDataType:
    """
    Defines the value to be used for parameter assignment.

    Attributes:
        boolean: Boolean
        currency: Currency
        date: Date
        date_time: DateTime
        numeric: Numeric
        text: Text
        business_object_instance_reference: Business Object Instance Reference
        enumeration_reference: Workday Integration Enumeration Reference
        external_field_reference: If Parameter Initialization Operator is "Determine Value at
            Runtime", then specify an External Field to be resolved at runtime.
        report_prompt_reference: If Parameter Initialization Operator is "Report Prompt", then
            specify a Report Prompt
        integration_parameter_reference: If Parameter Initialization Operator is "Document
            Parameter", then specify an Integration Parameter
        parameter_initialization_operator_reference: Parameter Initialization Operator Reference
        currency_reference: Currency Reference
    """

    class Meta:
        name = "Parameter_Initialization_WWS_DataType"
        target_namespace = "urn:com.workday/bsvc"

    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Currency",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    business_object_instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Business_Object_Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    enumeration_reference: Optional[IntegrationEnumerationObjectType] = field(
        default=None,
        metadata={
            "name": "Enumeration_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    report_prompt_reference: Optional[ExternalPromptableObjectType] = field(
        default=None,
        metadata={
            "name": "Report_Prompt_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_parameter_reference: Optional[IntegrationParameterReferenceType] = field(
        default=None,
        metadata={
            "name": "Integration_Parameter_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_initialization_operator_reference: Optional[
        ParameterInitializationOperatorObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Operator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    currency_reference: Optional[CurrencyObjectType] = field(
        default=None,
        metadata={
            "name": "Currency_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutHideWorkdayDeliveredReportRequest(PutHideWorkdayDeliveredReportRequestType):
    class Meta:
        name = "Put_Hide_Workday_Delivered_Report_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationMessageRequestType:
    """Integration Message request element."""

    class Meta:
        name = "Put_Integration_Message_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_message_data: Optional[IntegrationMessageDataType] = field(
        default=None,
        metadata={
            "name": "Integration_Message_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationSystemResponse(PutIntegrationSystemResponseType):
    class Meta:
        name = "Put_Integration_System_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationSystemUserRequestType:
    """
    Put Integration System User Request element.

    Attributes:
        integration_system_reference: Integration System Reference
        integration_system_user_data
        version
    """

    class Meta:
        name = "Put_Integration_System_User_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_user_data: Optional[IntegrationSystemUserDataType] = field(
        default=None,
        metadata={
            "name": "Integration_System_User_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSequenceGeneratorRequest(PutSequenceGeneratorRequestType):
    class Meta:
        name = "Put_Sequence_Generator_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class ReassignBusinessProcessStepRequest(ReassignBusinessProcessStepRequestType):
    class Meta:
        name = "Reassign_Business_Process_Step_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class SequenceGeneratorResponseDataType:
    """Sequence Generator Response Data."""

    class Meta:
        name = "Sequence_Generator_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    sequence_generator: list[SequenceGeneratorType] = field(
        default_factory=list,
        metadata={
            "name": "Sequence_Generator",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SimpleWorkDataParameterInitializationDataType:
    """
    Simple Work Data Parameter Initialization Data element.

    Attributes:
        simple_work_data_reference: Simple Work Data Reference
        parameter_initialization_data
    """

    class Meta:
        name = "Simple_Work_Data_Parameter_Initialization_DataType"
        target_namespace = "urn:com.workday/bsvc"

    simple_work_data_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Simple_Work_Data_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_initialization_data: Optional[ParameterInitializationDataType] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


class ApproveBusinessProcess:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = ApproveBusinessProcessInput
    output = ApproveBusinessProcessOutput


class CancelBusinessProcess:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = CancelBusinessProcessInput
    output = CancelBusinessProcessOutput


class CancelIntegrationEvent:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = CancelIntegrationEventInput
    output = CancelIntegrationEventOutput


class DeleteIntegrationSystem:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = DeleteIntegrationSystemInput
    output = DeleteIntegrationSystemOutput


class DenyBusinessProcess:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = DenyBusinessProcessInput
    output = DenyBusinessProcessOutput


@dataclass
class GetEventDetailInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetEventDetailInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetEventDetailInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_event_details_request: Optional[GetEventDetailsRequest] = field(
            default=None,
            metadata={
                "name": "Get_Event_Details_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetEventDocumentsInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetEventDocumentsInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetEventDocumentsInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_event_documents_request: Optional[GetEventDocumentsRequest] = field(
            default=None,
            metadata={
                "name": "Get_Event_Documents_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetHideWorkdayDeliveredReportInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetHideWorkdayDeliveredReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetHideWorkdayDeliveredReportInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_hide_workday_delivered_report_request: Optional[
            GetHideWorkdayDeliveredReportRequest
        ] = field(
            default=None,
            metadata={
                "name": "Get_Hide_Workday_Delivered_Report_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetImportProcessMessagesInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetImportProcessMessagesInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetImportProcessMessagesInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_import_process_messages_request: Optional[GetImportProcessMessagesRequest] = field(
            default=None,
            metadata={
                "name": "Get_Import_Process_Messages_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetImportProcessesInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetImportProcessesInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetImportProcessesInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_import_processes_request: Optional[GetImportProcessesRequest] = field(
            default=None,
            metadata={
                "name": "Get_Import_Processes_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetIntegrationEventsInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetIntegrationEventsInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetIntegrationEventsInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_integration_events_request: Optional[GetIntegrationEventsRequest] = field(
            default=None,
            metadata={
                "name": "Get_Integration_Events_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetIntegrationSystemUsersInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetIntegrationSystemUsersInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetIntegrationSystemUsersInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_integration_system_users_request: Optional[GetIntegrationSystemUsersRequest] = field(
            default=None,
            metadata={
                "name": "Get_Integration_System_Users_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetIntegrationSystemsInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetIntegrationSystemsInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetIntegrationSystemsInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_integration_systems_request: Optional[GetIntegrationSystemsRequest] = field(
            default=None,
            metadata={
                "name": "Get_Integration_Systems_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetReferencesInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetReferencesInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetReferencesInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_references_request: Optional[GetReferencesRequest] = field(
            default=None,
            metadata={
                "name": "Get_References_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetSequenceGeneratorsInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetSequenceGeneratorsInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetSequenceGeneratorsInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_sequence_generators_request: Optional[GetSequenceGeneratorsRequest] = field(
            default=None,
            metadata={
                "name": "Get_Sequence_Generators_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetSubscriptionsInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetSubscriptionsInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["GetSubscriptionsInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_subscriptions_request: Optional[GetSubscriptionsRequest] = field(
            default=None,
            metadata={
                "name": "Get_Subscriptions_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


class IncrementSequenceGenerator:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = IncrementSequenceGeneratorInput
    output = IncrementSequenceGeneratorOutput


@dataclass
class PutHideWorkdayDeliveredReportInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutHideWorkdayDeliveredReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutHideWorkdayDeliveredReportInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_hide_workday_delivered_report_request: Optional[
            PutHideWorkdayDeliveredReportRequest
        ] = field(
            default=None,
            metadata={
                "name": "Put_Hide_Workday_Delivered_Report_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class PutIntegrationSystemOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationSystemOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_system_response: Optional[PutIntegrationSystemResponse] = field(
            default=None,
            metadata={
                "name": "Put_Integration_System_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["PutIntegrationSystemOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["PutIntegrationSystemOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class PutReference:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutReferenceInput
    output = PutReferenceOutput


@dataclass
class PutSequenceGeneratorInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutSequenceGeneratorInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutSequenceGeneratorInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_sequence_generator_request: Optional[PutSequenceGeneratorRequest] = field(
            default=None,
            metadata={
                "name": "Put_Sequence_Generator_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class ReassignBusinessProcessStepInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["ReassignBusinessProcessStepInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["ReassignBusinessProcessStepInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        reassign_business_process_step_request: Optional[ReassignBusinessProcessStepRequest] = (
            field(
                default=None,
                metadata={
                    "name": "Reassign_Business_Process_Step_Request",
                    "type": "Element",
                    "namespace": "urn:com.workday/bsvc",
                },
            )
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


class RescindBusinessProcess:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = RescindBusinessProcessInput
    output = RescindBusinessProcessOutput


class SendBackBusinessProcess:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = SendBackBusinessProcessInput
    output = SendBackBusinessProcessOutput


@dataclass
class EventDocumentsResponseDataType:
    """Event Documents Response Data element."""

    class Meta:
        name = "Event_Documents_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    event_documents: list[EventDocumentsType] = field(
        default_factory=list,
        metadata={
            "name": "Event_Documents",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDetailsResponse(GetEventDetailsResponseType):
    class Meta:
        name = "Get_Event_Details_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetHideWorkdayDeliveredReportResponse(GetHideWorkdayDeliveredReportResponseType):
    class Meta:
        name = "Get_Hide_Workday_Delivered_Report_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetImportProcessMessagesResponse(GetImportProcessMessagesResponseType):
    class Meta:
        name = "Get_Import_Process_Messages_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetImportProcessesResponseType:
    """
    Get Import Processes Response element.

    Attributes:
        request_references: Import Process Request References
        response_filter: Parameters that let you filter the data returned in the response. You can
            filter returned data by dates and page attributes.
        response_results: The "Response_Results" element contains summary information about the data
            that has been returned from your request including "Total_Results", "Total_Pages", and
            the current "Page" returned.
        response_data: Import Process Response Data
        version
    """

    class Meta:
        name = "Get_Import_Processes_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[ImportProcessRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[ImportProcessResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetReferencesResponse(GetReferencesResponseType):
    class Meta:
        name = "Get_References_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetSequenceGeneratorsResponseType:
    """Response element containing instances of Sequence Generator and each of its associated
    data."""

    class Meta:
        name = "Get_Sequence_Generators_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[SequenceGeneratorRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[SequenceGeneratorResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationEventType:
    """
    Integration Event.

    Attributes:
        integration_event_reference: Integration Event Reference
        integration_event_data: Integration Event Data
        background_process_instance_data
    """

    class Meta:
        name = "Integration_EventType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_event_data: Optional[IntegrationEventDataWwstype] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    background_process_instance_data: Optional[IntegrationEventReportingDetailsDataType] = field(
        default=None,
        metadata={
            "name": "Background_Process_Instance_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationFieldOverrideParameterInitializationDataType:
    """
    For each parameter, assignment details.

    Attributes:
        external_parameter_reference: External Parameter Reference
        parameter_initialization_data: Parameter Initialization Data
    """

    class Meta:
        name = "Integration_Field_Override_Parameter_Initialization_DataType"
        target_namespace = "urn:com.workday/bsvc"

    external_parameter_reference: Optional[AbstractExternalParameterObjectType] = field(
        default=None,
        metadata={
            "name": "External_Parameter_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parameter_initialization_data: Optional[ParameterInitializationWwsDataType] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationParameterInitializationDataType:
    """
    Integration Parameter Initialization Data element.

    Attributes:
        launch_parameter_reference: Launch Parameter Reference
        parameter_initialization_data
    """

    class Meta:
        name = "Integration_Parameter_Initialization_DataType"
        target_namespace = "urn:com.workday/bsvc"

    launch_parameter_reference: Optional[LaunchParameterObjectType] = field(
        default=None,
        metadata={
            "name": "Launch_Parameter_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    parameter_initialization_data: Optional[ParameterInitializationWwsDataType] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationReportParameterInitializationDataType:
    """
    Integration Report Parameter Initialization Data element.

    Attributes:
        simple_work_data_reference: Simple Work Data Reference
        xml_name: XML Name
        parameter_initialization_data: Defines the value to be used for parameter assignment
    """

    class Meta:
        name = "Integration_Report_Parameter_Initialization_DataType"
        target_namespace = "urn:com.workday/bsvc"

    simple_work_data_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Simple_Work_Data_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    xml_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "XML_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_initialization_data: Optional[ParameterInitializationWwsDataType] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class IntegrationSystemUserResponseDataType:
    """Integration System User Response Data element."""

    class Meta:
        name = "Integration_System_User_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_user: list[IntegrationSystemUserType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_System_User",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationToolProviderIntegrationMapValuesDataWwstype:
    """
    Container element for all the Integration Maps associated with a specific Attributable instance
    (e.g. Integration Template, Integration Service).

    Attributes:
        integration_map_provider_reference: Unique identifier for an Integration Map Consumer
            reference
        integration_map_data
    """

    class Meta:
        name = "Integration_Tool_Provider_Integration_Map_Values_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_map_provider_reference: Optional[ExternalInstanceObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Map_Provider_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_map_data: list[IntegrationMapIntegrationMapValueDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Map_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class JobRetrievalInboundProtocolDataType:
    """
    Describes how the input file is retrieved.

    Attributes:
        attachment_data_source_data: Attachment Data Source data
        custom_report_data_source_data: Report Background Future Process data
        external_file_data_source
        rest_endpoint_data_source_reference: Rest Endpoint Data Source Reference
        rest_endpoint_data_source_data: REST Endpoint Data Source data
        web_service_data_source_reference: Web Service Data Source Reference
    """

    class Meta:
        name = "Job_Retrieval_Inbound_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    attachment_data_source_data: Optional[EibAttachmentDataSourceDataType] = field(
        default=None,
        metadata={
            "name": "Attachment_Data_Source_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_report_data_source_data: Optional[
        ReportBackgroundFutureProcessAsCustomReportDataType
    ] = field(
        default=None,
        metadata={
            "name": "Custom_Report_Data_Source_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_file_data_source: Optional[EibExternalFileDataSourceDataType] = field(
        default=None,
        metadata={
            "name": "External_File_Data_Source",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    rest_endpoint_data_source_reference: Optional[RestEndpointDataSourceObjectType] = field(
        default=None,
        metadata={
            "name": "REST_Endpoint_Data_Source_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    rest_endpoint_data_source_data: Optional[RestEndpointDataSourceDataType] = field(
        default=None,
        metadata={
            "name": "REST_Endpoint_Data_Source_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    web_service_data_source_reference: Optional[WebServiceDataSourceObjectType] = field(
        default=None,
        metadata={
            "name": "Web_Service_Data_Source_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchEibRequestType:
    """
    Launch EIB Request.

    Attributes:
        integration_system_reference: EIB Definition
        service_component_data
        version
    """

    class Meta:
        name = "Launch_EIB_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    service_component_data: list[IntegrationServiceComponentOverrideDataType] = field(
        default_factory=list,
        metadata={
            "name": "Service_Component_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchIntegrationEventRequest(LaunchIntegrationEventRequestType):
    class Meta:
        name = "Launch_Integration_Event_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationEventRequestType:
    """
    Integration event request element.

    Attributes:
        integration_event_reference: Reference element representing a unique instance of Integration
            Event.
        integration_event_data: Integration Event Data
        version
    """

    class Meta:
        name = "Put_Integration_Event_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event_reference: Optional[IntegrationEsbInvocationAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_event_data: Optional[IntegrationEventDataWwstype] = field(
        default=None,
        metadata={
            "name": "Integration_Event_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationMessageRequest(PutIntegrationMessageRequestType):
    class Meta:
        name = "Put_Integration_Message_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationSystemUserRequest(PutIntegrationSystemUserRequestType):
    class Meta:
        name = "Put_Integration_System_User_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class ReportParameterInitializationDataType:
    """
    Indicates how a report parameter is initialized.

    Attributes:
        xml_name: The XML name of the parameter
        simple_work_data_parameter_initialization_data: Details about how the parameter is
            initialized
    """

    class Meta:
        name = "Report_Parameter_Initialization_DataType"
        target_namespace = "urn:com.workday/bsvc"

    xml_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "XML_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    simple_work_data_parameter_initialization_data: Optional[
        SimpleWorkDataParameterInitializationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Simple_Work_Data_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )


@dataclass
class GetEventDetailOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetEventDetailOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_event_details_response: Optional[GetEventDetailsResponse] = field(
            default=None,
            metadata={
                "name": "Get_Event_Details_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetEventDetailOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetEventDetailOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class GetHideWorkdayDeliveredReportOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetHideWorkdayDeliveredReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_hide_workday_delivered_report_response: Optional[
            GetHideWorkdayDeliveredReportResponse
        ] = field(
            default=None,
            metadata={
                "name": "Get_Hide_Workday_Delivered_Report_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetHideWorkdayDeliveredReportOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetHideWorkdayDeliveredReportOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class GetImportProcessMessagesOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetImportProcessMessagesOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_import_process_messages_response: Optional[GetImportProcessMessagesResponse] = field(
            default=None,
            metadata={
                "name": "Get_Import_Process_Messages_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetImportProcessMessagesOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetImportProcessMessagesOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class GetReferencesOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetReferencesOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_references_response: Optional[GetReferencesResponse] = field(
            default=None,
            metadata={
                "name": "Get_References_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetReferencesOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetReferencesOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class LaunchIntegrationInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["LaunchIntegrationInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["LaunchIntegrationInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        launch_integration_event_request: Optional[LaunchIntegrationEventRequest] = field(
            default=None,
            metadata={
                "name": "Launch_Integration_Event_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


class PutHideWorkdayDeliveredReport:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutHideWorkdayDeliveredReportInput
    output = PutHideWorkdayDeliveredReportOutput


@dataclass
class PutIntegrationMessageInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationMessageInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutIntegrationMessageInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_message_request: Optional[PutIntegrationMessageRequest] = field(
            default=None,
            metadata={
                "name": "Put_Integration_Message_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class PutIntegrationSystemUserInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationSystemUserInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutIntegrationSystemUserInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_system_user_request: Optional[PutIntegrationSystemUserRequest] = field(
            default=None,
            metadata={
                "name": "Put_Integration_System_User_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


class PutSequenceGenerator:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutSequenceGeneratorInput
    output = PutSequenceGeneratorOutput


class ReassignBusinessProcessStep:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = ReassignBusinessProcessStepInput
    output = ReassignBusinessProcessStepOutput


@dataclass
class DynamicFilenameDefinitionAssignmentDataType:
    """
    Dynamic Filename Definition Assignment Data element.

    Attributes:
        tag_reference: Dynamic Filename Definition Tag
        report_prompt_reference: Report Prompt
        external_field_reference: External Field
        field_prompt: Field Prompt
    """

    class Meta:
        name = "Dynamic_Filename_Definition_Assignment_DataType"
        target_namespace = "urn:com.workday/bsvc"

    tag_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Tag_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    report_prompt_reference: Optional[ExternalPromptableObjectType] = field(
        default=None,
        metadata={
            "name": "Report_Prompt_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    field_prompt: list[IntegrationFieldOverrideParameterInitializationDataType] = field(
        default_factory=list,
        metadata={
            "name": "Field_Prompt",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class ExtendedIntegrationDocumentFieldDataType:
    """
    Integration Document Field for Document Extension Data.

    Attributes:
        field_name: Field Name
        description: Field Description
        field_data_type_reference: Field Data Type Reference
        reference_id_type: Reference ID Type
        external_field_reference: External Field Content
        document_builder_reference: Document Builder Reference
        loops_on_external_field_reference: Loops On External Field Reference
        loop_on_order_external_field_reference: Loop On Order External Field Reference
        descending: Order the loop on in descending order
        integration_field_override_parameter_initialization_data
        integration_document_field_options
    :ivar
        integration_document_stacks_for_integration_document_field_configuration_data:
    """

    class Meta:
        name = "Extended_Integration_Document_Field_DataType"
        target_namespace = "urn:com.workday/bsvc"

    field_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Field_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    field_data_type_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Field_Data_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    reference_id_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reference_ID_Type",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    document_builder_reference: Optional[GenericDocumentBuilderAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Document_Builder_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    loops_on_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Loops_On_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    loop_on_order_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Loop_On_Order_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    descending: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Descending",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_field_override_parameter_initialization_data: list[
        IntegrationFieldOverrideParameterInitializationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Override_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_stacks_for_integration_document_field_configuration_data: list[
        IntegrationDocumentStackDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Stacks_for_Integration_Document_Field_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_field_options: list[IntegrationDocumentFieldOptionsType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Field_Options",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDocumentsResponseType:
    """Get Event Documents Response element."""

    class Meta:
        name = "Get_Event_Documents_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationEventRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[EventDocumentsResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetImportProcessesResponse(GetImportProcessesResponseType):
    class Meta:
        name = "Get_Import_Processes_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetIntegrationSystemUsersResponseType:
    """Root Response Element."""

    class Meta:
        name = "Get_Integration_System_Users_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationSystemRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[IntegrationSystemRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[IntegrationSystemUserResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetSequenceGeneratorsResponse(GetSequenceGeneratorsResponseType):
    class Meta:
        name = "Get_Sequence_Generators_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationEventResponseDataType:
    """
    Integration Event Response Data.

    Attributes:
        integration_event: Integration Event
    """

    class Meta:
        name = "Integration_Event_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event: list[IntegrationEventType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Event",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationFieldOverrideFieldConfigurationDataType:
    """
    Integration Document Field Override Configuration Data.

    Attributes:
        field_reference: Document Field Reference
        external_field_reference: External Field Content
        external_parameter_assignment_data: External Parameter Assignment Data
        required_field: If this field is to be included in the Output document, denotes whether
            there must be a value supplied for this field.  If there is not a value, then error
            handling should occur.
        maximum_length: If this field is to be included in the Output document, denotes whether
            there should be a maximum length enforced for this field.  If the value, exceeds the
            maximum length then special handling should occur.
    """

    class Meta:
        name = "Integration_Field_Override_Field_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    field_reference: Optional[IntegrationDocumentFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_parameter_assignment_data: list[
        IntegrationFieldOverrideParameterInitializationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "External_Parameter_Assignment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    required_field: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Required_Field",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    maximum_length: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Maximum_Length",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 6,
            "fraction_digits": 0,
        },
    )


@dataclass
class IntegrationParameterAssignmentDataType:
    """
    Parameter Data.

    Attributes:
        integration_parameter_name: Integration Parameter Name
        data_type_external_field_reference: Defines Data Type of Parameter Assignment
        boolean: Boolean
        currency: Currency
        date: Date
        date_time: DateTime
        time: Time
        numeric: Numeric
        text: Text
        business_object_instance_reference: Business Object Instance Reference
        external_field_reference: If Parameter Initialization Operator is "Determine Value at
            Runtime", then specify an External Field to be resolved at runtime.
        integration_attribute_reference: Parameter assigns using value from Integration Attribute
        launch_parameter_reference: Parameter assigns using value from Launch Parameter
        date_from_date_time_zone: Date from DateTimeZone
        time_from_date_time_zone: Time from DateTimeZone
        time_zone_from_date_time_zone_reference: Time Zone from DateTimeZone
        parameter_initialization_operator_reference: Parameter Initialization Operator Reference
        integration_field_override_parameter_initialization_data
        currency_reference: Currency Reference
        integration_document_stack_data
        global_value: Context of Integration Event.  If FALSE, then takes the Context of the level
            within the Document.
    """

    class Meta:
        name = "Integration_Parameter_Assignment_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_parameter_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_Parameter_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    data_type_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Data_Type_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    boolean: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Boolean",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    currency: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Currency",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DateTime",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    time: Optional[XmlTime] = field(
        default=None,
        metadata={
            "name": "Time",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    numeric: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Numeric",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 26,
            "fraction_digits": 6,
        },
    )
    text: Optional[str] = field(
        default=None,
        metadata={
            "name": "Text",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    business_object_instance_reference: list[InstanceObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Business_Object_Instance_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attribute_reference: Optional[IntegrationAttributeObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Attribute_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    launch_parameter_reference: Optional[LaunchParameterObjectType] = field(
        default=None,
        metadata={
            "name": "Launch_Parameter_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    date_from_date_time_zone: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Date_from_DateTimeZone",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    time_from_date_time_zone: Optional[XmlTime] = field(
        default=None,
        metadata={
            "name": "Time_from_DateTimeZone",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    time_zone_from_date_time_zone_reference: Optional[TimeZoneObjectType] = field(
        default=None,
        metadata={
            "name": "TimeZone_from_DateTimeZone_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    parameter_initialization_operator_reference: Optional[
        ParameterInitializationOperatorObjectType
    ] = field(
        default=None,
        metadata={
            "name": "Parameter_Initialization_Operator_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_field_override_parameter_initialization_data: list[
        IntegrationFieldOverrideParameterInitializationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Override_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    currency_reference: Optional[CurrencyObjectType] = field(
        default=None,
        metadata={
            "name": "Currency_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_stack_data: list[IntegrationDocumentStackDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Stack_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    global_value: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Global",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationScheduledFutureProcessDataType:
    """
    Integration Scheduled Future Process Data element.

    Attributes:
        integration_system_reference: Unique identifier for an Integration System reference
        integration_parameter_initialization_data
        integration_report_parameter_initialization_data
        concurrency_configuration_data
    """

    class Meta:
        name = "Integration_Scheduled_Future_Process_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_parameter_initialization_data: list[IntegrationParameterInitializationDataType] = (
        field(
            default_factory=list,
            metadata={
                "name": "Integration_Parameter_Initialization_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    integration_report_parameter_initialization_data: list[
        IntegrationReportParameterInitializationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Report_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    concurrency_configuration_data: Optional[ConcurrencyConfigurationDataType] = field(
        default=None,
        metadata={
            "name": "Concurrency_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class JobIntegrationRetrievalProtocolDataType:
    """
    Describes how the Job Integration Retrieval Configuration (Audited) is configured.

    Attributes:
        inbound_protocol_data: Describes how the input file is retrieved
        pgp_decryption_settings_data: Decryption on the input file
        filename: Name of the input file
        restricted_to_environment_reference: Unique identifier for an OMS Environment reference
        decompress: Decompress the input file after retrieval
        delete_after_retrieval: Delete the input file from the remote endpoint after retrieval
        decrypt_using_aws_kms_key: If specified, the AWS KMS Key alias used to decrypt the payload
        kms_region: AWS Bucket Region for Inbound EIB
    """

    class Meta:
        name = "Job_Integration_Retrieval_Protocol_DataType"
        target_namespace = "urn:com.workday/bsvc"

    inbound_protocol_data: Optional[JobRetrievalInboundProtocolDataType] = field(
        default=None,
        metadata={
            "name": "Inbound_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    pgp_decryption_settings_data: Optional[PgpDecryptionSettingsDataType] = field(
        default=None,
        metadata={
            "name": "PGP_Decryption_Settings_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    filename: Optional[str] = field(
        default=None,
        metadata={
            "name": "Filename",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    restricted_to_environment_reference: list[OmsEnvironmentObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Restricted_To_Environment_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    decompress: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Decompress",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    delete_after_retrieval: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Delete_After_Retrieval",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    decrypt_using_aws_kms_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Decrypt_using_AWS_KMS_Key",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    kms_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "KMS_Region",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchEibRequest(LaunchEibRequestType):
    class Meta:
        name = "Launch_EIB_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class LaunchEibResponseType:
    """Launch EIB Response."""

    class Meta:
        name = "Launch_EIB_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    application_instance_exceptions: list[ApplicationInstanceExceptionsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Application_Instance_Exceptions",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_event: Optional[IntegrationEventType] = field(
        default=None,
        metadata={
            "name": "Integration_Event",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchIntegrationEventResponseType:
    """
    Launch Integration Event Response.

    Attributes:
        integration_event: Integration Event
        launch_integration_event_data
        application_instance_exceptions
        debug_mode: Launch in Debug mode only.  This means that the Integration Event will be
            created in the system, but the integration will not be run.  It will be the
            responsibility of the caller to utilize the runtime parameters within the response
            element to execute the integration.
        version
    """

    class Meta:
        name = "Launch_Integration_Event_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    integration_event: Optional[IntegrationEventType] = field(
        default=None,
        metadata={
            "name": "Integration_Event",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    launch_integration_event_data: Optional[LaunchIntegrationEventDataType] = field(
        default=None,
        metadata={
            "name": "Launch_Integration_Event_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    application_instance_exceptions: list[ApplicationInstanceExceptionsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Application_Instance_Exceptions",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    debug_mode: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Debug_Mode",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class OverriddenIntegrationDocumentFieldDataType:
    """
    Integration Document Field for Override Data.

    Attributes:
        integration_document_field_reference: Document Field Reference
        external_field_reference: External Field Content
        integration_field_override_parameter_initialization_data: Integration Field Override
            Parameter Initialization Data
        integration_document_field_options: Integration Document Field Options
    :ivar
        integration_document_stacks_for_integration_document_field_configuration_data:
        Integration Document Stacks for Integration Document Field
        Configuration Data
    """

    class Meta:
        name = "Overridden_Integration_Document_Field_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_document_field_reference: Optional[IntegrationDocumentFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Document_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_field_override_parameter_initialization_data: list[
        IntegrationFieldOverrideParameterInitializationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Override_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_stacks_for_integration_document_field_configuration_data: list[
        IntegrationDocumentStackDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Stacks_for_Integration_Document_Field_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_field_options: list[IntegrationDocumentFieldOptionsType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Field_Options",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PopulationEligibilityDataType:
    """
    Post Population Predicate.

    Attributes:
        external_field_reference: External Field
        integration_field_override_parameter_initialization_data: External Field Parameters
    """

    class Meta:
        name = "Population_Eligibility_DataType"
        target_namespace = "urn:com.workday/bsvc"

    external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_field_override_parameter_initialization_data: list[
        IntegrationFieldOverrideParameterInitializationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Override_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationEventRequest(PutIntegrationEventRequestType):
    class Meta:
        name = "Put_Integration_Event_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class WorkflowReportGroupStepBackgroundFutureProcessDefinitionDataType:
    """
    A scheduled future process for a report group definition.

    Attributes:
        report_group_reference: The Report Group that this process executes.
        report_parameter_initialization_data
        do_not_output_empty_report: Indicates if empty reports will be outputted.
        file_expiration_in_days: The expiration period for the created file
    """

    class Meta:
        name = "Workflow_Report_Group_Step_Background_Future_Process_Definition_DataType"
        target_namespace = "urn:com.workday/bsvc"

    report_group_reference: Optional[ReportGroupObjectType] = field(
        default=None,
        metadata={
            "name": "Report_Group_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    report_parameter_initialization_data: list[ReportParameterInitializationDataType] = field(
        default_factory=list,
        metadata={
            "name": "Report_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    do_not_output_empty_report: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Do_Not_Output_Empty_Report",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    file_expiration_in_days: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "File_Expiration_in_Days",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
            "total_digits": 4,
            "fraction_digits": 0,
        },
    )


@dataclass
class WorkflowStepReportBackgroundProcessDefinitionDataType:
    """
    A scheduled future process for a custom report definition or a report task.

    Attributes:
        document_type_reference: The type of document created
        custom_business_form_layout_reference: The Custom Business Form Layout for the Custom Report
            Definition or the Referenced Report Task.
        delivered_business_form_layout_reference: The Delivered Business Form Layout for the
            Referenced Report Task.
        referenced_task_reference: The task that this process runs
        tenanted_report_definition_reference: The Custom Report Definition this process is for
        report_parameter_initialization_data: Indicates how a report parameter is initialized
        report_tags_reference: Indicates the Report Tags to associate with the report.
        file_expiration_in_days: The expiration period for the created file
        do_not_output_an_empty_report: Indicates if empty reports will be outputted.
        hide_prompt_values: If the output type is Excel or CSV, this field determines whether prompt
            values will be hidden from the output.
    """

    class Meta:
        name = "Workflow_Step_Report_Background_Process_Definition_DataType"
        target_namespace = "urn:com.workday/bsvc"

    document_type_reference: Optional[DocumentTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Document_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    custom_business_form_layout_reference: Optional[CustomBusinessFormLayoutObjectType] = field(
        default=None,
        metadata={
            "name": "Custom_Business_Form_Layout_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    delivered_business_form_layout_reference: Optional[DeliveredBusinessFormLayoutObjectType] = (
        field(
            default=None,
            metadata={
                "name": "Delivered_Business_Form_Layout_Reference",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    referenced_task_reference: Optional[ReferencedTaskObjectType] = field(
        default=None,
        metadata={
            "name": "Referenced_Task_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    tenanted_report_definition_reference: Optional[CustomReportDefinitionObjectType] = field(
        default=None,
        metadata={
            "name": "Tenanted_Report_Definition_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    report_parameter_initialization_data: list[ReportParameterInitializationDataType] = field(
        default_factory=list,
        metadata={
            "name": "Report_Parameter_Initialization_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    report_tags_reference: list[ReportTagObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Report_Tags_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    file_expiration_in_days: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "File_Expiration_in_Days",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "total_digits": 4,
            "fraction_digits": 0,
        },
    )
    do_not_output_an_empty_report: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Do_Not_Output_an_Empty_Report",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    hide_prompt_values: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Hide_Prompt_Values",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


class GetEventDetail:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetEventDetailInput
    output = GetEventDetailOutput


class GetHideWorkdayDeliveredReport:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetHideWorkdayDeliveredReportInput
    output = GetHideWorkdayDeliveredReportOutput


class GetImportProcessMessages:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetImportProcessMessagesInput
    output = GetImportProcessMessagesOutput


@dataclass
class GetImportProcessesOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetImportProcessesOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_import_processes_response: Optional[GetImportProcessesResponse] = field(
            default=None,
            metadata={
                "name": "Get_Import_Processes_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetImportProcessesOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetImportProcessesOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class GetReferences:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetReferencesInput
    output = GetReferencesOutput


@dataclass
class GetSequenceGeneratorsOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetSequenceGeneratorsOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_sequence_generators_response: Optional[GetSequenceGeneratorsResponse] = field(
            default=None,
            metadata={
                "name": "Get_Sequence_Generators_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetSequenceGeneratorsOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetSequenceGeneratorsOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class LaunchEibInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["LaunchEibInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["LaunchEibInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        launch_eib_request: Optional[LaunchEibRequest] = field(
            default=None,
            metadata={
                "name": "Launch_EIB_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class PutIntegrationEventInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationEventInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutIntegrationEventInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_event_request: Optional[PutIntegrationEventRequest] = field(
            default=None,
            metadata={
                "name": "Put_Integration_Event_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


class PutIntegrationMessage:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutIntegrationMessageInput
    output = PutIntegrationMessageOutput


class PutIntegrationSystemUser:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutIntegrationSystemUserInput
    output = PutIntegrationSystemUserOutput


@dataclass
class DynamicFilenameDefinitionDataType:
    """
    Dynamic Filename Definition Data element.

    Attributes:
        filename_definition: Dynamic Filename Definition Filename Expression
        dynamic_filename_definition_assignment_data
    """

    class Meta:
        name = "Dynamic_Filename_Definition_DataType"
        target_namespace = "urn:com.workday/bsvc"

    filename_definition: Optional[str] = field(
        default=None,
        metadata={
            "name": "Filename_Definition",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    dynamic_filename_definition_assignment_data: list[
        DynamicFilenameDefinitionAssignmentDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Dynamic_Filename_Definition_Assignment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetEventDocumentsResponse(GetEventDocumentsResponseType):
    class Meta:
        name = "Get_Event_Documents_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetIntegrationEventsResponseType:
    """
    Get Integration Events Response.

    Attributes:
        request_references: Request References
        request_criteria: Request Criteria
        response_filter: Response Filter
        response_results: Response Results
        response_data: Response Data
        response_invalid_references
        version
    """

    class Meta:
        name = "Get_Integration_Events_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationEventRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[IntegrationEventRequestCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[IntegrationEventResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_invalid_references: list[InvalidReferenceIdResponseType] = field(
        default_factory=list,
        metadata={
            "name": "Response_Invalid_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetIntegrationSystemUsersResponse(GetIntegrationSystemUsersResponseType):
    class Meta:
        name = "Get_Integration_System_Users_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationBackgroundProcessDefinitionDataType:
    """
    Integration Background Process Definition Data element.

    Attributes:
        process_description: When Integration Event is created for this Background Future Process,
            this text will be used for its Process Description
        dynamic_description_external_field_reference: When Integration Event is created for this
            Background Future Process, the result of this External Field will be used for its
            Process Description
        integration_background_process_data
    """

    class Meta:
        name = "Integration_Background_Process_Definition_DataType"
        target_namespace = "urn:com.workday/bsvc"

    process_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Process_Description",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    dynamic_description_external_field_reference: Optional[ExternalFieldObjectType] = field(
        default=None,
        metadata={
            "name": "Dynamic_Description_External_Field_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_background_process_data: Optional[IntegrationScheduledFutureProcessDataType] = (
        field(
            default=None,
            metadata={
                "name": "Integration_Background_Process_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
                "required": True,
            },
        )
    )


@dataclass
class IntegrationDataInitializationConfigurationDataType:
    """
    Integration Data Initialization Configuration Data.

    Attributes:
        integration_field_attributes_field_configuration_data: Integration Field Attributes Field
            Configuration Data
        population_eligibility_data: Post Population Predicate
    """

    class Meta:
        name = "Integration_Data_Initialization_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_field_attributes_field_configuration_data: list[
        IntegrationFieldAttributesFieldConfigurationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Field_Attributes_Field_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    population_eligibility_data: Optional[PopulationEligibilityDataType] = field(
        default=None,
        metadata={
            "name": "Population_Eligibility_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationDataInitializationOverrideConfigurationDataType:
    """
    Integration Data Initialization Override Configuration Data.

    Attributes:
        parameter_data: Parameter Data
        integration_document_field_for_field_override_data: Integration Document Field for Field
            Override Data
        integration_document_field_for_document_extension_data: Integration Document Field for
            Document Extension Data
    """

    class Meta:
        name = "Integration_Data_Initialization_Override_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    parameter_data: list[IntegrationParameterAssignmentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Parameter_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_field_for_field_override_data: list[
        OverriddenIntegrationDocumentFieldDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Field_for_Field_Override_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_field_for_document_extension_data: list[
        ExtendedIntegrationDocumentFieldDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Field_for_Document_Extension_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationFieldOverrideConfigurationDataType:
    """
    Integration Field Override Configuration Data.

    Attributes:
        integration_business_object_reference: Integration Business Object Reference for DFO
            Services
        integration_document_field_override_configuration_data: Integration Document Field Override
            Configuration Data
    """

    class Meta:
        name = "Integration_Field_Override_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_business_object_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Business_Object_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_document_field_override_configuration_data: list[
        IntegrationFieldOverrideFieldConfigurationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Document_Field_Override_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_occurs": 1,
        },
    )


@dataclass
class JobIntegrationRetrievalConfigurationDataType:
    """
    Contains Information about the configuration of a Job Integration Retrieval Configuration, used
    for configuring an EIB retrieval step.

    Attributes:
        integration_data_source_data: Describes how the Job Integration Retrieval Configuration
            (Audited) is configured
    """

    class Meta:
        name = "Job_Integration_Retrieval_Configuration_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_data_source_data: list[JobIntegrationRetrievalProtocolDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Data_Source_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class LaunchEibResponse(LaunchEibResponseType):
    class Meta:
        name = "Launch_EIB_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class LaunchIntegrationEventResponse(LaunchIntegrationEventResponseType):
    class Meta:
        name = "Launch_Integration_Event_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetEventDocumentsOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetEventDocumentsOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_event_documents_response: Optional[GetEventDocumentsResponse] = field(
            default=None,
            metadata={
                "name": "Get_Event_Documents_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetEventDocumentsOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetEventDocumentsOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class GetImportProcesses:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetImportProcessesInput
    output = GetImportProcessesOutput


@dataclass
class GetIntegrationSystemUsersOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetIntegrationSystemUsersOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_integration_system_users_response: Optional[GetIntegrationSystemUsersResponse] = field(
            default=None,
            metadata={
                "name": "Get_Integration_System_Users_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetIntegrationSystemUsersOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetIntegrationSystemUsersOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class GetSequenceGenerators:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetSequenceGeneratorsInput
    output = GetSequenceGeneratorsOutput


@dataclass
class LaunchEibOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["LaunchEibOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        launch_eib_response: Optional[LaunchEibResponse] = field(
            default=None,
            metadata={
                "name": "Launch_EIB_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["LaunchEibOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["LaunchEibOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class LaunchIntegrationOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["LaunchIntegrationOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        launch_integration_event_response: Optional[LaunchIntegrationEventResponse] = field(
            default=None,
            metadata={
                "name": "Launch_Integration_Event_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["LaunchIntegrationOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["LaunchIntegrationOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class PutIntegrationEvent:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutIntegrationEventInput
    output = PutIntegrationEventOutput


@dataclass
class GetIntegrationEventsResponse(GetIntegrationEventsResponseType):
    class Meta:
        name = "Get_Integration_Events_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationFileUtilityDataType:
    """
    File Utility Data element.

    Attributes:
        id: Unique identifier
        filename: Filename to use when creating the file, without file extension validations.
        sequence_generator_data
        dynamic_filename_definition_data
        mime_type_reference: Mime Type Reference
        compressed: Compressed
        document_retention_policy: Number of Days to keep the resulting document.  Maximum is 180
            Days.  If set to 0, the document will not be retained for access after the integration
            has executed. Note that a Document Retention Policy is required when used in conjunction
            with any Workday Attachment Transport Protocol.
        pgp_encryption_settings_data
        encrypt_using_aws_kms_key: Amazon Key Management Service (KMS) Key Alias to use to encrypt.
        kms_region: AWS KMS Region for Outbound EIB
        transfer_acceleration_enabled: Enable Transfer Acceleration when delivering the file to an
            Amazon S3 bucket.
        storage_class: Amazon Simple Storage Service (S3) Storage Class to use when storing the
            object in the bucket.
    """

    class Meta:
        name = "Integration_File_Utility_DataType"
        target_namespace = "urn:com.workday/bsvc"

    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    filename: Optional[str] = field(
        default=None,
        metadata={
            "name": "Filename",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 255,
        },
    )
    sequence_generator_data: Optional[AbstractSequenceGeneratorDataType] = field(
        default=None,
        metadata={
            "name": "Sequence_Generator_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    dynamic_filename_definition_data: Optional[DynamicFilenameDefinitionDataType] = field(
        default=None,
        metadata={
            "name": "Dynamic_Filename_Definition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    mime_type_reference: Optional[MimeTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Mime_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    compressed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Compressed",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    document_retention_policy: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Document_Retention_Policy",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "min_inclusive": Decimal("0"),
            "total_digits": 12,
            "fraction_digits": 0,
        },
    )
    pgp_encryption_settings_data: Optional[PgpEncryptionSettingsDataType] = field(
        default=None,
        metadata={
            "name": "PGP_Encryption_Settings_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    encrypt_using_aws_kms_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "Encrypt_using_AWS_KMS_Key",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    kms_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "KMS_Region",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    transfer_acceleration_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Transfer_Acceleration_Enabled",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    storage_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "Storage_Class",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SubscriptionDataType:
    """
    Subscription Data element.

    Attributes:
        subscriber_reference: Subscriber Reference
        endpoint_info_data
        run_as_user_reference: System User to use to fire the Integration Background Future Process
        integration_background_future_process_data
        subscribe_to_all_transaction_types: Subscribe to all Transaction Types (e.g. both Business
            Processes and Event Lites)
        excluded_transaction_log_type_reference: Subscribe to all Transaction Types except for the
            specified Transaction Types
        subscribe_to_all_business_processes: Subscribe to all Business Processes
        excluded_business_process_type_reference: Subscribe to all Business Processes except for the
            specified Business Processes
        included_transaction_log_type_reference: Subscribe to specific Transaction Log Type
        subscription_condition_data
    """

    class Meta:
        name = "Subscription_DataType"
        target_namespace = "urn:com.workday/bsvc"

    subscriber_reference: Optional[SubscriberObjectType] = field(
        default=None,
        metadata={
            "name": "Subscriber_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    endpoint_info_data: list[ExternalEndpointDataType] = field(
        default_factory=list,
        metadata={
            "name": "Endpoint_Info_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    run_as_user_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "Run_As_User_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_background_future_process_data: Optional[
        IntegrationBackgroundProcessDefinitionDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Background_Future_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscribe_to_all_transaction_types: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Subscribe_to_all_Transaction_Types",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    excluded_transaction_log_type_reference: list[TransactionLogTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Excluded_Transaction_Log_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscribe_to_all_business_processes: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Subscribe_to_all_Business_Processes",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    excluded_business_process_type_reference: list[BusinessProcessTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Excluded_Business_Process_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    included_transaction_log_type_reference: list[TransactionLogTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Included_Transaction_Log_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_condition_data: list[SubscriptionConditionDataType] = field(
        default_factory=list,
        metadata={
            "name": "Subscription_Condition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SubscriptionDataWwstype:
    """
    Subscription Data element.

    Attributes:
        endpoint_info_data
        system_user_to_fire_integration_reference: System User to Fire Integration
        integration_background_future_process_data
        subscribe_to_all_transaction_types: Subscribe to all Transaction Types
        transaction_log_type_excluded_from_subscription_reference: Subscribe to all Transaction
            Types except this Transaction Type
        subscribe_to_all_business_processes: Subscribe to all Business Processes
        business_process_type_excluded_from_subscription_reference: Subscribe to all Business
            Process Types except this Business Process Type
        specific_transaction_type_for_suscription_reference: Subscribe to specific Transaction Types
        subscription_condition_data
    """

    class Meta:
        name = "Subscription_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    endpoint_info_data: list[ExternalEndpointDataType] = field(
        default_factory=list,
        metadata={
            "name": "Endpoint_Info_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    system_user_to_fire_integration_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "System_User_to_Fire_Integration_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_background_future_process_data: list[
        IntegrationBackgroundProcessDefinitionDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Background_Future_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscribe_to_all_transaction_types: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Subscribe_to_all_Transaction_Types",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    transaction_log_type_excluded_from_subscription_reference: list[
        TransactionLogTypeObjectType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Transaction_Log_Type_Excluded_from_Subscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscribe_to_all_business_processes: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Subscribe_to_all_Business_Processes",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    business_process_type_excluded_from_subscription_reference: list[
        BusinessProcessTypeObjectType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Business_Process_Type_Excluded_From_Subscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    specific_transaction_type_for_suscription_reference: list[TransactionLogTypeObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Specific_Transaction_Type_for_Suscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_condition_data: list[SubscriptionConditionDataType] = field(
        default_factory=list,
        metadata={
            "name": "Subscription_Condition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkflowStepContentDataType:
    """
    Some details about a step in a Business Process (Workflow)

    Attributes:
        order: The order of this Step within the Workflow
        workflow_step_type_reference: The type of this Step
        task_reference: A Referenced Task that is triggered by this Step
        checklist_reference: A Checklist that is triggered by this Step
        report_background_process_definition_data: A Report Background Future Process that is
            triggered by this Step
        report_group_background_process_definition_data
        partitioned_background_process_reference: A Partitioned Background Process that is triggered
            by this Step
        to_do_reference: A To Do that is triggered by this Step
        event_service_reference: An Event Service that is triggered by this Step
        integration_background_process_definition_data: An Integration Background Future Process
            that is triggered by this Step
    """

    class Meta:
        name = "Workflow_Step_Content_DataType"
        target_namespace = "urn:com.workday/bsvc"

    order: Optional[str] = field(
        default=None,
        metadata={
            "name": "Order",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workflow_step_type_reference: Optional[WorkflowStepTypeObjectType] = field(
        default=None,
        metadata={
            "name": "Workflow_Step_Type_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    task_reference: Optional[ReferencedTaskObjectType] = field(
        default=None,
        metadata={
            "name": "Task_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    checklist_reference: Optional[ChecklistObjectType] = field(
        default=None,
        metadata={
            "name": "Checklist_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    report_background_process_definition_data: Optional[
        WorkflowStepReportBackgroundProcessDefinitionDataType
    ] = field(
        default=None,
        metadata={
            "name": "Report_Background_Process_Definition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    report_group_background_process_definition_data: Optional[
        WorkflowReportGroupStepBackgroundFutureProcessDefinitionDataType
    ] = field(
        default=None,
        metadata={
            "name": "Report_Group_Background_Process_Definition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    partitioned_background_process_reference: Optional[PartitionedBackgroundProcessObjectType] = (
        field(
            default=None,
            metadata={
                "name": "Partitioned_Background_Process_Reference",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    to_do_reference: Optional[ToDoObjectType] = field(
        default=None,
        metadata={
            "name": "To_Do_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_service_reference: Optional[EventServiceObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Service_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_background_process_definition_data: Optional[
        IntegrationBackgroundProcessDefinitionDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Background_Process_Definition_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


class GetEventDocuments:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetEventDocumentsInput
    output = GetEventDocumentsOutput


@dataclass
class GetIntegrationEventsOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetIntegrationEventsOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_integration_events_response: Optional[GetIntegrationEventsResponse] = field(
            default=None,
            metadata={
                "name": "Get_Integration_Events_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetIntegrationEventsOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetIntegrationEventsOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class GetIntegrationSystemUsers:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetIntegrationSystemUsersInput
    output = GetIntegrationSystemUsersOutput


class LaunchEib:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = LaunchEibInput
    output = LaunchEibOutput


class LaunchIntegration:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = LaunchIntegrationInput
    output = LaunchIntegrationOutput


@dataclass
class IntegrationTransportProtocolAssignmentDataType:
    """
    Integration Data Communication Data element.

    Attributes:
        integration_transport_protocol_data
        integration_file_utility_data
        integration_payload_data
        restricted_to_environment_reference: Unique identifier for an OMS Environment reference
        preview_only: Configuration will only apply in a Preview tenant
    """

    class Meta:
        name = "Integration_Transport_Protocol_Assignment_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_transport_protocol_data: Optional[IntegrationTransportProtocolDataWwstype] = field(
        default=None,
        metadata={
            "name": "Integration_Transport_Protocol_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_file_utility_data: Optional[IntegrationFileUtilityDataType] = field(
        default=None,
        metadata={
            "name": "Integration_File_Utility_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_payload_data: Optional[IntegrationPayloadDataType] = field(
        default=None,
        metadata={
            "name": "Integration_Payload_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    restricted_to_environment_reference: list[OmsEnvironmentObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Restricted_To_Environment_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    preview_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Preview_Only",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSubscriptionRequestType:
    """
    Put Subscription Request.

    Attributes:
        subscription_reference: Subscription Reference
        subscription_data
        version
    """

    class Meta:
        name = "Put_Subscription_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    subscription_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Subscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_data: Optional[SubscriptionDataType] = field(
        default=None,
        metadata={
            "name": "Subscription_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class SubscriptionType:
    """
    Subscription element.

    Attributes:
        subscription_reference: Subscription Reference
        subscription_data
    """

    class Meta:
        target_namespace = "urn:com.workday/bsvc"

    subscription_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Subscription_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_data: Optional[SubscriptionDataType] = field(
        default=None,
        metadata={
            "name": "Subscription_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class WorkflowStepType:
    """
    A step in a Business Process (Workflow)

    Attributes:
        workflow_step_reference: A reference to the Workflow Step instance
        workflow_step_data
    """

    class Meta:
        name = "Workflow_StepType"
        target_namespace = "urn:com.workday/bsvc"

    workflow_step_reference: Optional[WorkflowStepObjectType] = field(
        default=None,
        metadata={
            "name": "Workflow_Step_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workflow_step_data: list[WorkflowStepContentDataType] = field(
        default_factory=list,
        metadata={
            "name": "Workflow_Step_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


class GetIntegrationEvents:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetIntegrationEventsInput
    output = GetIntegrationEventsOutput


@dataclass
class EventRecordProcessViewWwstype:
    """
    All completed or in progress steps for the event.

    Attributes:
        process_reference: The Process Action Event for this Event Record
        workflow_step: The Workflow Step this Event Record is doing
        status_reference: The Event Record Action that indicates the status of this Event Record
        completed_date: The date on which this Event Record was completed or delayed until
        due_date: The date on which this Event Record is due
        workflow_process_participant_reference: The Workflow Process Participants relevant to this
            Event Record
    """

    class Meta:
        name = "Event_Record_Process_View_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    process_reference: Optional[ActionEventObjectType] = field(
        default=None,
        metadata={
            "name": "Process_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workflow_step: list[WorkflowStepType] = field(
        default_factory=list,
        metadata={
            "name": "Workflow_Step",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    status_reference: Optional[EventRecordActionObjectType] = field(
        default=None,
        metadata={
            "name": "Status_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    completed_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Completed_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    due_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Due_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workflow_process_participant_reference: list[WorkflowProcessParticipantObjectType] = field(
        default_factory=list,
        metadata={
            "name": "Workflow_Process_Participant_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class EventRemainingProcessViewWwstype:
    """
    All remaining steps for the event.

    Attributes:
        event_reference: A reference to this event
        workflow_step
    """

    class Meta:
        name = "Event_Remaining_Process_View_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    event_reference: Optional[EventObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    workflow_step: list[WorkflowStepType] = field(
        default_factory=list,
        metadata={
            "name": "Workflow_Step",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class JobIntegrationDeliveryConfigurationType:
    """
    Contains Information about the configuration of a Job Integration Delivery Configuration, used
    for configuring an EIB delivery step.

    Attributes:
        integration_transport_protocol_assignment_data: Describes how the Job Integration Delivery
            Configuration (Audited) is configured
    """

    class Meta:
        name = "Job_Integration_Delivery_ConfigurationType"
        target_namespace = "urn:com.workday/bsvc"

    integration_transport_protocol_assignment_data: list[
        IntegrationTransportProtocolAssignmentDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Transport_Protocol_Assignment_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSubscriptionRequest(PutSubscriptionRequestType):
    class Meta:
        name = "Put_Subscription_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class SubscriptionResponseDataType:
    """Subscription Response Data element."""

    class Meta:
        name = "Subscription_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    subscription: list[SubscriptionType] = field(
        default_factory=list,
        metadata={
            "name": "Subscription",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutSubscriptionInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutSubscriptionInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutSubscriptionInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_subscription_request: Optional[PutSubscriptionRequest] = field(
            default=None,
            metadata={
                "name": "Put_Subscription_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class EventDetailDataType:
    """
    This element is wrapper for Event data.

    Attributes:
        creation_date: The Event Creation Date
        due_date: The Event Due Date
        completed_date: The Event Completed Date
        event_category_reference: The reference to the Category for the Event.
        event_state_reference: The reference to the State of the Event.
        event_target_reference: The "target" of the Event (e.g. an Employee for Staffing Events, an
            Organization for Reorganization Events, etc...).
        initiating_person_reference: The reference to the Person who initiated the Event.
        awaiting_task_data: This element is a wrapper element for Awaiting Task information.
        sub_event: This element is wrapper for all Sub-Events for this Event. (Recursive)
        process_history_data: Event Records that describe the process history
        remaining_process_data: Events and related Workflow Steps that are remaining
    """

    class Meta:
        name = "Event_Detail_DataType"
        target_namespace = "urn:com.workday/bsvc"

    creation_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Creation_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    due_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "Due_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    completed_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "Completed_Date",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_category_reference: Optional[EventClassificationSubcategoryObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Category_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_state_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Event_State_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    event_target_reference: Optional[EventTargetObjectType] = field(
        default=None,
        metadata={
            "name": "Event_Target_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    initiating_person_reference: Optional[UniqueIdentifierObjectType] = field(
        default=None,
        metadata={
            "name": "Initiating_Person_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    awaiting_task_data: list[AwaitingTaskDataType] = field(
        default_factory=list,
        metadata={
            "name": "Awaiting_Task_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    sub_event: list[EventWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Sub-Event",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    process_history_data: list[EventRecordProcessViewWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Process_History_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    remaining_process_data: list[EventRemainingProcessViewWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Remaining_Process_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetSubscriptionsResponseType:
    """Get Subscriptions Response."""

    class Meta:
        name = "Get_Subscriptions_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[SubscriptionRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[SubscriptionResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class IntegrationServiceDataWwstype:
    """
    Container element for data related to an Integration Service and its use within an Integration
    System.

    Attributes:
        integration_service_reference: Reference element representing an object within the Workday
            system.  The sub-elements and attributes within this element are used to return one and
            only one instance of the identifying object.
        integration_transaction_log_service_data: Integration Transaction Log Service Data
        integration_sequence_generator_service_data: Integration Sequence Generator Service Data
        integration_data_change_service_data: Integration Data Change Service Data
        integration_field_override_service_data: Integration Field Override Service Data
        integration_data_initialization_override_configuration_data
        integration_field_attributes_service_data: Integration Field Attributes Service Data
        integration_delivery_configuration_data: Integration Delivery Configuration Data
        job_integration_delivery_configuration_data
        job_integration_transformation_configuration_data
        integration_retrieval_configuration_data
        job_integration_retrieval_configuration_data
        integration_attachment_service_data
        integration_report_service_configuration_data
        integration_custom_object_configuration_data
        integration_connector_configuration_data
        integration_data_initialization_service_data
        wid: Workday ID of instance of Integration System Service. Note that this value is ignored
            on the inbound request.
        enabled: Boolean attribute representing whether the Integration Service is enabled for the
            Integration System.  Only enabled Integration Services are allowed to have
            values/defaults for Integration Attributes and Maps.
    """

    class Meta:
        name = "Integration_Service_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_service_reference: Optional[IntegrationServiceObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Service_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    integration_transaction_log_service_data: Optional[
        IntegrationTransactionLogConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Transaction_Log_Service_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_sequence_generator_service_data: list[
        IntegrationSequenceGeneratorConfigurationDataType
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Sequence_Generator_Service_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_data_change_service_data: Optional[IntegrationDataChangeConfigurationDataType] = (
        field(
            default=None,
            metadata={
                "name": "Integration_Data_Change_Service_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    integration_field_override_service_data: Optional[
        IntegrationFieldOverrideConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Field_Override_Service_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_data_initialization_override_configuration_data: Optional[
        IntegrationDataInitializationOverrideConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Data_Initialization_Override_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_field_attributes_service_data: Optional[
        IntegrationFieldAttributesConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Field_Attributes_Service_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_delivery_configuration_data: Optional[IntegrationDeliveryConfigurationDataType] = (
        field(
            default=None,
            metadata={
                "name": "Integration_Delivery_Configuration_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    job_integration_delivery_configuration_data: Optional[
        JobIntegrationDeliveryConfigurationType
    ] = field(
        default=None,
        metadata={
            "name": "Job_Integration_Delivery_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    job_integration_transformation_configuration_data: Optional[
        JobIntegrationTransformationConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Job_Integration_Transformation_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_retrieval_configuration_data: Optional[
        IntegrationRetrievalConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Retrieval_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    job_integration_retrieval_configuration_data: Optional[
        JobIntegrationRetrievalConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Job_Integration_Retrieval_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attachment_service_data: Optional[IntegrationAttachmentConfigurationDataType] = (
        field(
            default=None,
            metadata={
                "name": "Integration_Attachment_Service_Data",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    integration_report_service_configuration_data: Optional[
        IntegrationReportServiceConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Report_Service_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_custom_object_configuration_data: Optional[
        IntegrationCustomObjectConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Custom_Object_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_connector_configuration_data: Optional[
        IntegrationConnectorConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Connector_Configuration_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_data_initialization_service_data: Optional[
        IntegrationDataInitializationConfigurationDataType
    ] = field(
        default=None,
        metadata={
            "name": "Integration_Data_Initialization_Service_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    wid: Optional[str] = field(
        default=None,
        metadata={
            "name": "WID",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
            "max_length": 36,
        },
    )
    enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Enabled",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


class PutSubscription:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutSubscriptionInput
    output = PutSubscriptionOutput


@dataclass
class GetSubscriptionsResponse(GetSubscriptionsResponseType):
    class Meta:
        name = "Get_Subscriptions_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class IntegrationSystemDataWwstype:
    """
    Element containing data for an Integration System, including Template reference, Attributes and
    Maps.

    Attributes:
        integration_system_id: Text attribute representing external System ID.
        integration_system_name: Text attribute representing external System Name.
        integration_system_comment: Integration System Comment
        integration_template_reference: Reference element representing a unique Integration
            Template.
        integration_system_user_reference: Integration System User Reference
        integration_tag_data
        integration_repository_document_references
        integration_system_contact
        integration_service_data: Integration Service Data
        integration_attributes_data: Integration Attributes Data
        integration_maps_data: Integration Maps Data
        custom_attribute_data: Custom Attribute Data
        custom_map_data: Custom Map Data
        custom_launch_parameter_data: Custom Launch Parameter Data
        integration_notification_data: Integration Notification Data
        subscription_data: Subscription Data element
        web_service_operation_data: Integration System Data
    """

    class Meta:
        name = "Integration_System_Data_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_System_ID",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_System_Name",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "Integration_System_Comment",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_template_reference: Optional[IntegrationTemplateAbstractObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_Template_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_user_reference: Optional[SystemUserObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_User_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_tag_data: list[IntegrationTagForIntegrationSystemWwsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Tag_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_repository_document_references: list[IntegrationSystemRepositoryDocumentWwstype] = (
        field(
            default_factory=list,
            metadata={
                "name": "Integration_Repository_Document_References",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
    )
    integration_system_contact: list[IntegrationSystemContactDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_System_Contact",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_service_data: list[IntegrationServiceDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Service_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_attributes_data: list[
        IntegrationToolProviderIntegrationAttributeValuesDataWwstype
    ] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Attributes_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_maps_data: list[IntegrationToolProviderIntegrationMapValuesDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Maps_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_attribute_data: list[IntegrationAttributeDataType] = field(
        default_factory=list,
        metadata={
            "name": "Custom_Attribute_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_map_data: list[IntegrationMapDataType] = field(
        default_factory=list,
        metadata={
            "name": "Custom_Map_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    custom_launch_parameter_data: list[LaunchParameterDataType] = field(
        default_factory=list,
        metadata={
            "name": "Custom_Launch_Parameter_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_notification_data: list[IntegrationNotificationDataType] = field(
        default_factory=list,
        metadata={
            "name": "Integration_Notification_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    subscription_data: list[SubscriptionDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Subscription_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    web_service_operation_data: list[WebServiceOperationDataWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Web_Service_Operation_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class GetSubscriptionsOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetSubscriptionsOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_subscriptions_response: Optional[GetSubscriptionsResponse] = field(
            default=None,
            metadata={
                "name": "Get_Subscriptions_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetSubscriptionsOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetSubscriptionsOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


@dataclass
class IntegrationSystemWwstype:
    """
    Encapsulating element containing all Integration System data.

    Attributes:
        integration_system_reference: Unique identifier for an Integration System reference
        integration_system_data
        exceptions_response_data
    """

    class Meta:
        name = "Integration_System_WWSType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_data: Optional[IntegrationSystemDataWwstype] = field(
        default=None,
        metadata={
            "name": "Integration_System_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    exceptions_response_data: list[ApplicationInstanceRelatedExceptionsDataType] = field(
        default_factory=list,
        metadata={
            "name": "Exceptions_Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationSystemRequestType:
    """
    Integration System request element.

    Attributes:
        integration_system_reference: Integration System Reference
        integration_system_data: Integration System Data
        add_only: Add Only
        version
    """

    class Meta:
        name = "Put_Integration_System_RequestType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system_reference: Optional[IntegrationSystemAuditedObjectType] = field(
        default=None,
        metadata={
            "name": "Integration_System_Reference",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    integration_system_data: Optional[IntegrationSystemDataWwstype] = field(
        default=None,
        metadata={
            "name": "Integration_System_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
            "required": True,
        },
    )
    add_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Add_Only",
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


class GetSubscriptions:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetSubscriptionsInput
    output = GetSubscriptionsOutput


@dataclass
class IntegrationSystemResponseDataType:
    """
    Contains each Integration System based on the Request Criteria.

    The data returned is the current information as of the dates in the response filter.
    """

    class Meta:
        name = "Integration_System_Response_DataType"
        target_namespace = "urn:com.workday/bsvc"

    integration_system: list[IntegrationSystemWwstype] = field(
        default_factory=list,
        metadata={
            "name": "Integration_System",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )


@dataclass
class PutIntegrationSystemRequest(PutIntegrationSystemRequestType):
    class Meta:
        name = "Put_Integration_System_Request"
        namespace = "urn:com.workday/bsvc"


@dataclass
class PutIntegrationSystemInput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["PutIntegrationSystemInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["PutIntegrationSystemInput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        put_integration_system_request: Optional[PutIntegrationSystemRequest] = field(
            default=None,
            metadata={
                "name": "Put_Integration_System_Request",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )

    @dataclass
    class Header:
        workday_common_header: Optional[WorkdayCommonHeader] = field(
            default=None,
            metadata={
                "name": "Workday_Common_Header",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )


@dataclass
class GetIntegrationSystemsResponseType:
    """Response element containing instances of Integration System and each of its associated
    data."""

    class Meta:
        name = "Get_Integration_Systems_ResponseType"
        target_namespace = "urn:com.workday/bsvc"

    request_references: Optional[IntegrationSystemRequestReferencesType] = field(
        default=None,
        metadata={
            "name": "Request_References",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    request_criteria: Optional[GetIntegrationSystemsCriteriaType] = field(
        default=None,
        metadata={
            "name": "Request_Criteria",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_filter: Optional[ResponseFilterType] = field(
        default=None,
        metadata={
            "name": "Response_Filter",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_group: Optional[IntegrationSystemResponseGroupType] = field(
        default=None,
        metadata={
            "name": "Response_Group",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_results: Optional[ResponseResultsType] = field(
        default=None,
        metadata={
            "name": "Response_Results",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    response_data: Optional[IntegrationSystemResponseDataType] = field(
        default=None,
        metadata={
            "name": "Response_Data",
            "type": "Element",
            "namespace": "urn:com.workday/bsvc",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "urn:com.workday/bsvc",
        },
    )


class PutIntegrationSystem:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = PutIntegrationSystemInput
    output = PutIntegrationSystemOutput


@dataclass
class GetIntegrationSystemsResponse(GetIntegrationSystemsResponseType):
    class Meta:
        name = "Get_Integration_Systems_Response"
        namespace = "urn:com.workday/bsvc"


@dataclass
class GetIntegrationSystemsOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://schemas.xmlsoap.org/soap/envelope/"
        target_namespace = "urn:com.workday/bsvc/Integrations"

    body: Optional["GetIntegrationSystemsOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_integration_systems_response: Optional[GetIntegrationSystemsResponse] = field(
            default=None,
            metadata={
                "name": "Get_Integration_Systems_Response",
                "type": "Element",
                "namespace": "urn:com.workday/bsvc",
            },
        )
        fault: Optional["GetIntegrationSystemsOutput.Body.Fault"] = field(
            default=None,
            metadata={
                "name": "Fault",
                "type": "Element",
            },
        )

        @dataclass
        class Fault:
            faultcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultstring: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            faultactor: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )
            detail: Optional["GetIntegrationSystemsOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                validation_fault: Optional[ValidationFault] = field(
                    default=None,
                    metadata={
                        "name": "Validation_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                processing_fault: Optional[ProcessingFault] = field(
                    default=None,
                    metadata={
                        "name": "Processing_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )
                authentication_fault: Optional[AuthenticationFault] = field(
                    default=None,
                    metadata={
                        "name": "Authentication_Fault",
                        "type": "Element",
                        "namespace": "urn:com.workday/bsvc",
                    },
                )


class GetIntegrationSystems:
    style = "document"
    location = "Integrations"
    transport = "http://schemas.xmlsoap.org/soap/http"
    input = GetIntegrationSystemsInput
    output = GetIntegrationSystemsOutput
