from dataclasses import dataclass, field
from typing import Optional

from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class AccessDeniedException:
    class Meta:
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class ArrayOfString:
    item: list[str] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class EmailDeliveryOption:
    class Meta:
        name = "EMailDeliveryOption"

    email_bcc: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailBCC",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_body: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailBody",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_cc: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailCC",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_from: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailFrom",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_reply_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailReplyTo",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_server_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailServerName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_subject: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailSubject",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "emailTo",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class FtpdeliveryOption:
    class Meta:
        name = "FTPDeliveryOption"

    ftp_server_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ftpServerName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    ftp_user_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ftpUserName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    ftp_user_password: Optional[str] = field(
        default=None,
        metadata={
            "name": "ftpUserPassword",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    remote_file: Optional[str] = field(
        default=None,
        metadata={
            "name": "remoteFile",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    sftp_option: Optional[bool] = field(
        default=None,
        metadata={
            "name": "sftpOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )


@dataclass
class FaxDeliveryOption:
    fax_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "faxNumber",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    fax_server: Optional[str] = field(
        default=None,
        metadata={
            "name": "faxServer",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class FileDataSource:
    dynamic_data_source_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "dynamicDataSourcePath",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    temporary_data_source: Optional[bool] = field(
        default=None,
        metadata={
            "name": "temporaryDataSource",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )


@dataclass
class InvalidParametersException:
    class Meta:
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class ItemData:
    absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "absolutePath",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    creation_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "creationDate",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    display_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "displayName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "fileName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    last_modified: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "lastModified",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    last_modifier: Optional[str] = field(
        default=None,
        metadata={
            "name": "lastModifier",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    owner: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    parent_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "parentAbsolutePath",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class JdbcdataSource:
    class Meta:
        name = "JDBCDataSource"

    jdbcdriver_class: Optional[str] = field(
        default=None,
        metadata={
            "name": "JDBCDriverClass",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    jdbcdriver_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "JDBCDriverType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    jdbcpassword: Optional[str] = field(
        default=None,
        metadata={
            "name": "JDBCPassword",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    jdbcurl: Optional[str] = field(
        default=None,
        metadata={
            "name": "JDBCURL",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    jdbcuser_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "JDBCUserName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    data_source_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "dataSourceName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class LocalDeliveryOption:
    destination: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class MetaData:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
        },
    )


@dataclass
class OperationFailedException:
    class Meta:
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class PrintDeliveryOption:
    print_number_of_copy: Optional[str] = field(
        default=None,
        metadata={
            "name": "printNumberOfCopy",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    print_orientation: Optional[str] = field(
        default=None,
        metadata={
            "name": "printOrientation",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    print_range: Optional[str] = field(
        default=None,
        metadata={
            "name": "printRange",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    print_side: Optional[str] = field(
        default=None,
        metadata={
            "name": "printSide",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    print_tray: Optional[str] = field(
        default=None,
        metadata={
            "name": "printTray",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    printer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "printerName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class ReportDataChunk:
    report_data_chunk: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "reportDataChunk",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
            "format": "base64",
        },
    )
    report_data_file_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportDataFileID",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_data_offset: Optional[int] = field(
        default=None,
        metadata={
            "name": "reportDataOffset",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )


@dataclass
class SchedulingException:
    class Meta:
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class TemplateFormatLabelValue:
    template_format_label: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateFormatLabel",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    template_format_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateFormatValue",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class WebDavdeliveryOption:
    class Meta:
        name = "WebDAVDeliveryOption"

    delivery_auth_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "deliveryAuthType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    password: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    remote_file_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "remoteFilePath",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    server: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    user_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "userName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class CreateReport:
    class Meta:
        name = "createReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportName",
            "type": "Element",
            "required": True,
        },
    )
    folder_absolute_path_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "folderAbsolutePathURL",
            "type": "Element",
            "required": True,
        },
    )
    template_file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateFileName",
            "type": "Element",
            "required": True,
        },
    )
    template_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "templateData",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )
    xlifffile_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "XLIFFFileName",
            "type": "Element",
            "required": True,
        },
    )
    xliffdata: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "XLIFFData",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )
    update_flag: Optional[bool] = field(
        default=None,
        metadata={
            "name": "updateFlag",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class CreateReportFolder:
    class Meta:
        name = "createReportFolder"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    folder_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "folderAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class CreateReportFolderResponse:
    class Meta:
        name = "createReportFolderResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    create_report_folder_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "createReportFolderReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class CreateReportResponse:
    class Meta:
        name = "createReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    create_report_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "createReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DeleteFolder:
    class Meta:
        name = "deleteFolder"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    folder_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "folderAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DeleteFolderResponse:
    class Meta:
        name = "deleteFolderResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    delete_folder_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "deleteFolderReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DeleteReport:
    class Meta:
        name = "deleteReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DeleteReportResponse:
    class Meta:
        name = "deleteReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    delete_report_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "deleteReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DeliveryServiceResponse:
    class Meta:
        name = "deliveryServiceResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    delivery_service_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "deliveryServiceReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DownloadReportDataChunk:
    class Meta:
        name = "downloadReportDataChunk"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    file_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "fileID",
            "type": "Element",
            "required": True,
        },
    )
    begin_idx: Optional[int] = field(
        default=None,
        metadata={
            "name": "beginIdx",
            "type": "Element",
            "required": True,
        },
    )
    size: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DownloadReportObject:
    class Meta:
        name = "downloadReportObject"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class DownloadReportObjectResponse:
    class Meta:
        name = "downloadReportObjectResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    download_report_object_return: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "downloadReportObjectReturn",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class GetBiphttpsessionInterval:
    class Meta:
        name = "getBIPHTTPSessionInterval"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class GetBiphttpsessionIntervalResponse:
    class Meta:
        name = "getBIPHTTPSessionIntervalResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_biphttpsession_interval_return: Optional[int] = field(
        default=None,
        metadata={
            "name": "getBIPHTTPSessionIntervalReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetDeliveryServiceDefinition:
    class Meta:
        name = "getDeliveryServiceDefinition"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class GetFolderContents:
    class Meta:
        name = "getFolderContents"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    folder_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "folderAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetReportDefinition:
    class Meta:
        name = "getReportDefinition"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetReportSampleData:
    class Meta:
        name = "getReportSampleData"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetReportSampleDataResponse:
    class Meta:
        name = "getReportSampleDataResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_report_sample_data_return: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "getReportSampleDataReturn",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class GetSecurityModel:
    class Meta:
        name = "getSecurityModel"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class GetSecurityModelResponse:
    class Meta:
        name = "getSecurityModelResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_security_model_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "getSecurityModelReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetTemplate:
    class Meta:
        name = "getTemplate"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )
    template_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateID",
            "type": "Element",
            "required": True,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetTemplateParameters:
    class Meta:
        name = "getTemplateParameters"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )
    template_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateID",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetTemplateResponse:
    class Meta:
        name = "getTemplateResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_template_return: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "getTemplateReturn",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class GetXdoschema:
    class Meta:
        name = "getXDOSchema"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetXdoschemaResponse:
    class Meta:
        name = "getXDOSchemaResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_xdoschema_return: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "getXDOSchemaReturn",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class HasReportAccess:
    class Meta:
        name = "hasReportAccess"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class HasReportAccessResponse:
    class Meta:
        name = "hasReportAccessResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    has_report_access_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasReportAccessReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class IsFolderExist:
    class Meta:
        name = "isFolderExist"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    folder_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "folderAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class IsFolderExistResponse:
    class Meta:
        name = "isFolderExistResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    is_folder_exist_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isFolderExistReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class IsReportExist:
    class Meta:
        name = "isReportExist"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class IsReportExistResponse:
    class Meta:
        name = "isReportExistResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    is_report_exist_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "isReportExistReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class RemoveTemplateForReport:
    class Meta:
        name = "removeTemplateForReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )
    template_file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateFileName",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class RemoveTemplateForReportResponse:
    class Meta:
        name = "removeTemplateForReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    remove_template_for_report_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "removeTemplateForReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SubmitReport:
    class Meta:
        name = "submitReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    submit_report_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "submitReportData",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )
    app_params: Optional[str] = field(
        default=None,
        metadata={
            "name": "appParams",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class SubmitReportResponse:
    class Meta:
        name = "submitReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    submit_report_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "submitReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UpdateReportDefinitionResponse:
    class Meta:
        name = "updateReportDefinitionResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    update_report_definition_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "updateReportDefinitionReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UpdateTemplateForReport:
    class Meta:
        name = "updateTemplateForReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )
    template_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateName",
            "type": "Element",
            "required": True,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    template_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "templateData",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class UpdateTemplateForReportResponse:
    class Meta:
        name = "updateTemplateForReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    update_template_for_report_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "updateTemplateForReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UploadReportDataChunk:
    class Meta:
        name = "uploadReportDataChunk"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    file_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "fileID",
            "type": "Element",
            "required": True,
        },
    )
    report_data_chunk: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "reportDataChunk",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )
    report_raw_data_chunk: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportRawDataChunk",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UploadReportDataChunkResponse:
    class Meta:
        name = "uploadReportDataChunkResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    upload_report_data_chunk_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "uploadReportDataChunkReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UploadReportObject:
    class Meta:
        name = "uploadReportObject"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_object_absolute_path_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportObjectAbsolutePathURL",
            "type": "Element",
            "required": True,
        },
    )
    object_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "objectType",
            "type": "Element",
            "required": True,
        },
    )
    object_zipped_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "objectZippedData",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class UploadReportObjectResponse:
    class Meta:
        name = "uploadReportObjectResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    upload_report_object_return: Optional[str] = field(
        default=None,
        metadata={
            "name": "uploadReportObjectReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UploadTemplateForReport:
    class Meta:
        name = "uploadTemplateForReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "required": True,
        },
    )
    template_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateName",
            "type": "Element",
            "required": True,
        },
    )
    template_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateType",
            "type": "Element",
            "required": True,
        },
    )
    locale: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    template_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "templateData",
            "type": "Element",
            "required": True,
            "format": "base64",
        },
    )


@dataclass
class UploadTemplateForReportResponse:
    class Meta:
        name = "uploadTemplateForReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    upload_template_for_report_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "uploadTemplateForReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ValidateLogin:
    class Meta:
        name = "validateLogin"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"


@dataclass
class ValidateLoginResponse:
    class Meta:
        name = "validateLoginResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    validate_login_return: Optional[bool] = field(
        default=None,
        metadata={
            "name": "validateLoginReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ArrayOfItemData:
    item: list[ItemData] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class ArrayOfTemplateFormatLabelValue:
    item: list[TemplateFormatLabelValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class BipdataSource:
    class Meta:
        name = "BIPDataSource"

    jdbcdata_source: Optional[JdbcdataSource] = field(
        default=None,
        metadata={
            "name": "JDBCDataSource",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    file_data_source: Optional[FileDataSource] = field(
        default=None,
        metadata={
            "name": "fileDataSource",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class DeliveryServiceDefinition:
    email_server_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "EMailServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    ftpserver_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "FTPServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    httpserver_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "HTTPServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    sftpserver_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "SFTPServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    default_server_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "defaultServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    fax_server_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "faxServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    printer_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "printerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    web_davserver_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "webDAVServerNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class ExternalReportWssserviceCreateReportFolderInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceCreateReportFolderInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceCreateReportFolderInput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        create_report_folder: Optional[CreateReportFolder] = field(
            default=None,
            metadata={
                "name": "createReportFolder",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        create_report_folder: Optional[CreateReportFolder] = field(
            default=None,
            metadata={
                "name": "createReportFolder",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceCreateReportFolderOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceCreateReportFolderOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceCreateReportFolderOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        create_report_folder_response: Optional[CreateReportFolderResponse] = field(
            default=None,
            metadata={
                "name": "createReportFolderResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceCreateReportFolderOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceCreateReportFolderOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        create_report_folder_response: Optional[CreateReportFolderResponse] = field(
            default=None,
            metadata={
                "name": "createReportFolderResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceCreateReportInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceCreateReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceCreateReportInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        create_report: Optional[CreateReport] = field(
            default=None,
            metadata={
                "name": "createReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        create_report: Optional[CreateReport] = field(
            default=None,
            metadata={
                "name": "createReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceCreateReportOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceCreateReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceCreateReportOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        create_report_response: Optional[CreateReportResponse] = field(
            default=None,
            metadata={
                "name": "createReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceCreateReportOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceCreateReportOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        create_report_response: Optional[CreateReportResponse] = field(
            default=None,
            metadata={
                "name": "createReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDeleteFolderInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDeleteFolderInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceDeleteFolderInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        delete_folder: Optional[DeleteFolder] = field(
            default=None,
            metadata={
                "name": "deleteFolder",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        delete_folder: Optional[DeleteFolder] = field(
            default=None,
            metadata={
                "name": "deleteFolder",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDeleteFolderOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDeleteFolderOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceDeleteFolderOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        delete_folder_response: Optional[DeleteFolderResponse] = field(
            default=None,
            metadata={
                "name": "deleteFolderResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceDeleteFolderOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceDeleteFolderOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        delete_folder_response: Optional[DeleteFolderResponse] = field(
            default=None,
            metadata={
                "name": "deleteFolderResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDeleteReportInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDeleteReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceDeleteReportInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        delete_report: Optional[DeleteReport] = field(
            default=None,
            metadata={
                "name": "deleteReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        delete_report: Optional[DeleteReport] = field(
            default=None,
            metadata={
                "name": "deleteReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDeleteReportOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDeleteReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceDeleteReportOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        delete_report_response: Optional[DeleteReportResponse] = field(
            default=None,
            metadata={
                "name": "deleteReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceDeleteReportOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceDeleteReportOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        delete_report_response: Optional[DeleteReportResponse] = field(
            default=None,
            metadata={
                "name": "deleteReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDeliveryServiceOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDeliveryServiceOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceDeliveryServiceOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        delivery_service_response: Optional[DeliveryServiceResponse] = field(
            default=None,
            metadata={
                "name": "deliveryServiceResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceDeliveryServiceOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceDeliveryServiceOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        delivery_service_response: Optional[DeliveryServiceResponse] = field(
            default=None,
            metadata={
                "name": "deliveryServiceResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDownloadReportDataChunkInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDownloadReportDataChunkInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceDownloadReportDataChunkInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        download_report_data_chunk: Optional[DownloadReportDataChunk] = field(
            default=None,
            metadata={
                "name": "downloadReportDataChunk",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        download_report_data_chunk: Optional[DownloadReportDataChunk] = field(
            default=None,
            metadata={
                "name": "downloadReportDataChunk",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDownloadReportObjectInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDownloadReportObjectInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceDownloadReportObjectInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        download_report_object: Optional[DownloadReportObject] = field(
            default=None,
            metadata={
                "name": "downloadReportObject",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        download_report_object: Optional[DownloadReportObject] = field(
            default=None,
            metadata={
                "name": "downloadReportObject",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceDownloadReportObjectOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDownloadReportObjectOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceDownloadReportObjectOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        download_report_object_response: Optional[DownloadReportObjectResponse] = field(
            default=None,
            metadata={
                "name": "downloadReportObjectResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceDownloadReportObjectOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceDownloadReportObjectOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        download_report_object_response: Optional[DownloadReportObjectResponse] = field(
            default=None,
            metadata={
                "name": "downloadReportObjectResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetBiphttpsessionIntervalInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetBiphttpsessionIntervalInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetBiphttpsessionIntervalInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_biphttpsession_interval: Optional[GetBiphttpsessionInterval] = field(
            default=None,
            metadata={
                "name": "getBIPHTTPSessionInterval",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_biphttpsession_interval: Optional[GetBiphttpsessionInterval] = field(
            default=None,
            metadata={
                "name": "getBIPHTTPSessionInterval",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetBiphttpsessionIntervalOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetBiphttpsessionIntervalOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetBiphttpsessionIntervalOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_biphttpsession_interval_response: Optional[GetBiphttpsessionIntervalResponse] = field(
            default=None,
            metadata={
                "name": "getBIPHTTPSessionIntervalResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetBiphttpsessionIntervalOutput.Body.Fault"] = (
            field(
                default=None,
                metadata={
                    "name": "Fault",
                    "type": "Element",
                },
            )
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
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Policyreference:
        get_biphttpsession_interval_response: Optional[GetBiphttpsessionIntervalResponse] = field(
            default=None,
            metadata={
                "name": "getBIPHTTPSessionIntervalResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetDeliveryServiceDefinitionInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetDeliveryServiceDefinitionInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetDeliveryServiceDefinitionInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_delivery_service_definition: Optional[GetDeliveryServiceDefinition] = field(
            default=None,
            metadata={
                "name": "getDeliveryServiceDefinition",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_delivery_service_definition: Optional[GetDeliveryServiceDefinition] = field(
            default=None,
            metadata={
                "name": "getDeliveryServiceDefinition",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetFolderContentsInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetFolderContentsInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetFolderContentsInput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        get_folder_contents: Optional[GetFolderContents] = field(
            default=None,
            metadata={
                "name": "getFolderContents",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_folder_contents: Optional[GetFolderContents] = field(
            default=None,
            metadata={
                "name": "getFolderContents",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetReportDefinitionInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetReportDefinitionInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetReportDefinitionInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_report_definition: Optional[GetReportDefinition] = field(
            default=None,
            metadata={
                "name": "getReportDefinition",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_report_definition: Optional[GetReportDefinition] = field(
            default=None,
            metadata={
                "name": "getReportDefinition",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetReportSampleDataInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetReportSampleDataInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetReportSampleDataInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_report_sample_data: Optional[GetReportSampleData] = field(
            default=None,
            metadata={
                "name": "getReportSampleData",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_report_sample_data: Optional[GetReportSampleData] = field(
            default=None,
            metadata={
                "name": "getReportSampleData",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetReportSampleDataOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetReportSampleDataOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetReportSampleDataOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_report_sample_data_response: Optional[GetReportSampleDataResponse] = field(
            default=None,
            metadata={
                "name": "getReportSampleDataResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetReportSampleDataOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceGetReportSampleDataOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_report_sample_data_response: Optional[GetReportSampleDataResponse] = field(
            default=None,
            metadata={
                "name": "getReportSampleDataResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetSecurityModelInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetSecurityModelInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetSecurityModelInput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        get_security_model: Optional[GetSecurityModel] = field(
            default=None,
            metadata={
                "name": "getSecurityModel",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_security_model: Optional[GetSecurityModel] = field(
            default=None,
            metadata={
                "name": "getSecurityModel",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetSecurityModelOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetSecurityModelOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetSecurityModelOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        get_security_model_response: Optional[GetSecurityModelResponse] = field(
            default=None,
            metadata={
                "name": "getSecurityModelResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetSecurityModelOutput.Body.Fault"] = field(
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
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Policyreference:
        get_security_model_response: Optional[GetSecurityModelResponse] = field(
            default=None,
            metadata={
                "name": "getSecurityModelResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetTemplateParametersInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetTemplateParametersInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetTemplateParametersInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_template_parameters: Optional[GetTemplateParameters] = field(
            default=None,
            metadata={
                "name": "getTemplateParameters",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_template_parameters: Optional[GetTemplateParameters] = field(
            default=None,
            metadata={
                "name": "getTemplateParameters",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetTemplateInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetTemplateInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetTemplateInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_template: Optional[GetTemplate] = field(
            default=None,
            metadata={
                "name": "getTemplate",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_template: Optional[GetTemplate] = field(
            default=None,
            metadata={
                "name": "getTemplate",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetTemplateOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetTemplateOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetTemplateOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_template_response: Optional[GetTemplateResponse] = field(
            default=None,
            metadata={
                "name": "getTemplateResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetTemplateOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceGetTemplateOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_template_response: Optional[GetTemplateResponse] = field(
            default=None,
            metadata={
                "name": "getTemplateResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetXdoschemaInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetXdoschemaInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetXdoschemaInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_xdoschema: Optional[GetXdoschema] = field(
            default=None,
            metadata={
                "name": "getXDOSchema",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_xdoschema: Optional[GetXdoschema] = field(
            default=None,
            metadata={
                "name": "getXDOSchema",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetXdoschemaOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetXdoschemaOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetXdoschemaOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_xdoschema_response: Optional[GetXdoschemaResponse] = field(
            default=None,
            metadata={
                "name": "getXDOSchemaResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetXdoschemaOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceGetXdoschemaOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_xdoschema_response: Optional[GetXdoschemaResponse] = field(
            default=None,
            metadata={
                "name": "getXDOSchemaResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceHasReportAccessInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceHasReportAccessInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceHasReportAccessInput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        has_report_access: Optional[HasReportAccess] = field(
            default=None,
            metadata={
                "name": "hasReportAccess",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        has_report_access: Optional[HasReportAccess] = field(
            default=None,
            metadata={
                "name": "hasReportAccess",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceHasReportAccessOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceHasReportAccessOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceHasReportAccessOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        has_report_access_response: Optional[HasReportAccessResponse] = field(
            default=None,
            metadata={
                "name": "hasReportAccessResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceHasReportAccessOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceHasReportAccessOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        has_report_access_response: Optional[HasReportAccessResponse] = field(
            default=None,
            metadata={
                "name": "hasReportAccessResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceIsFolderExistInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceIsFolderExistInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceIsFolderExistInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        is_folder_exist: Optional[IsFolderExist] = field(
            default=None,
            metadata={
                "name": "isFolderExist",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        is_folder_exist: Optional[IsFolderExist] = field(
            default=None,
            metadata={
                "name": "isFolderExist",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceIsFolderExistOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceIsFolderExistOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceIsFolderExistOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        is_folder_exist_response: Optional[IsFolderExistResponse] = field(
            default=None,
            metadata={
                "name": "isFolderExistResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceIsFolderExistOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceIsFolderExistOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        is_folder_exist_response: Optional[IsFolderExistResponse] = field(
            default=None,
            metadata={
                "name": "isFolderExistResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceIsReportExistInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceIsReportExistInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceIsReportExistInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        is_report_exist: Optional[IsReportExist] = field(
            default=None,
            metadata={
                "name": "isReportExist",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        is_report_exist: Optional[IsReportExist] = field(
            default=None,
            metadata={
                "name": "isReportExist",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceIsReportExistOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceIsReportExistOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceIsReportExistOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        is_report_exist_response: Optional[IsReportExistResponse] = field(
            default=None,
            metadata={
                "name": "isReportExistResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceIsReportExistOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceIsReportExistOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        is_report_exist_response: Optional[IsReportExistResponse] = field(
            default=None,
            metadata={
                "name": "isReportExistResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceRemoveTemplateForReportInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceRemoveTemplateForReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceRemoveTemplateForReportInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        remove_template_for_report: Optional[RemoveTemplateForReport] = field(
            default=None,
            metadata={
                "name": "removeTemplateForReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        remove_template_for_report: Optional[RemoveTemplateForReport] = field(
            default=None,
            metadata={
                "name": "removeTemplateForReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceRemoveTemplateForReportOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceRemoveTemplateForReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceRemoveTemplateForReportOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        remove_template_for_report_response: Optional[RemoveTemplateForReportResponse] = field(
            default=None,
            metadata={
                "name": "removeTemplateForReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceRemoveTemplateForReportOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceRemoveTemplateForReportOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        remove_template_for_report_response: Optional[RemoveTemplateForReportResponse] = field(
            default=None,
            metadata={
                "name": "removeTemplateForReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceSubmitReportInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceSubmitReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceSubmitReportInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        submit_report: Optional[SubmitReport] = field(
            default=None,
            metadata={
                "name": "submitReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        submit_report: Optional[SubmitReport] = field(
            default=None,
            metadata={
                "name": "submitReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceSubmitReportOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceSubmitReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceSubmitReportOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        submit_report_response: Optional[SubmitReportResponse] = field(
            default=None,
            metadata={
                "name": "submitReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceSubmitReportOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceSubmitReportOutput.Body.Fault.Detail"] = (
                field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "namespace": "",
                    },
                )
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                scheduling_exception: Optional[SchedulingException] = field(
                    default=None,
                    metadata={
                        "name": "SchedulingException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        submit_report_response: Optional[SubmitReportResponse] = field(
            default=None,
            metadata={
                "name": "submitReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUpdateReportDefinitionOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUpdateReportDefinitionOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUpdateReportDefinitionOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        update_report_definition_response: Optional[UpdateReportDefinitionResponse] = field(
            default=None,
            metadata={
                "name": "updateReportDefinitionResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceUpdateReportDefinitionOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceUpdateReportDefinitionOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        update_report_definition_response: Optional[UpdateReportDefinitionResponse] = field(
            default=None,
            metadata={
                "name": "updateReportDefinitionResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUpdateTemplateForReportInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUpdateTemplateForReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUpdateTemplateForReportInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        update_template_for_report: Optional[UpdateTemplateForReport] = field(
            default=None,
            metadata={
                "name": "updateTemplateForReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        update_template_for_report: Optional[UpdateTemplateForReport] = field(
            default=None,
            metadata={
                "name": "updateTemplateForReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUpdateTemplateForReportOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUpdateTemplateForReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUpdateTemplateForReportOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        update_template_for_report_response: Optional[UpdateTemplateForReportResponse] = field(
            default=None,
            metadata={
                "name": "updateTemplateForReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceUpdateTemplateForReportOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceUpdateTemplateForReportOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        update_template_for_report_response: Optional[UpdateTemplateForReportResponse] = field(
            default=None,
            metadata={
                "name": "updateTemplateForReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUploadReportDataChunkInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUploadReportDataChunkInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUploadReportDataChunkInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        upload_report_data_chunk: Optional[UploadReportDataChunk] = field(
            default=None,
            metadata={
                "name": "uploadReportDataChunk",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        upload_report_data_chunk: Optional[UploadReportDataChunk] = field(
            default=None,
            metadata={
                "name": "uploadReportDataChunk",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUploadReportDataChunkOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUploadReportDataChunkOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUploadReportDataChunkOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        upload_report_data_chunk_response: Optional[UploadReportDataChunkResponse] = field(
            default=None,
            metadata={
                "name": "uploadReportDataChunkResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceUploadReportDataChunkOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceUploadReportDataChunkOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        upload_report_data_chunk_response: Optional[UploadReportDataChunkResponse] = field(
            default=None,
            metadata={
                "name": "uploadReportDataChunkResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUploadReportObjectInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUploadReportObjectInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceUploadReportObjectInput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        upload_report_object: Optional[UploadReportObject] = field(
            default=None,
            metadata={
                "name": "uploadReportObject",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        upload_report_object: Optional[UploadReportObject] = field(
            default=None,
            metadata={
                "name": "uploadReportObject",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUploadReportObjectOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUploadReportObjectOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUploadReportObjectOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        upload_report_object_response: Optional[UploadReportObjectResponse] = field(
            default=None,
            metadata={
                "name": "uploadReportObjectResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceUploadReportObjectOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceUploadReportObjectOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        upload_report_object_response: Optional[UploadReportObjectResponse] = field(
            default=None,
            metadata={
                "name": "uploadReportObjectResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUploadTemplateForReportInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUploadTemplateForReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUploadTemplateForReportInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        upload_template_for_report: Optional[UploadTemplateForReport] = field(
            default=None,
            metadata={
                "name": "uploadTemplateForReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        upload_template_for_report: Optional[UploadTemplateForReport] = field(
            default=None,
            metadata={
                "name": "uploadTemplateForReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceUploadTemplateForReportOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUploadTemplateForReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUploadTemplateForReportOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        upload_template_for_report_response: Optional[UploadTemplateForReportResponse] = field(
            default=None,
            metadata={
                "name": "uploadTemplateForReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceUploadTemplateForReportOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceUploadTemplateForReportOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        upload_template_for_report_response: Optional[UploadTemplateForReportResponse] = field(
            default=None,
            metadata={
                "name": "uploadTemplateForReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceValidateLoginInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceValidateLoginInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceValidateLoginInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        validate_login: Optional[ValidateLogin] = field(
            default=None,
            metadata={
                "name": "validateLogin",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        validate_login: Optional[ValidateLogin] = field(
            default=None,
            metadata={
                "name": "validateLogin",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceValidateLoginOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceValidateLoginOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceValidateLoginOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        validate_login_response: Optional[ValidateLoginResponse] = field(
            default=None,
            metadata={
                "name": "validateLoginResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceValidateLoginOutput.Body.Fault"] = field(
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
            detail: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

    @dataclass
    class Policyreference:
        validate_login_response: Optional[ValidateLoginResponse] = field(
            default=None,
            metadata={
                "name": "validateLoginResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class MetaDataList:
    meta_data_list: list[MetaData] = field(
        default_factory=list,
        metadata={
            "name": "metaDataList",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class ParamNameValue:
    uitype: Optional[str] = field(
        default=None,
        metadata={
            "name": "UIType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    data_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "dataType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    date_format_string: Optional[str] = field(
        default=None,
        metadata={
            "name": "dateFormatString",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    date_from: Optional[str] = field(
        default=None,
        metadata={
            "name": "dateFrom",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    date_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "dateTo",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    default_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "defaultValue",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    field_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "fieldSize",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    lov_labels: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "lovLabels",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    multi_values_allowed: Optional[bool] = field(
        default=None,
        metadata={
            "name": "multiValuesAllowed",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    refresh_param_on_change: Optional[bool] = field(
        default=None,
        metadata={
            "name": "refreshParamOnChange",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    select_all: Optional[bool] = field(
        default=None,
        metadata={
            "name": "selectAll",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    template_param: Optional[bool] = field(
        default=None,
        metadata={
            "name": "templateParam",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    use_null_for_all: Optional[bool] = field(
        default=None,
        metadata={
            "name": "useNullForAll",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    values: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class DownloadReportDataChunkResponse:
    class Meta:
        name = "downloadReportDataChunkResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    download_report_data_chunk_return: Optional[ReportDataChunk] = field(
        default=None,
        metadata={
            "name": "downloadReportDataChunkReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ArrayOfParamNameValue:
    item: list[ParamNameValue] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class CatalogContents:
    catalog_contents: Optional[ArrayOfItemData] = field(
        default=None,
        metadata={
            "name": "catalogContents",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class DeliveryRequest:
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    document_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "documentData",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
            "format": "base64",
        },
    )
    dynamic_data_source: Optional[BipdataSource] = field(
        default=None,
        metadata={
            "name": "dynamicDataSource",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    email_option: Optional[EmailDeliveryOption] = field(
        default=None,
        metadata={
            "name": "emailOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    fax_option: Optional[FaxDeliveryOption] = field(
        default=None,
        metadata={
            "name": "faxOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    ftp_option: Optional[FtpdeliveryOption] = field(
        default=None,
        metadata={
            "name": "ftpOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    local_option: Optional[LocalDeliveryOption] = field(
        default=None,
        metadata={
            "name": "localOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    print_option: Optional[PrintDeliveryOption] = field(
        default=None,
        metadata={
            "name": "printOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    web_davoption: Optional[WebDavdeliveryOption] = field(
        default=None,
        metadata={
            "name": "webDAVOption",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


class ExternalReportWssserviceCreateReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceCreateReportInput
    output = ExternalReportWssserviceCreateReportOutput


class ExternalReportWssserviceCreateReportFolder:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceCreateReportFolderInput
    output = ExternalReportWssserviceCreateReportFolderOutput


class ExternalReportWssserviceDeleteFolder:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceDeleteFolderInput
    output = ExternalReportWssserviceDeleteFolderOutput


class ExternalReportWssserviceDeleteReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceDeleteReportInput
    output = ExternalReportWssserviceDeleteReportOutput


@dataclass
class ExternalReportWssserviceDownloadReportDataChunkOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDownloadReportDataChunkOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceDownloadReportDataChunkOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        download_report_data_chunk_response: Optional[DownloadReportDataChunkResponse] = field(
            default=None,
            metadata={
                "name": "downloadReportDataChunkResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceDownloadReportDataChunkOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceDownloadReportDataChunkOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        download_report_data_chunk_response: Optional[DownloadReportDataChunkResponse] = field(
            default=None,
            metadata={
                "name": "downloadReportDataChunkResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


class ExternalReportWssserviceDownloadReportObject:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceDownloadReportObjectInput
    output = ExternalReportWssserviceDownloadReportObjectOutput


class ExternalReportWssserviceGetBiphttpsessionInterval:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetBiphttpsessionIntervalInput
    output = ExternalReportWssserviceGetBiphttpsessionIntervalOutput


class ExternalReportWssserviceGetReportSampleData:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetReportSampleDataInput
    output = ExternalReportWssserviceGetReportSampleDataOutput


class ExternalReportWssserviceGetSecurityModel:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetSecurityModelInput
    output = ExternalReportWssserviceGetSecurityModelOutput


class ExternalReportWssserviceGetTemplate:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetTemplateInput
    output = ExternalReportWssserviceGetTemplateOutput


class ExternalReportWssserviceGetXdoschema:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetXdoschemaInput
    output = ExternalReportWssserviceGetXdoschemaOutput


class ExternalReportWssserviceHasReportAccess:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceHasReportAccessInput
    output = ExternalReportWssserviceHasReportAccessOutput


class ExternalReportWssserviceIsFolderExist:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceIsFolderExistInput
    output = ExternalReportWssserviceIsFolderExistOutput


class ExternalReportWssserviceIsReportExist:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceIsReportExistInput
    output = ExternalReportWssserviceIsReportExistOutput


class ExternalReportWssserviceRemoveTemplateForReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceRemoveTemplateForReportInput
    output = ExternalReportWssserviceRemoveTemplateForReportOutput


class ExternalReportWssserviceSubmitReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceSubmitReportInput
    output = ExternalReportWssserviceSubmitReportOutput


class ExternalReportWssserviceUpdateTemplateForReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceUpdateTemplateForReportInput
    output = ExternalReportWssserviceUpdateTemplateForReportOutput


class ExternalReportWssserviceUploadReportDataChunk:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceUploadReportDataChunkInput
    output = ExternalReportWssserviceUploadReportDataChunkOutput


class ExternalReportWssserviceUploadReportObject:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceUploadReportObjectInput
    output = ExternalReportWssserviceUploadReportObjectOutput


class ExternalReportWssserviceUploadTemplateForReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceUploadTemplateForReportInput
    output = ExternalReportWssserviceUploadTemplateForReportOutput


class ExternalReportWssserviceValidateLogin:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceValidateLoginInput
    output = ExternalReportWssserviceValidateLoginOutput


@dataclass
class ReportResponse:
    report_bytes: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportBytes",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
            "format": "base64",
        },
    )
    report_content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportContentType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_file_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportFileID",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_locale: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportLocale",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    meta_data_list: Optional[MetaDataList] = field(
        default=None,
        metadata={
            "name": "metaDataList",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class TemplateFormatsLabelValues:
    list_of_template_format_label_value: Optional[ArrayOfTemplateFormatLabelValue] = field(
        default=None,
        metadata={
            "name": "listOfTemplateFormatLabelValue",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    template_available_locales: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "templateAvailableLocales",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    template_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateID",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    template_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    template_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "templateURL",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class GetDeliveryServiceDefinitionResponse:
    class Meta:
        name = "getDeliveryServiceDefinitionResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_delivery_service_definition_return: Optional[DeliveryServiceDefinition] = field(
        default=None,
        metadata={
            "name": "getDeliveryServiceDefinitionReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetTemplateParametersResponse:
    class Meta:
        name = "getTemplateParametersResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_template_parameters_return: list[ParamNameValue] = field(
        default_factory=list,
        metadata={
            "name": "getTemplateParametersReturn",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class ArrayOfTemplateFormatsLabelValues:
    item: list[TemplateFormatsLabelValues] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


class ExternalReportWssserviceDownloadReportDataChunk:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceDownloadReportDataChunkInput
    output = ExternalReportWssserviceDownloadReportDataChunkOutput


@dataclass
class ExternalReportWssserviceGetDeliveryServiceDefinitionOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetDeliveryServiceDefinitionOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetDeliveryServiceDefinitionOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_delivery_service_definition_response: Optional[GetDeliveryServiceDefinitionResponse] = (
            field(
                default=None,
                metadata={
                    "name": "getDeliveryServiceDefinitionResponse",
                    "type": "Element",
                    "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                },
            )
        )
        fault: Optional["ExternalReportWssserviceGetDeliveryServiceDefinitionOutput.Body.Fault"] = (
            field(
                default=None,
                metadata={
                    "name": "Fault",
                    "type": "Element",
                },
            )
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
            detail: Optional[
                "ExternalReportWssserviceGetDeliveryServiceDefinitionOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_delivery_service_definition_response: Optional[GetDeliveryServiceDefinitionResponse] = (
            field(
                default=None,
                metadata={
                    "name": "getDeliveryServiceDefinitionResponse",
                    "type": "Element",
                    "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                },
            )
        )


@dataclass
class ExternalReportWssserviceGetTemplateParametersOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetTemplateParametersOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetTemplateParametersOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_template_parameters_response: Optional[GetTemplateParametersResponse] = field(
            default=None,
            metadata={
                "name": "getTemplateParametersResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetTemplateParametersOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceGetTemplateParametersOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_template_parameters_response: Optional[GetTemplateParametersResponse] = field(
            default=None,
            metadata={
                "name": "getTemplateParametersResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ParamNameValues:
    list_of_param_name_values: Optional[ArrayOfParamNameValue] = field(
        default=None,
        metadata={
            "name": "listOfParamNameValues",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class ReportRequest:
    xdoproperty_list: Optional[MetaDataList] = field(
        default=None,
        metadata={
            "name": "XDOPropertyList",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    attribute_calendar: Optional[str] = field(
        default=None,
        metadata={
            "name": "attributeCalendar",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    attribute_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "attributeFormat",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    attribute_locale: Optional[str] = field(
        default=None,
        metadata={
            "name": "attributeLocale",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    attribute_template: Optional[str] = field(
        default=None,
        metadata={
            "name": "attributeTemplate",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    attribute_timezone: Optional[str] = field(
        default=None,
        metadata={
            "name": "attributeTimezone",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    attribute_uilocale: Optional[str] = field(
        default=None,
        metadata={
            "name": "attributeUILocale",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    by_pass_cache: Optional[bool] = field(
        default=None,
        metadata={
            "name": "byPassCache",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    dynamic_data_source: Optional[BipdataSource] = field(
        default=None,
        metadata={
            "name": "dynamicDataSource",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    flatten_xml: Optional[bool] = field(
        default=None,
        metadata={
            "name": "flattenXML",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    parameter_name_values: Optional[ArrayOfParamNameValue] = field(
        default=None,
        metadata={
            "name": "parameterNameValues",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_absolute_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsolutePath",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "reportData",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
            "format": "base64",
        },
    )
    report_output_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportOutputPath",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_raw_data: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportRawData",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    size_of_data_chunk_download: Optional[int] = field(
        default=None,
        metadata={
            "name": "sizeOfDataChunkDownload",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )


@dataclass
class DeliveryService:
    class Meta:
        name = "deliveryService"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    delivery_request: Optional[DeliveryRequest] = field(
        default=None,
        metadata={
            "name": "deliveryRequest",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetFolderContentsResponse:
    class Meta:
        name = "getFolderContentsResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_folder_contents_return: Optional[CatalogContents] = field(
        default=None,
        metadata={
            "name": "getFolderContentsReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class RunReportResponse:
    class Meta:
        name = "runReportResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    run_report_return: Optional[ReportResponse] = field(
        default=None,
        metadata={
            "name": "runReportReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ExternalReportWssserviceDeliveryServiceInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceDeliveryServiceInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceDeliveryServiceInput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        delivery_service: Optional[DeliveryService] = field(
            default=None,
            metadata={
                "name": "deliveryService",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        delivery_service: Optional[DeliveryService] = field(
            default=None,
            metadata={
                "name": "deliveryService",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


class ExternalReportWssserviceGetDeliveryServiceDefinition:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetDeliveryServiceDefinitionInput
    output = ExternalReportWssserviceGetDeliveryServiceDefinitionOutput


@dataclass
class ExternalReportWssserviceGetFolderContentsOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetFolderContentsOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceGetFolderContentsOutput.Policyreference"] = (
        field(
            default=None,
            metadata={
                "name": "Policyreference",
                "type": "Element",
            },
        )
    )

    @dataclass
    class Body:
        get_folder_contents_response: Optional[GetFolderContentsResponse] = field(
            default=None,
            metadata={
                "name": "getFolderContentsResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetFolderContentsOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceGetFolderContentsOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_folder_contents_response: Optional[GetFolderContentsResponse] = field(
            default=None,
            metadata={
                "name": "getFolderContentsResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


class ExternalReportWssserviceGetTemplateParameters:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetTemplateParametersInput
    output = ExternalReportWssserviceGetTemplateParametersOutput


@dataclass
class ExternalReportWssserviceRunReportOutput:
    class Meta:
        name = "Envelope"
        namespace = "http://www.w3.org/2003/05/soap-envelope"

    body: Optional["ExternalReportWssserviceRunReportOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    header: Optional["ExternalReportWssserviceRunReportOutput.Header"] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceRunReportOutput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Header:
        run_report_response: Optional[RunReportResponse] = field(
            default=None,
            metadata={
                "name": "runReportResponse",
                "type": "Element",
            },
        )

    @dataclass
    class Body:
        run_report_response: Optional[RunReportResponse] = field(
            default=None,
            metadata={
                "name": "runReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceRunReportOutput.Body.Fault"] = field(
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
            detail: Optional["ExternalReportWssserviceRunReportOutput.Body.Fault.Detail"] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        run_report_response: Optional[RunReportResponse] = field(
            default=None,
            metadata={
                "name": "runReportResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ReportDefinition:
    auto_run: Optional[bool] = field(
        default=None,
        metadata={
            "name": "autoRun",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    cache_document: Optional[bool] = field(
        default=None,
        metadata={
            "name": "cacheDocument",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    default_output_format: Optional[str] = field(
        default=None,
        metadata={
            "name": "defaultOutputFormat",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    default_template_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "defaultTemplateId",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    diagnostics: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    list_of_template_formats_label_values: Optional[ArrayOfTemplateFormatsLabelValues] = field(
        default=None,
        metadata={
            "name": "listOfTemplateFormatsLabelValues",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    on_line: Optional[bool] = field(
        default=None,
        metadata={
            "name": "onLine",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    open_link_in_new_window: Optional[bool] = field(
        default=None,
        metadata={
            "name": "openLinkInNewWindow",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    parameter_columns: Optional[int] = field(
        default=None,
        metadata={
            "name": "parameterColumns",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    parameter_names: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "parameterNames",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_defn_title: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportDefnTitle",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportDescription",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportName",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_parameter_name_values: Optional[ArrayOfParamNameValue] = field(
        default=None,
        metadata={
            "name": "reportParameterNameValues",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    report_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportType",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )
    show_controls: Optional[bool] = field(
        default=None,
        metadata={
            "name": "showControls",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    show_report_links: Optional[bool] = field(
        default=None,
        metadata={
            "name": "showReportLinks",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "required": True,
        },
    )
    template_ids: Optional[ArrayOfString] = field(
        default=None,
        metadata={
            "name": "templateIds",
            "type": "Element",
            "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            "nillable": True,
        },
    )


@dataclass
class GetReportParameters:
    class Meta:
        name = "getReportParameters"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_request: Optional[ReportRequest] = field(
        default=None,
        metadata={
            "name": "reportRequest",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class GetReportParametersResponse:
    class Meta:
        name = "getReportParametersResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_report_parameters_return: Optional[ParamNameValues] = field(
        default=None,
        metadata={
            "name": "getReportParametersReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class RunReport:
    class Meta:
        name = "runReport"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_request: Optional[ReportRequest] = field(
        default=None,
        metadata={
            "name": "reportRequest",
            "type": "Element",
            "required": True,
        },
    )
    app_params: Optional[str] = field(
        default=None,
        metadata={
            "name": "appParams",
            "type": "Element",
            "required": True,
        },
    )


class ExternalReportWssserviceDeliveryService:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceDeliveryServiceInput
    output = ExternalReportWssserviceDeliveryServiceOutput


class ExternalReportWssserviceGetFolderContents:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetFolderContentsInput
    output = ExternalReportWssserviceGetFolderContentsOutput


@dataclass
class ExternalReportWssserviceGetReportParametersInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetReportParametersInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetReportParametersInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_report_parameters: Optional[GetReportParameters] = field(
            default=None,
            metadata={
                "name": "getReportParameters",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        get_report_parameters: Optional[GetReportParameters] = field(
            default=None,
            metadata={
                "name": "getReportParameters",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceGetReportParametersOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetReportParametersOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetReportParametersOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_report_parameters_response: Optional[GetReportParametersResponse] = field(
            default=None,
            metadata={
                "name": "getReportParametersResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetReportParametersOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceGetReportParametersOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_report_parameters_response: Optional[GetReportParametersResponse] = field(
            default=None,
            metadata={
                "name": "getReportParametersResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class ExternalReportWssserviceRunReportInput:
    class Meta:
        name = "Envelope"
        namespace = "http://www.w3.org/2003/05/soap-envelope"

    body: Optional["ExternalReportWssserviceRunReportInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional["ExternalReportWssserviceRunReportInput.Policyreference"] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        run_report: Optional[RunReport] = field(
            default=None,
            metadata={
                "name": "runReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        run_report: Optional[RunReport] = field(
            default=None,
            metadata={
                "name": "runReport",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


@dataclass
class GetReportDefinitionResponse:
    class Meta:
        name = "getReportDefinitionResponse"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    get_report_definition_return: Optional[ReportDefinition] = field(
        default=None,
        metadata={
            "name": "getReportDefinitionReturn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class UpdateReportDefinition:
    class Meta:
        name = "updateReportDefinition"
        namespace = "http://xmlns.oracle.com/oxp/service/PublicReportService"

    report_abs_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "reportAbsPath",
            "type": "Element",
            "required": True,
        },
    )
    new_report_defn: Optional[ReportDefinition] = field(
        default=None,
        metadata={
            "name": "newReportDefn",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class ExternalReportWssserviceGetReportDefinitionOutput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceGetReportDefinitionOutput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceGetReportDefinitionOutput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        get_report_definition_response: Optional[GetReportDefinitionResponse] = field(
            default=None,
            metadata={
                "name": "getReportDefinitionResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )
        fault: Optional["ExternalReportWssserviceGetReportDefinitionOutput.Body.Fault"] = field(
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
            detail: Optional[
                "ExternalReportWssserviceGetReportDefinitionOutput.Body.Fault.Detail"
            ] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "namespace": "",
                },
            )

            @dataclass
            class Detail:
                access_denied_exception: Optional[AccessDeniedException] = field(
                    default=None,
                    metadata={
                        "name": "AccessDeniedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                operation_failed_exception: Optional[OperationFailedException] = field(
                    default=None,
                    metadata={
                        "name": "OperationFailedException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )
                invalid_parameters_exception: Optional[InvalidParametersException] = field(
                    default=None,
                    metadata={
                        "name": "InvalidParametersException",
                        "type": "Element",
                        "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
                    },
                )

    @dataclass
    class Policyreference:
        get_report_definition_response: Optional[GetReportDefinitionResponse] = field(
            default=None,
            metadata={
                "name": "getReportDefinitionResponse",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


class ExternalReportWssserviceGetReportParameters:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetReportParametersInput
    output = ExternalReportWssserviceGetReportParametersOutput


class ExternalReportWssserviceRunReport:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceRunReportInput
    output = ExternalReportWssserviceRunReportOutput


@dataclass
class ExternalReportWssserviceUpdateReportDefinitionInput:
    class Meta:
        name = "Envelope"

    body: Optional["ExternalReportWssserviceUpdateReportDefinitionInput.Body"] = field(
        default=None,
        metadata={
            "name": "Body",
            "type": "Element",
        },
    )
    policyreference: Optional[
        "ExternalReportWssserviceUpdateReportDefinitionInput.Policyreference"
    ] = field(
        default=None,
        metadata={
            "name": "Policyreference",
            "type": "Element",
        },
    )

    @dataclass
    class Body:
        update_report_definition: Optional[UpdateReportDefinition] = field(
            default=None,
            metadata={
                "name": "updateReportDefinition",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )

    @dataclass
    class Policyreference:
        update_report_definition: Optional[UpdateReportDefinition] = field(
            default=None,
            metadata={
                "name": "updateReportDefinition",
                "type": "Element",
                "namespace": "http://xmlns.oracle.com/oxp/service/PublicReportService",
            },
        )


class ExternalReportWssserviceGetReportDefinition:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceGetReportDefinitionInput
    output = ExternalReportWssserviceGetReportDefinitionOutput


class ExternalReportWssserviceUpdateReportDefinition:
    uri = "#wss11_saml_or_username_token_with_message_protection_service_policy"
    style = "document"
    required = "false"
    location = "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/xmlpserver/services/ExternalReportWSSService"
    transport = "http://www.w3.org/2003/05/soap/bindings/HTTP/"
    soap_action_required = "false"
    input = ExternalReportWssserviceUpdateReportDefinitionInput
    output = ExternalReportWssserviceUpdateReportDefinitionOutput
