from rich.console import Console
from rich.table import Table

console = Console()

def make_progress_bar(pct):
    filled = int(pct * 10)
    empty = 10 - filled
    return f"[cyan]{'█' * filled}[/cyan]{'░' * empty} {int(pct * 100)}%"

def print_amortization(amortization):
    table = Table(title="Amortization Schedule", show_lines=True)

    table.add_column("Date", style="cyan")
    table.add_column("Debt", style="white")
    table.add_column("Start", justify="right", style="yellow")
    table.add_column("Interest", justify="right", style="magenta")
    table.add_column("Payment", justify="right", style="green")
    table.add_column("Extra", justify="right", style="blue")
    table.add_column("End", justify="right", style="red")
    table.add_column("Progress", justify="left", style="white")

    for row in amortization:
        pct = row["progress"]

        # -----------------------------
        # Conditional formatting rules
        # -----------------------------
        if pct >= 1.0:
            # Final payment — bright green background
            debt_cell = f"[on bright_green]{row['debt']}[/]"
            row_style = "on bright_green"
        #elif pct >= 0.90:
        #    # 90%+ — light blue background
        #    debt_cell = f"[on sky_blue1]{row['debt']}[/]"
        #    row_style = "on sky_blue1"
        else:
            debt_cell = row["debt"]
            row_style = ""

        # Progress bar
        progress_bar = make_progress_bar(pct)

        table.add_row(
            row["date"],
            debt_cell,
            f"${row['starting_balance']:,.2f}",
            f"${row['interest_added']:,.2f}",
            f"${row['payment']:,.2f}",
            f"${row['extra']:,.2f}",
            f"${row['ending_balance']:,.2f}",
            progress_bar,
            style=row_style
        )

    console.print()
    console.print(table)
    console.print()
