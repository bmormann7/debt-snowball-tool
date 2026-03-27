import csv
from datetime import datetime

def export_amortization_csv(amortization, filename=None):
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"amortization_{timestamp}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Date", "Debt", "Starting Balance", "Interest Added",
            "Payment", "Extra", "Ending Balance"
        ])

        for row in amortization:
            writer.writerow([
                row["date"],
                row["debt"],
                f"{row['starting_balance']:.2f}",
                f"{row['interest_added']:.2f}",
                f"{row['payment']:.2f}",
                f"{row['extra']:.2f}",
                f"{row['ending_balance']:.2f}",
            ])

    return filename
