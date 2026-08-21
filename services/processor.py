import csv
import time




REQUIRED_COLUMNS = {
    "customer_id",
    "product",
    "quantity",
    "price"
}

class PermanentCSVError(Exception):
    pass




def process_csv(file_path : str):
    start_time = time.perf_counter()
    with open(file_path, "r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        actual_columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - actual_columns

        if missing_columns:
            raise PermanentCSVError(f"missing required columns {sorted(missing_columns)}")


        rows_recieved = 0
        rows_valid = 0
        rows_rejected = 0
        total_revenue = 0
        duplicates_removed = 0
        seen_rows = set()


        for row in reader:
            rows_recieved += 1

            try : 
                customer_id = row["customer_id"].strip()
                product = row["product"].strip()
                quantity = float(row["quantity"])
                price = float(row["price"])

                if not customer_id or not product:
                    raise ValueError(f'Empty required fields')

                if quantity <=0 or price<=0:
                    raise ValueError(f'Invalid Quantity or price')
            except (ValueError, TypeError, AttributeError):
                rows_rejected += 1
                continue
            row_key = (customer_id, product, quantity, price)
            if row_key in seen_rows:
                duplicates_removed += 1
                continue

            rows_valid += 1
            seen_rows.add(row_key)
            total_revenue += quantity * price

    processing_time_ms = round(
        (time.perf_counter() - start_time) * 1000,2
    )
        
    return {
        "rows_received" : rows_recieved,
        "rows_valid" : rows_valid,
        "rows_rejected" : rows_rejected,
        "total_revenue" : round(total_revenue, 2),
        "duplicates_removed" : duplicates_removed,
        "processing_time_ms" : processing_time_ms
    }