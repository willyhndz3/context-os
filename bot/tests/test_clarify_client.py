import pytest
from clarify_client import ClarifyClient


def test_client_init():
    client = ClarifyClient("test-slug", "test-key")
    assert client.base_url == "https://api.clarify.ai/v1/workspaces/test-slug"


def test_headers():
    client = ClarifyClient("test-slug", "test-key")
    assert client.headers["Authorization"] == "api-key test-key"
    assert client.headers["Content-Type"] == "application/json"


def test_person_payload():
    client = ClarifyClient("test-slug", "test-key")
    payload = client._build_person_payload("Jane Smith", "jane@acme.com", title="VP Sales")
    assert payload["data"]["attributes"]["name"] == "Jane Smith"
    assert payload["data"]["attributes"]["email_addresses"] == ["jane@acme.com"]
    assert payload["data"]["attributes"]["title"] == "VP Sales"


def test_company_payload():
    client = ClarifyClient("test-slug", "test-key")
    payload = client._build_company_payload("Acme Corp", "acme.com")
    assert payload["data"]["attributes"]["name"] == "Acme Corp"
    assert payload["data"]["attributes"]["domains"] == ["acme.com"]
