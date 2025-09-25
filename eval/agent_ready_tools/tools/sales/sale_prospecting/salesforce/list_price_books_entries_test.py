from unittest.mock import MagicMock, patch

from agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_price_book_entries import (
    list_price_book_entries,
)
from agent_ready_tools.tools.sales.sale_prospecting.salesforce.salesforce_schemas import (
    PriceBookEntry,
)


def test_list_pricebook_entries() -> None:
    """Test that the `list_price_book_entries` function returns the expected response."""

    expected = [
        PriceBookEntry(
            id="01ugL000000JwgDQAS",
            product_id="01tgL00000175yUQAQ",
            product_name="GenWatt Diesel 200kW",
            unit_price=25000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgEQAS",
            product_id="01tgL00000175yVQAQ",
            product_name="GenWatt Diesel 10kW",
            unit_price=5000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgFQAS",
            product_id="01tgL00000175yWQAQ",
            product_name="Installation: Industrial - High",
            unit_price=85000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgGQAS",
            product_id="01tgL00000175yXQAQ",
            product_name="SLA: Silver",
            unit_price=20000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgHQAS",
            product_id="01tgL00000175yYQAQ",
            product_name="GenWatt Propane 500kW",
            unit_price=50000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgIQAS",
            product_id="01tgL00000175yZQAQ",
            product_name="SLA: Platinum",
            unit_price=40000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgJQAS",
            product_id="01tgL00000175yaQAA",
            product_name="GenWatt Propane 100kW",
            unit_price=15000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgKQAS",
            product_id="01tgL00000175ybQAA",
            product_name="GenWatt Propane 1500kW",
            unit_price=120000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgLQAS",
            product_id="01tgL00000175yTQAQ",
            product_name="GenWatt Diesel 1000kW",
            unit_price=100000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgMQAS",
            product_id="01tgL00000175ycQAA",
            product_name="SLA: Bronze",
            unit_price=10000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgNQAS",
            product_id="01tgL00000175ydQAA",
            product_name="GenWatt Gasoline 750kW",
            unit_price=75000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgOQAS",
            product_id="01tgL00000175yeQAA",
            product_name="Installation: Portable",
            unit_price=5000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgPQAS",
            product_id="01tgL00000175yfQAA",
            product_name="SLA: Gold",
            unit_price=30000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgQQAS",
            product_id="01tgL00000175ygQAA",
            product_name="GenWatt Gasoline 300kW",
            unit_price=35000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgRQAS",
            product_id="01tgL00000175yhQAA",
            product_name="Installation: Industrial - Low",
            unit_price=20000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgSQAS",
            product_id="01tgL00000175yiQAA",
            product_name="GenWatt Gasoline 2000kW",
            unit_price=150000.0,
        ),
        PriceBookEntry(
            id="01ugL000000JwgTQAS",
            product_id="01tgL00000175yjQAA",
            product_name="Installation: Industrial - Medium",
            unit_price=50000.0,
        ),
        PriceBookEntry(
            id="01ugL000000SmXxQAK",
            product_id="01tgL000001TPLqQAO",
            product_name="Product1",
            unit_price=140.0,
        ),
    ]
    with patch(
        "agent_ready_tools.tools.sales.sale_prospecting.salesforce.list_price_book_entries.get_salesforce_client"
    ) as mock_salesforce_client:
        mock_client = MagicMock()
        mock_salesforce_client.return_value = mock_client
        mock_client.salesforce_object.query_all_iter.return_value = [
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgDQAS",
                },
                "Id": "01ugL000000JwgDQAS",
                "Product2Id": "01tgL00000175yUQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yUQAQ",
                    },
                    "Name": "GenWatt Diesel 200kW",
                },
                "UnitPrice": 25000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgEQAS",
                },
                "Id": "01ugL000000JwgEQAS",
                "Product2Id": "01tgL00000175yVQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yVQAQ",
                    },
                    "Name": "GenWatt Diesel 10kW",
                },
                "UnitPrice": 5000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgFQAS",
                },
                "Id": "01ugL000000JwgFQAS",
                "Product2Id": "01tgL00000175yWQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yWQAQ",
                    },
                    "Name": "Installation: Industrial - High",
                },
                "UnitPrice": 85000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgGQAS",
                },
                "Id": "01ugL000000JwgGQAS",
                "Product2Id": "01tgL00000175yXQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yXQAQ",
                    },
                    "Name": "SLA: Silver",
                },
                "UnitPrice": 20000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgHQAS",
                },
                "Id": "01ugL000000JwgHQAS",
                "Product2Id": "01tgL00000175yYQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yYQAQ",
                    },
                    "Name": "GenWatt Propane 500kW",
                },
                "UnitPrice": 50000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgIQAS",
                },
                "Id": "01ugL000000JwgIQAS",
                "Product2Id": "01tgL00000175yZQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yZQAQ",
                    },
                    "Name": "SLA: Platinum",
                },
                "UnitPrice": 40000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgJQAS",
                },
                "Id": "01ugL000000JwgJQAS",
                "Product2Id": "01tgL00000175yaQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yaQAA",
                    },
                    "Name": "GenWatt Propane 100kW",
                },
                "UnitPrice": 15000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgKQAS",
                },
                "Id": "01ugL000000JwgKQAS",
                "Product2Id": "01tgL00000175ybQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175ybQAA",
                    },
                    "Name": "GenWatt Propane 1500kW",
                },
                "UnitPrice": 120000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgLQAS",
                },
                "Id": "01ugL000000JwgLQAS",
                "Product2Id": "01tgL00000175yTQAQ",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yTQAQ",
                    },
                    "Name": "GenWatt Diesel 1000kW",
                },
                "UnitPrice": 100000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgMQAS",
                },
                "Id": "01ugL000000JwgMQAS",
                "Product2Id": "01tgL00000175ycQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175ycQAA",
                    },
                    "Name": "SLA: Bronze",
                },
                "UnitPrice": 10000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgNQAS",
                },
                "Id": "01ugL000000JwgNQAS",
                "Product2Id": "01tgL00000175ydQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175ydQAA",
                    },
                    "Name": "GenWatt Gasoline 750kW",
                },
                "UnitPrice": 75000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgOQAS",
                },
                "Id": "01ugL000000JwgOQAS",
                "Product2Id": "01tgL00000175yeQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yeQAA",
                    },
                    "Name": "Installation: Portable",
                },
                "UnitPrice": 5000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgPQAS",
                },
                "Id": "01ugL000000JwgPQAS",
                "Product2Id": "01tgL00000175yfQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yfQAA",
                    },
                    "Name": "SLA: Gold",
                },
                "UnitPrice": 30000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgQQAS",
                },
                "Id": "01ugL000000JwgQQAS",
                "Product2Id": "01tgL00000175ygQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175ygQAA",
                    },
                    "Name": "GenWatt Gasoline 300kW",
                },
                "UnitPrice": 35000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgRQAS",
                },
                "Id": "01ugL000000JwgRQAS",
                "Product2Id": "01tgL00000175yhQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yhQAA",
                    },
                    "Name": "Installation: Industrial - Low",
                },
                "UnitPrice": 20000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgSQAS",
                },
                "Id": "01ugL000000JwgSQAS",
                "Product2Id": "01tgL00000175yiQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yiQAA",
                    },
                    "Name": "GenWatt Gasoline 2000kW",
                },
                "UnitPrice": 150000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000JwgTQAS",
                },
                "Id": "01ugL000000JwgTQAS",
                "Product2Id": "01tgL00000175yjQAA",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL00000175yjQAA",
                    },
                    "Name": "Installation: Industrial - Medium",
                },
                "UnitPrice": 50000,
            },
            {
                "attributes": {
                    "type": "PricebookEntry",
                    "url": "/services/data/v60.0/sobjects/PricebookEntry/01ugL000000SmXxQAK",
                },
                "Id": "01ugL000000SmXxQAK",
                "Product2Id": "01tgL000001TPLqQAO",
                "Product2": {
                    "attributes": {
                        "type": "Product2",
                        "url": "/services/data/v60.0/sobjects/Product2/01tgL000001TPLqQAO",
                    },
                    "Name": "Product1",
                },
                "UnitPrice": 140,
            },
        ]

        response = list_price_book_entries(
            search="Pricebook2Id = '01sgL000000unndQAA' AND IsActive = true"
        )

        assert response
        assert response == expected
