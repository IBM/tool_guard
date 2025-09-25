from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_information_l3 import (
    dnb_get_company_information_l3,
)


def test_dnb_get_company_information_l3() -> None:
    """Test that the `find_company_information_l3` function returns the expected response."""

    # Define test data:
    test_company_id = "001368083"
    test_data = {
        "organization": {
            "duns": test_company_id,
            "primaryName": "International Business Machines Corporation",
            "localOperatingStatus": [],
            "numberOfEmployees": [
                {
                    "value": 850,
                    "employeeFiguresDate": None,
                    "informationScopeDescription": "Headquarters Only (Employs Here)",
                    "informationScopeDnBCode": 9068,
                    "reliabilityDescription": "Actual",
                    "reliabilityDnBCode": 9092,
                    "employeeCategories": [],
                },
                {
                    "value": 279200,
                    "employeeFiguresDate": None,
                    "informationScopeDescription": "Consolidated",
                    "informationScopeDnBCode": 9067,
                    "reliabilityDescription": "Actual",
                    "reliabilityDnBCode": 9092,
                    "employeeCategories": [
                        {
                            "employmentBasisDescription": "Principals",
                            "employmentBasisDnBCode": 9064,
                        }
                    ],
                    "trend": [
                        {
                            "timePeriod": {
                                "description": "1-3 years",
                                "dnbCode": 13711,
                            },
                            "growthRate": -16.0,
                            "value": 345900.0,
                            "reliabilityDescription": "Actual",
                            "reliabilityDnBCode": 9092,
                        }
                    ],
                },
            ],
            "startDate": "1911",
            "websiteAddress": [{"url": "www.ibm.com", "domainName": "ibm.com"}],
            "email": [],
            "telephone": [{"telephoneNumber": "9144991900", "isdCode": "1"}],
            "primaryAddress": {
                "language": {},
                "addressCountry": {"name": "United States", "isoAlpha2Code": "US"},
                "continentalRegion": {"name": "North America"},
                "addressLocality": {"name": "Armonk"},
                "minorTownName": None,
                "addressRegion": {
                    "name": "New York",
                    "abbreviatedName": "NY",
                    "isoSubDivisionName": "New York",
                    "isoSubDivisionCode": "US-NY",
                    "administrativeDivisionCode": None,
                },
                "addressCounty": {
                    "name": "Westchester",
                    "administrativeDivisionCode": None,
                },
                "postalCode": "10504-1722",
                "postalCodePosition": {},
                "postalRoute": "C007",
                "streetAddress": {"line1": "1 New Orchard Rd Ste 1", "line2": None},
                "streetNumber": None,
                "streetName": None,
                "postOfficeBox": {},
                "latitude": 41.10709,
                "longitude": -73.71912,
                "geographicalPrecision": {
                    "description": "Street Address Centroid",
                    "dnbCode": 30257,
                },
                "statisticalArea": {
                    "cbsaName": "New York-Newark-Jersey City NY-NJ-PA",
                    "cbsaCode": "35620",
                    "economicAreaOfInfluenceCode": "118",
                    "populationRank": {
                        "rankNumber": "9",
                        "rankDnBCode": 10961,
                        "rankDescription": "500,000 +",
                    },
                },
                "locationOwnership": {"description": "Occupies", "dnbCode": 3921},
                "premisesArea": {
                    "measurement": 17289.0,
                    "unitDescription": "Square Feet",
                    "unitDnBCode": 3848,
                    "reliabilityDescription": "Modelled",
                    "reliabilityDnBCode": 9094,
                },
                "standardAddressCodes": [],
                "isManufacturingLocation": None,
                "isRegisteredAddress": False,
                "isResidentialAddress": None,
                "congressionalDistricts": [{"district": "17"}],
            },
            "businessActivitiesInfo": [
                {
                    "description": "mfg electronic computers,  mfg computer storage devices",
                    "language": {"description": "US English", "dnbCode": 331},
                }
            ],
            "businessEntityType": {"description": "Corporation", "dnbCode": 451},
            "isSmallBusiness": None,
        }
    }

    # Patch `get_dnb_client` to return a mock clients
    with patch(
        "agent_ready_tools.tools.procurement.supplier_research.dnb.get_company_information_l3.get_dnb_client"
    ) as mock_dnb_client:
        # Create a mock client instance
        mock_client = MagicMock()
        mock_dnb_client.return_value = mock_client
        mock_client.get_request.return_value = test_data

        # Find company information by L4
        response = dnb_get_company_information_l3(duns_number=test_company_id).content

        # Ensure that find_company_information_l4() executed and returned proper values
        assert response
        assert response.duns_number == test_data["organization"]["duns"]
        assert response.primary_name == test_data["organization"]["primaryName"]
        assert response.operating_status == test_data["organization"]["localOperatingStatus"]
        assert response.number_of_employees == test_data["organization"]["numberOfEmployees"]
        assert response.start_date == test_data["organization"]["startDate"]
        assert response.website == test_data["organization"]["websiteAddress"]
        assert response.email == test_data["organization"]["email"]
        assert response.telephone == test_data["organization"]["telephone"]
        assert response.address == test_data["organization"]["primaryAddress"]
        assert (
            response.business_activities_info == test_data["organization"]["businessActivitiesInfo"]
        )
        assert response.business_entities_type == test_data["organization"]["businessEntityType"]
        assert response.is_small_business == test_data["organization"]["isSmallBusiness"]

        # Ensure the API call was made with expected parameters
        mock_client.get_request.assert_called_once_with(
            "v1",
            "data",
            "duns/" + test_company_id,
            params={"blockIDs": "companyinfo_L4_v1"},
        )
