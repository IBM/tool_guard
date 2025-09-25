from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_hierarchies_and_connections_l1 import (
    dnb_get_hierarchies_and_connections_l1,
)


def test_dnb_get_hierarchies_and_connections_l1() -> None:
    """Test that the `get_hierarchies_and_connections_l1` function returns the expected response."""

    # Define test data:
    test_company_id = "001368083"
    test_data = {
        "family_tree_roles": [
            {"description": "Global Ultimate", "dnbCode": 12775},
            {"description": "Domestic Ultimate", "dnbCode": 12774},
            {"description": "Parent/Headquarters", "dnbCode": 9141},
        ],
        "global_ultimate_primary_name": "International Business Machines Corporation",
        "domestic_ultimate_primary_name": "International Business Machines Corporation",
        "global_ultimate_family_tree_members_count": 1352,
        "hierarchy_level": 1,
        "branch_count": None,
        "branches": None,
    }

    # Patch `get_dnb_client` to return a mock client
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_hierarchies_and_connections_l1.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = {
            "organization": {
                "duns": test_company_id,
                "corporateLinkage": {
                    "familytreeRolesPlayed": test_data["family_tree_roles"],
                    "globalUltimate": {
                        "primaryName": test_data["global_ultimate_primary_name"],
                        "duns": test_company_id,
                    },
                    "domesticUltimate": {
                        "primaryName": test_data["domestic_ultimate_primary_name"],
                        "duns": test_company_id,
                    },
                    "globalUltimateFamilyTreeMembersCount": test_data[
                        "global_ultimate_family_tree_members_count"
                    ],
                    "hierarchyLevel": test_data["hierarchy_level"],
                    "branchesCount": test_data["branch_count"],
                    "branches": test_data["branches"],
                },
            },
        }

        # Get purchase by ID
        response = dnb_get_hierarchies_and_connections_l1(duns_number=test_company_id).content

        # Ensure that get_hierarchies_and_connections_l1() executed and returned proper values
        assert response
        assert response.duns_number == test_company_id

        assert response.family_tree_roles == test_data["family_tree_roles"]
        assert (
            response.family_tree_member_count
            == test_data["global_ultimate_family_tree_members_count"]
        )
        assert response.global_ultimate == test_data["global_ultimate_primary_name"]
        assert response.domestic_ultimate == test_data["domestic_ultimate_primary_name"]
        assert response.hierarchy_level == test_data["hierarchy_level"]
        assert response.branches_count == test_data["branch_count"]
        assert response.branches == test_data["branches"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_company_id,
            params={"blockIDs": "hierarchyconnections_L1_v1"},
        )
