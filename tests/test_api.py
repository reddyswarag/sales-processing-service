from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_upload_rejects_non_csv_file():
    response = client.post(
        "/jobs/upload",
        files={
            "file": ("notes.txt", b"hello", "text/plain")
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "only .csv files are accepted"
    }


def test_upload_rejects_empty_csv_file():
    response = client.post(
        "/jobs/upload",
        files={
            "file": ("empty.csv", b"", "text/csv")
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "empty files are not allowed"
    }


def test_upload_rejects_file_too_large():
    large_file = b"a" * (50 * 1024 * 1024 + 1)

    response = client.post(
        "/jobs/upload",
        files={
            "file": ("large.csv", large_file, "text/csv")
        }
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "file size exceeds the maximum limit"
    }