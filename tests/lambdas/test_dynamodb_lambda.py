from decimal import Decimal
from unittest import TestCase
import json
from lambdas.dynamodb.dynamodb_lambda import handler
import boto3
from unittest.mock import patch


class TestDynamodbLambda(TestCase):
    @patch.object(boto3, "resource")
    def test_dynamodb_lambda(self, mock_resource):
        table_mock = mock_resource().Table.return_value
        table_mock.update_item.return_value = {
            "Attributes": {"atomic_counter": Decimal(4)},
        }
        response = handler({}, {})
        self.assertDictEqual(response["headers"], {"Content-Type": "application/json"})
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(response["body"], json.dumps({"counter": 4}))
