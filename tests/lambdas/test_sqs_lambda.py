from unittest import TestCase
import json
from lambdas.sqs.sqs_lambda import handler
import boto3
from unittest.mock import patch


class TestSqsLambda(TestCase):
    @patch.object(boto3, "resource")
    def test_dynamodb_lambda(self, mock_resource):
        queue_mock = mock_resource().Queue.return_value
        queue_mock.send_message.return_value = {}
        response = handler({}, {})
        self.assertDictEqual(response["headers"], {"Content-Type": "application/json"})
        self.assertEqual(response["statusCode"], 200)
        self.assertEqual(
            response["body"], json.dumps({"message": "Message sent to SQS"})
        )
