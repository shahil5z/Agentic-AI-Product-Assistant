import csv
import os
from model import ProductResponse

def log_query_response(query: str, response: ProductResponse):
    filename = "query_log.csv"
    file_exists = os.path.exists(filename)

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["query", "product_name", "details", "price", "release_date"])
        writer.writerow([query, response.name, response.details, response.price, response.release_date])
