from rich.console import Console
from rich.table import Table

console = Console()

def run_simulation_wizard(debts, simulate_callback):
    """
    debts: list of Debt objects
    simulate_callback: function to call when user selects 'Run simulation'
                       simulate_callback(debts, snowball_pct, extra_amount, extra_duration)
    """

    # -----------------------------
    # Simulation settings (remembered while in wizard)
    # -----------------------------
    snowball_pct = 1.0  # default 100%
    extra_amount = None
    extra_duration = None  # None, int, or "life_of_smallest"

    while True:
        console.print("\n[bold cyan]Simulation Setup[/]")
        console.print("----------------")

        # Display current settings
        console.print(f"1. Set snowball rollover percentage "
                      f"(current: {int(snowball_pct * 100)}%)")

        if extra_amount is None:
            console.print("2. Add extra payment to smallest debt (current: none)")
        else:
            if extra_duration == "life_of_smallest":
                console.print(f"2. Add extra payment to smallest debt "
                              f"(current: ${extra_amount} for life of smallest loan)")
            else:
                console.print(f"2. Add extra payment to smallest debt "
                              f"(current: ${extra_amount} for {extra_duration} months)")

        console.print("3. Clear extra payments")
        console.print("4. Run simulation")
        console.print("5. Back")

        choice = input("\nChoose an option: ")

        # -----------------------------
        # 1. Set snowball rollover %
        # -----------------------------
        if choice == "1":
            pct = input("\nEnter snowball rollover percentage (e.g., 100 for full): ")
            try:
                pct_val = float(pct)
                snowball_pct = pct_val / 100
                console.print(f"[bold green]Snowball rollover set to {pct_val}%[/]\n")
            except ValueError:
                console.print("[bold red]Invalid percentage.[/]\n")

        # -----------------------------
        # 2. Extra payment setup
        # -----------------------------
        elif choice == "2":
            yn = input("\nApply extra money to smallest debt? (y/n): ").lower()
            if yn != "y":
                console.print("[yellow]Extra payment cancelled.[/]\n")
                continue

            amt = input("Enter extra amount: ")
            try:
                amt_val = float(amt)
            except ValueError:
                console.print("[bold red]Invalid amount.[/]\n")
                continue

            dur = input("For how long? (enter number of months or 0 for 'life of smallest loan'): ")

            try:
                dur_val = int(dur)
                if dur_val < 0:
                    raise ValueError

                if dur_val == 0:
                    extra_duration = "life_of_smallest"
                else:
                    extra_duration = dur_val

                extra_amount = amt_val
                console.print("[bold green]Extra payment settings updated.[/]\n")

            except ValueError:
                console.print("[bold red]Invalid duration.[/]\n")

        # -----------------------------
        # 3. Clear extra payments
        # -----------------------------
        elif choice == "3":
            extra_amount = None
            extra_duration = None
            console.print("[bold yellow]Extra payments cleared.[/]\n")

        # -----------------------------
        # 4. Run simulation
        # -----------------------------
        elif choice == "4":
            simulate_callback(
                debts,
                snowball_pct,
                extra_amount,
                extra_duration
            )
            # After simulation, stay in wizard with remembered settings

        # -----------------------------
        # 5. Back to main menu
        # -----------------------------
        elif choice == "5":
            return

        else:
            console.print("[bold red]Invalid choice.[/]\n")
