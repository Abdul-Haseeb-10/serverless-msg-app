import json
import os
import pytest
from lambda_fn.app import handler

@pytest.fixture
def valid_event():
    return {
        "body": json.dumps({
            "messageUUID": "123e4567-e89b-12d3-a456-426614174000",
            "messageText": "Hello from test!",
            "messageDatetime": "2025-06-21 12:00:00"
        })
    }

def test_handler_valid_payload(monkeypatch, valid_event):
    # Mock environment variable
    os.environ["TABLE_NAME"] = "DummyTable"

    # Mock boto3 DynamoDB Table put_item
    class DummyTable:
        def put_item(self, Item):
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    class DummyDynamoResource:
        def Table(self, name):
            return DummyTable()

    monkeypatch.setattr("boto3.resource", lambda service: DummyDynamoResource())

    response = handler(valid_event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["message"] == "Saved successfully."

def test_handler_short_message(monkeypatch):
    os.environ["TABLE_NAME"] = "DummyTable"

    short_event = {
        "body": json.dumps({
            "messageUUID": "123e4567-e89b-12d3-a456-426614174000",
            "messageText": "Hi",
            "messageDatetime": "2025-06-21 12:00:00"
        })
    }

    class DummyTable:
        def put_item(self, Item):
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    class DummyDynamoResource:
        def Table(self, name):
            return DummyTable()

    monkeypatch.setattr("boto3.resource", lambda service: DummyDynamoResource())

    response = handler(short_event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "messageText must be between 10 and 100 characters" in body["error"]

def test_handler_invalid_datetime(monkeypatch):
    os.environ["TABLE_NAME"] = "DummyTable"

    bad_date_event = {
        "body": json.dumps({
            "messageUUID": "123e4567-e89b-12d3-a456-426614174000",
            "messageText": "This is a valid length message.",
            "messageDatetime": "06-21-2025 12:00:00"  # wrong format
        })
    }

    class DummyTable:
        def put_item(self, Item):
            return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    class DummyDynamoResource:
        def Table(self, name):
            return DummyTable()

    monkeypatch.setattr("boto3.resource", lambda service: DummyDynamoResource())

    response = handler(bad_date_event, None)
    body = json.loads(response["body"])

    assert response["statusCode"] == 400
    assert "messageDatetime must be in YYYY-MM-DD HH:MM:SS format." in body["error"]