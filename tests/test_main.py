import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def lists_data():
    return {
        "list_1": ["first string", "second string", "third string"],
        "list_2": ["other string", "another string", "last string"]
    }


def test_create_payload(lists_data):
    response = client.post("/payload", json=lists_data)
    assert response.status_code == 200
    data = response.json()
    assert "payload_id" in data
    assert "message" in data


def test_read_payload(lists_data):
    # Create the payload
    create_resp = client.post("/payload", json=lists_data)
    assert create_resp.status_code == 200
    payload_id = create_resp.json()["payload_id"]

    # Retrieve the payload
    get_resp = client.get(f"/payload/{payload_id}")
    assert get_resp.status_code == 200
    payload_data = get_resp.json()

    # Verify the final output
    expected_output = (
        "FIRST STRING, OTHER STRING, "
        "SECOND STRING, ANOTHER STRING, "
        "THIRD STRING, LAST STRING"
    )
    assert payload_data["output"] == expected_output
