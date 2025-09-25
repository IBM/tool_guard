from typing import Any, Dict, List, cast
from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.enroll_learning import (
    enroll_learning,
)
from agent_ready_tools.utils.get_id_from_links import get_id_from_links


def test_enroll_learning() -> None:
    """Test that a manager change can be initiated successfully by the `enroll_learning` tool."""

    # Define test data:
    test_data = {
        "assignmentRecordId": 300000281731604,
        "assignmentType": "ORA_JOIN_ASSIGNMENT",
        "assignmentTypeMeaning": "Voluntary Assignment",
        "assignmentStatus": "ORA_ASSN_REC_ACTIVE",
        "assignmentStatusMeaning": "Active",
        "assignmentSubStatus": "ORA_ASSN_REC_NO_OFFR",
        "assignmentSubStatusMeaning": "No Active Offering",
        "assignmentDetailsDeepLink": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/fscmUI/redwood/learner/learn/learn-enrollment-details?learnerRecordId=300000281731604&persona=ORA_LEARNER",
        "assignmentDetailsEmbedLink": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/fscmUI/redwood/learner/learn/learn-enrollment-details?learnerRecordId=300000281731604&persona=ORA_LEARNER",
        "assignmentAttributionId": 300000281382510,
        "assignedToId": 300000281382510,
        "assignedToPersonImageURL": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmUI/personImage?personId=300000281382510",
        "assignerAttributionType": "ORA_PERSON",
        "assignerAttributionTypeMeaning": "Person",
        "learningItemId": 300000142578740,
        "learningItemNumber": "OLC130007",
        "learningItemType": "ORA_COURSE",
        "learningItemTypeMeaning": "Course",
        "learningItemDeepLink": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/fscmUI/redwood/learner/learn/redirect?learningItemId=300000142578740&learningItemType=ORA_COURSE",
        "learningItemEmbedLink": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/fscmUI/redwood/learner/learn/redirect?learningItemId=300000142578740&learningItemType=ORA_COURSE",
        "learningItemDataLink": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/latest/learnerLearningCatalogItems/300000142578740",
        "assignedDate": "2025-04-01T21:07:05.842+00:00",
        "expirationRule": "Never Expires",
        "dataSecurityPrivilege": "ORA_LEARNER",
        "dataSecurityPrivilegeMeaning": "Learner",
        "sourceType": "ORA_SELF_ENROLLMENTS",
        "activeDate": "2025-04-01T21:07:05.874+00:00",
        "learningItemCoverArtLink": "https://static.oracle.com/cdn/fnd/gallery/2310.0.1/images/hcm-journey-headers-abstract-final-3.png",
        "learningItemThumbnailLink": "https://static.oracle.com/cdn/fnd/gallery/2310.0.1/images/hcm-journey-headers-abstract-final-3.png",
        "canEditAssignmentHint": "CAN_WITHDRAW",
        "canEditAssignmentHintMeaning": "Can withdraw",
        "assignmentStateSeverity": "ORA_INFO",
        "assignmentStateMeaning": "No Active Offering",
        "links": [
            {
                "rel": "self",
                "href": "https://fa-etaj-dev23-saasfademo1.ds-fa.oraclepdemos.com:443/hcmRestApi/resources/11.13.18.05/learnerLearningRecords/00030000004AACED00057372000D6A6176612E73716C2E4461746514FA46683F3566970200007872000E6A6176612E7574696C2E44617465686A81014B5974190300007870770800000195EEA5D400780000000EACED00057708000110D94239A2140000000B4F52415F4C4541524E4552",
                "name": "learnerLearningRecords",
                "kind": "item",
                "properties": {
                    "changeIndicator": "ACED0005737200136A6176612E7574696C2E41727261794C6973747881D21D99C7619D03000149000473697A65787000000002770400000002737200116A6176612E6C616E672E496E746567657212E2A0A4F781873802000149000576616C7565787200106A6176612E6C616E672E4E756D62657286AC951D0B94E08B0200007870000000017371007E00020000000178"
                },
            }
        ],
        "status_code": 201,
    }

    # Patch `get_oracle_hcm_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.hr.learning_and_development.oracle_hcm.enroll_learning.get_oracle_hcm_client"
    ) as mock_get_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.post_request.return_value = {
            "assignmentSubStatusMeaning": test_data.get("assignmentSubStatusMeaning", ""),
            "assignerDisplayName": test_data.get("assignerDisplayName", ""),
            "assignedDate": test_data.get("assignedDate", ""),
            "links": test_data.get("links", []),
            "assignmentRecordId": test_data.get("assignmentRecordId", ""),
            "status_code": test_data["status_code"],
        }

        payload = {"course_number": "300000133971193", "person_id": "300000048984276"}

        response = enroll_learning(
            course_number=payload.get("course_number", ""),
            person_id=payload.get("person_id", ""),
        )

        links = cast(List[Dict[str, Any]], test_data.get("links", [{}]))

        assert response
        assert response.assignment_uuid == get_id_from_links(links[0].get("href", ""))

        # Ensure the API call was made with expected parameters
        mock_client.post_request.assert_called_once_with(
            payload={
                "learningItemNumber": payload.get("course_number", ""),
                "assignedToId": payload.get("person_id", ""),
            },
            entity="learnerLearningRecords",
            headers={"Content-Type": "application/vnd.oracle.adf.resourceitem+json"},
        )
