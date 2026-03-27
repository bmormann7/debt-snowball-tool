from storage.file_io import load_debts, save_debts
from models.debt import Debt
from engine.snowball import simulate_snowball
from ui.simulation_setup import run_simulation_wizard
from ui.amortization import print_amortization
from rich.console import Console
from rich.table import Table
from ui.summary import print_summary
from storage.export_csv import export_amortization_csv

console = Console()

# -----------------------------
# CHART MENU (kept for later use)
# -----------------------------
def chart_menu(amortization):
    console.print("\n[bold cyan]Charts Available:[/]")
    console.print("1. Balance Over Time")
    console.print("2. Payment Breakdown")
    console.print("3. Payoff Timeline")
    console.print("4. Progress Bars")
    console.print("5. Interest vs Principal")
    console.print("6. Back")

    choice = input("Choose a chart: ")

    if choice == "1":
        from charts.balance_over_time import show_chart
        show_chart(amortization)

    elif choice == "2":
        from charts.payment_breakdown import show_chart
        show_chart(amortization)

    elif choice == "3":
        from charts.payoff_timeline import show_chart
        show_chart(amortization)

    elif choice == "4":
        from charts.progress_bars import show_chart
        show_chart(amortization)

    elif choice == "5":
        from charts.interest_vs_principal import show_chart
        show_chart(amortization)

    else:
        return


# -----------------------------
# VIEW DEBTS
# -----------------------------
def view_debts(debts):
    if not debts:
        console.print("\n[bold red]No debts loaded.[/]\n")
        return

    table = Table(title="Current Debts", show_lines=True)

    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Balance", justify="right", style="green")
    table.add_column("Rate", justify="right", style="magenta")
    table.add_column("Min Payment", justify="right", style="yellow")

    for d in debts:
        table.add_row(
            d.name,
            f"${d.balance:,.2f}",
            f"{d.interest_rate*100:.2f}%",
            f"${d.min_payment:,.2f}"
        )

    console.print()
    console.print(table)
    console.print()


# -----------------------------
# ADD DEBT
# -----------------------------
def add_debt_interactively(debts):
    console.print("\n[bold cyan]Add a New Debt[/]")
    console.print("----------------")

    name = input("Debt name: ")
    balance = float(input("Balance: "))
    rate = float(input("Interest rate (e.g., 0.18 for 18%): "))
    min_payment = float(input("Minimum payment: "))

    debts.append(Debt(name, balance, rate, min_payment))
    console.print(f"\n[bold green]{name} added successfully.[/]\n")


# -----------------------------
# REMOVE DEBT
# -----------------------------
def remove_debt_interactively(debts):
    if not debts:
        console.print("\n[bold red]No debts to remove.[/]\n")
        return

    console.print("\n[bold cyan]Remove a Debt[/]")
    console.print("----------------")

    for i, d in enumerate(debts, start=1):
        console.print(f"{i}. {d.name} (${d.balance})")

    idx = int(input("\nSelect debt to remove: ")) - 1

    if 0 <= idx < len(debts):
        removed = debts[idx]
        confirm = input(f"Are you sure you want to remove {removed.name}? (y/n): ").lower()

        if confirm == "y":
            debts.pop(idx)
            console.print(f"\n[bold green]{removed.name} removed.[/]\n")
        else:
            console.print("\n[bold yellow]Cancelled.[/]\n")
    else:
        console.print("\n[bold red]Invalid selection.[/]\n")


# -----------------------------
# EDIT DEBT
# -----------------------------
def edit_debt(debts):
    if not debts:
        console.print("\n[bold red]No debts to edit.[/]\n")
        return

    console.print("\n[bold cyan]Edit a Debt[/]")
    console.print("-----------")

    for i, d in enumerate(debts, start=1):
        console.print(f"{i}. {d.name} (${d.balance})")

    idx = int(input("\nSelect debt to edit: ")) - 1

    if not (0 <= idx < len(debts)):
        console.print("\n[bold red]Invalid selection.[/]\n")
        return

    debt = debts[idx]

    console.print("\nLeave blank to keep current value.\n")

    new_name = input(f"Name [{debt.name}]: ") or debt.name
    new_balance = input(f"Balance [{debt.balance}]: ")
    new_rate = input(f"Interest rate [{debt.interest_rate}]: ")
    new_min = input(f"Minimum payment [{debt.min_payment}]: ")

    debt.name = new_name
    if new_balance: debt.balance = float(new_balance)
    if new_rate: debt.interest_rate = float(new_rate)
    if new_min: debt.min_payment = float(new_min)

    console.print("\n[bold green]Debt updated.[/]\n")


# -----------------------------
# SORT DEBTS
# -----------------------------
def sort_debts(debts):
    if not debts:
        console.print("\n[bold red]No debts to sort.[/]\n")
        return

    console.print("\n[bold cyan]Sort Debts By:[/]")
    console.print("1. Name")
    console.print("2. Balance")
    console.print("3. Interest Rate")
    console.print("4. Minimum Payment")

    choice = input("Choose: ")

    if choice == "1":
        debts.sort(key=lambda d: d.name.lower())
    elif choice == "2":
        debts.sort(key=lambda d: d.balance)
    elif choice == "3":
        debts.sort(key=lambda d: d.interest_rate)
    elif choice == "4":
        debts.sort(key=lambda d: d.min_payment)
    else:
        console.print("\n[bold red]Invalid choice.[/]\n")
        return

    console.print("\n[bold green]Debts sorted.[/]\n")
    view_debts(debts)


# -----------------------------
# SIMULATION CALLBACK
# -----------------------------
def simulation_callback(debts, snowball_pct, extra_amount, extra_duration):
    months, timeline, amortization = simulate_snowball(
        debts,
        snowball_pct=snowball_pct,
        extra_amount=extra_amount,
        extra_duration=extra_duration
    )

    console.print(f"\n[bold green]Debt-free in {months} months![/]\n")

    # 1. Amortization table FIRST
    print_amortization(amortization)

    # 2. Summary panel SECOND
    print_summary(amortization, months)

    # 3. Payments Remaining THIRD
    console.print("\n[bold cyan]Payments Remaining:[/]")
    for name, payoff_month in timeline:
        console.print(f"{name}: {payoff_month} months remaining")

    # 4. Total payment FOURTH
    total_payment = sum(d.min_payment for d in debts)
    console.print(f"\n[bold yellow]Total payment: ${total_payment:,.2f}[/]\n")

    # 5. Chart menu (DISABLED)
    # chart_choice = input("View charts? (y/n): ").lower()
    # if chart_choice == "y":
    #     chart_menu(amortization)

    # 6. CSV export LAST
    choice = input("Export amortization to CSV? (y/n): ").lower()
    if choice == "y":
        filename = export_amortization_csv(amortization)
        console.print(f"[bold green]Exported to {filename}[/]")


# -----------------------------
# MAIN MENU LOOP
# -----------------------------
def menu():
    debts = []

    while True:
        console.print("\n[bold cyan]Debt Snowball Tool[/]")
        console.print("------------------")
        console.print("1. Load debts from file")
        console.print("2. Add a debt")
        console.print("3. Remove a debt")
        console.print("4. Save debts to file")
        console.print("5. Run simulation")
        console.print("6. View current debts")
        console.print("7. Edit a debt")
        console.print("8. Sort debts")
        console.print("9. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            debts = load_debts()
            console.print("\n[bold green]Debts loaded successfully.[/]\n")

        elif choice == "2":
            add_debt_interactively(debts)

        elif choice == "3":
            remove_debt_interactively(debts)

        elif choice == "4":
            save_debts(debts)
            console.print("\n[bold green]Debts saved successfully.[/]\n")

        elif choice == "5":
            run_simulation_wizard(debts, simulation_callback)

        elif choice == "6":
            view_debts(debts)

        elif choice == "7":
            edit_debt(debts)

        elif choice == "8":
            sort_debts(debts)

        elif choice == "9":
            console.print("\n[bold yellow]Goodbye![/]\n")
            break

        else:
            console.print("\n[bold red]Invalid choice. Try again.[/]\n")
