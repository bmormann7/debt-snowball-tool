from rich.console import Console
from rich.panel import Panel

console = Console()

def print_summary(amortization, months, return_text=False):
    # ----- CALCULATIONS -----
    total_interest = sum(row["interest_added"] for row in amortization)
    total_payment = sum(row["payment"] + row["extra"] for row in amortization)
    total_extra = sum(row["extra"] for row in amortization)
    total_principal = total_payment - total_interest

    avg_monthly = total_payment / months if months > 0 else 0
    max_monthly = max(row["payment"] + row["extra"] for row in amortization)
    min_monthly = min(row["payment"] + row["extra"] for row in amortization)

    # ----- TEXT BLOCK (Rich formatting) -----
    rich_text = (
        f"[bold]Total Months:[/bold] {months}\n"
        f"[bold]Total Paid:[/bold] ${total_payment:,.2f}\n"
        f"[bold]Total Principal:[/bold] ${total_principal:,.2f}\n"
        f"[bold]Total Interest:[/bold] ${total_interest:,.2f}\n"
        f"[bold]Total Extra Applied:[/bold] ${total_extra:,.2f}\n"
        f"[bold]Average Monthly Payment:[/bold] ${avg_monthly:,.2f}\n"
        f"[bold]Highest Monthly Payment:[/bold] ${max_monthly:,.2f}\n"
        f"[bold]Lowest Monthly Payment:[/bold] ${min_monthly:,.2f}"
    )

    # ----- STREAMLIT VERSION (Markdown) -----
    markdown_text = (
        f"**Total Months:** {months}\n\n"
        f"**Total Paid:** ${total_payment:,.2f}\n\n"
        f"**Total Principal:** ${total_principal:,.2f}\n\n"
        f"**Total Interest:** ${total_interest:,.2f}\n\n"
        f"**Total Extra Applied:** ${total_extra:,.2f}\n\n"
        f"**Average Monthly Payment:** ${avg_monthly:,.2f}\n\n"
        f"**Highest Monthly Payment:** ${max_monthly:,.2f}\n\n"
        f"**Lowest Monthly Payment:** ${min_monthly:,.2f}"
    )

    # ----- RETURN TEXT FOR STREAMLIT -----
    if return_text:
        return markdown_text

    # ----- DEFAULT: PRINT TO CONSOLE -----
    console.print(Panel(rich_text, title="Simulation Summary", expand=False))
