from services.processor import process_csv
import pytest
from services.processor import process_csv, PermanentCSVError

def test_process_valid_csv_file(tmp_path):
    csv_file = tmp_path / "sales.csv"
    csv_file.write_text(
        "customer_id,product,quantity,price\n"
        "1,Laptop,2,100\n"

    )
    result = process_csv(csv_file)

    assert result["rows_received"] == 1
    assert result["rows_valid"] == 1
    assert result["rows_rejected"] == 0
    assert result["duplicates_removed"] == 0
    assert result["total_revenue"] == 200

def test_process_csv_rejects_invalid_row(tmp_path):
    csv_file = tmp_path/ "invalid_sales.csv"
    csv_file.write_text(
        "customer_id,product,quantity,price\n"
        "1,Laptop,-2,100\n"
    )

    result = process_csv(csv_file)

    assert result["rows_received"] == 1
    assert result["rows_valid"] == 0
    assert result["rows_rejected"] == 1
    assert result["duplicates_removed"] == 0
    assert result["total_revenue"] == 0

def test_process_csv_removes_duplicates(tmp_path):
    csv_file = tmp_path / "duplicate_sales.csv"

    csv_file.write_text(
        "customer_id,product,quantity,price\n"
        "1,Laptop,2,100\n"
        "1,Laptop,2,100\n"
    )

    result = process_csv(csv_file)

    assert result["rows_received"] == 2
    assert result["rows_valid"] == 1
    assert result["rows_rejected"] == 0
    assert result["duplicates_removed"] == 1
    assert result["total_revenue"] == 200

def test_process_csv_missing_required_column(tmp_path):
    csv_file = tmp_path / "missing_column.csv"

    csv_file.write_text(
        "customer_id,quantity,price\n"
        "1,2,100\n"
    )

    with pytest.raises(PermanentCSVError):
        process_csv(csv_file)


def test_process_csv_no_data_rows(tmp_path):
    csv_file = tmp_path / "no_rows.csv"

    csv_file.write_text(
        "customer_id,product,quantity,price\n"
    )

    with pytest.raises(PermanentCSVError):
        process_csv(csv_file)
