import os
from pathlib import Path
from typing import Optional

from ibm_watsonx_orchestrate.agent_builder.connections.types import (
    ConnectionType,
    ExpectedCredentials,
)
from ibm_watsonx_orchestrate.cli.config import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_FILE_FOLDER
from ibm_watsonx_orchestrate.client.utils import is_local_dev

from agent_ready_tools.clients.clients_enums import AccessLevel, AribaApplications, DNBEntitlements
from agent_ready_tools.utils.systems import Systems
from agent_ready_tools.utils.tool_cred_utils import (
    InvalidConnectionSubCategoryError,
    UnsupportedConnectionSubCategoryError,
)

# Assigned suffix for domain agents published by IBM in SaaS catalogs.
IBM_PUBLISHER_SUFFIX = "_ibm_184bdbd3"


def published_app_id(app_id: str, suffix: str = IBM_PUBLISHER_SUFFIX) -> str:
    """Returns the given app_id with the given suffix appended."""

    # For env setup during import in chat if permission error, then use suffix.
    # For local envs, will modify the suffix var during import deliverable building.
    config_path = Path(DEFAULT_CONFIG_FILE_FOLDER) / DEFAULT_CONFIG_FILE
    if config_path.exists() and os.access(str(config_path), os.R_OK):
        if is_local_dev():
            return app_id

    return app_id + suffix


### Connection Constants
ADOBE_WORKFRONT_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("adobe_workfront_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

AMAZON_S3_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("amazon_s3_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

ARIBA_BASE_CONNECTION = ExpectedCredentials(
    app_id=published_app_id("ariba_base_key_value"), type=ConnectionType.KEY_VALUE
)

ARIBA_BUYER_CONNECTIONS = [
    ARIBA_BASE_CONNECTION,
    ExpectedCredentials(
        app_id=published_app_id("ariba_buyer_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

ARIBA_SOAP_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("ariba_soap_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

ARIBA_SUPPLIER_CONNECTIONS = [
    ARIBA_BASE_CONNECTION,
    ExpectedCredentials(
        app_id=published_app_id("ariba_supplier_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

BOX_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("box_key_value"), type=ConnectionType.KEY_VALUE),
]

GOOGLE_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("google_key_value"), type=ConnectionType.KEY_VALUE),
]

COUPA_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("coupa_key_value"), type=ConnectionType.KEY_VALUE),
]

DNB_BASE_CONNECTION = ExpectedCredentials(
    app_id=published_app_id("dnb_base_key_value"), type=ConnectionType.KEY_VALUE
)

DNB_PROCUREMENT_CONNECTIONS = [
    DNB_BASE_CONNECTION,
    ExpectedCredentials(
        app_id=published_app_id("dnb_procurement_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

DNB_SALES_CONNECTIONS = [
    DNB_BASE_CONNECTION,
    ExpectedCredentials(
        app_id=published_app_id("dnb_sales_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

HUBSPOT_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("hubspot_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

IBM_PA_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("ibm_planning_analytics"), type=ConnectionType.BASIC_AUTH
    ),
]

IBM_COS_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("ibm_cos_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

JIRA_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("jira_basic"), type=ConnectionType.BASIC_AUTH),
    ExpectedCredentials(app_id=published_app_id("jira_key_value"), type=ConnectionType.KEY_VALUE),
]

MICROSOFT_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("microsoft_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

MONDAY_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("monday_bearer"), type=ConnectionType.BEARER_TOKEN),
]

OPENPAGES_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("openpages_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

GITHUB_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("github_key_value"), type=ConnectionType.KEY_VALUE),
]

ORACLE_HCM_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("oracle_hcm_basic"),
        type=ConnectionType.BASIC_AUTH,
    ),
    ExpectedCredentials(
        app_id=published_app_id("oracle_hcm_key_value"),
        type=ConnectionType.KEY_VALUE,
    ),
]

ORACLE_FUSION_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("oracle_fusion_basic"),
        type=ConnectionType.BASIC_AUTH,
    ),
]

SALESFORCE_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("salesforce_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

SALESLOFT_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("salesloft_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

SAP_SUCCESSFACTORS_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("sap_successfactors_basic"), type=ConnectionType.BASIC_AUTH
    ),
    ExpectedCredentials(
        app_id=published_app_id("sap_successfactors_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

SAP_S4_HANA_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("sap_s4_hana_basic"), type=ConnectionType.BASIC_AUTH
    )
]

SEISMIC_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("seismic_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

SERVICENOW_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("servicenow_bearer"), type=ConnectionType.BEARER_TOKEN
    ),
    ExpectedCredentials(
        app_id=published_app_id("servicenow_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

SLACK_CONNECTIONS = [
    ExpectedCredentials(app_id=published_app_id("slack_bearer"), type=ConnectionType.BEARER_TOKEN),
    ExpectedCredentials(app_id=published_app_id("slack_key_value"), type=ConnectionType.KEY_VALUE),
]

WORKDAY_BASE_CONNECTION = ExpectedCredentials(
    app_id=published_app_id("workday_base_key_value"), type=ConnectionType.KEY_VALUE
)

WORKDAY_EMPLOYEE_CONNECTIONS = [
    WORKDAY_BASE_CONNECTION,
    ExpectedCredentials(
        app_id=published_app_id("workday_employee_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

WORKDAY_MANAGER_CONNECTIONS = [
    WORKDAY_BASE_CONNECTION,
    ExpectedCredentials(
        app_id=published_app_id("workday_manager_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

# TODO: use when oauth2 is supported locally by ADK
WORKDAY_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("workday_oauth2_auth_code"), type=ConnectionType.OAUTH2_AUTH_CODE
    ),
]

WATSON_COMMERCE_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("watson_commerce_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

STERLING_OMS_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("sterling_oms_basic"), type=ConnectionType.BASIC_AUTH
    ),
    ExpectedCredentials(
        app_id=published_app_id("sterling_oms_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

ZENDESK_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("zendesk_key_value"), type=ConnectionType.KEY_VALUE
    ),
]

ZOOMINFO_CONNECTIONS = [
    ExpectedCredentials(
        app_id=published_app_id("zoominfo_key_value"), type=ConnectionType.KEY_VALUE
    ),
]


def get_expected_credentials(
    system: Systems, sub_category: Optional[str] = None
) -> Optional[ExpectedCredentials]:
    """
    Returns the required ExpectedCredentials configuration for a given system's tools.

    Args:
        system: The system to return connections for.
        sub_category: A specific sub-category of creds for the given system.

    Returns:
        The ExpectedCredentials for the system.
    """
    if system == Systems.ADOBEWORKFRONT:
        return ADOBE_WORKFRONT_CONNECTIONS
    elif system == Systems.ARIBA:
        if sub_category not in AribaApplications:
            raise InvalidConnectionSubCategoryError(system, sub_category, AribaApplications)
        elif sub_category == AribaApplications.BUYER:
            return ARIBA_BUYER_CONNECTIONS
        elif sub_category == AribaApplications.SUPPLIER:
            return ARIBA_SUPPLIER_CONNECTIONS
        raise UnsupportedConnectionSubCategoryError(system, sub_category)
    elif system == Systems.ARIBA_SOAP:
        return ARIBA_SOAP_CONNECTIONS
    elif system == Systems.AMAZON_S3:
        return AMAZON_S3_CONNECTIONS
    elif system == Systems.BOX:
        return BOX_CONNECTIONS
    elif system == Systems.COUPA:
        return COUPA_CONNECTIONS
    elif system == Systems.DNB:
        if sub_category not in DNBEntitlements:
            raise InvalidConnectionSubCategoryError(system, sub_category, DNBEntitlements)
        elif sub_category == DNBEntitlements.PROCUREMENT:
            return DNB_PROCUREMENT_CONNECTIONS
        elif sub_category == DNBEntitlements.SALES:
            return DNB_SALES_CONNECTIONS
        raise UnsupportedConnectionSubCategoryError(system, sub_category)
    elif system == Systems.GOOGLE:
        return GOOGLE_CONNECTIONS
    elif system == Systems.HUBSPOT:
        return HUBSPOT_CONNECTIONS
    elif system == Systems.IBM_COS:
        return IBM_COS_CONNECTIONS
    elif system == Systems.JIRA:
        return JIRA_CONNECTIONS
    elif system == Systems.MICROSOFT:
        return MICROSOFT_CONNECTIONS
    elif system == Systems.ORACLE_HCM:
        return ORACLE_HCM_CONNECTIONS
    elif system == Systems.ORACLE_FUSION:
        return ORACLE_FUSION_CONNECTIONS
    elif system == Systems.SALESFORCE:
        return SALESFORCE_CONNECTIONS
    elif system == Systems.SALESLOFT:
        return SALESLOFT_CONNECTIONS
    elif system == Systems.SAP_SUCCESSFACTORS:
        return SAP_SUCCESSFACTORS_CONNECTIONS
    elif system == Systems.SAP_S4_HANA:
        return SAP_S4_HANA_CONNECTIONS
    elif system == Systems.SEISMIC:
        return SEISMIC_CONNECTIONS
    elif system == Systems.SERVICENOW:
        return SERVICENOW_CONNECTIONS
    elif system == Systems.SLACK:
        return SLACK_CONNECTIONS
    elif system == Systems.WATSON_COMMERCE:
        return WATSON_COMMERCE_CONNECTIONS
    elif system == Systems.STERLING_OMS:
        return STERLING_OMS_CONNECTIONS
    elif system == Systems.WORKDAY:
        if sub_category not in AccessLevel:
            raise InvalidConnectionSubCategoryError(system, sub_category, AccessLevel)
        elif sub_category == AccessLevel.EMPLOYEE:
            return WORKDAY_EMPLOYEE_CONNECTIONS
        elif sub_category == AccessLevel.MANAGER:
            return WORKDAY_MANAGER_CONNECTIONS
        raise UnsupportedConnectionSubCategoryError(system, sub_category)
    elif system == Systems.ZENDESK:
        return ZENDESK_CONNECTIONS
    elif system == Systems.ZOOMINFO:
        return ZOOMINFO_CONNECTIONS
    return None
