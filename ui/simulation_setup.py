from rich.console import Console

console = Console()

# ---------------------------------------------------------
# Comparison Function (Snowball vs Avalanche)
# ---------------------------------------------------------
def compare_strategies(debts, snowball_pct, extra_amount, extra_duration):
    from engine.snowball import simulate_snowball

    # Run Snowball
    s_months, s_timeline, s_amort = simulate_snowball(
        debts,
        snowball_pct=snowball_pct,
        extra_amount=extra_amount,
        extra_duration=extra_duration,
        mode="snowball"
    )

    # Run Avalanche
    a_months, a_timeline, a_amort = simulate_snowball(
        debts,
        snowball_pct=snowball_pct,
        extra_amount=extra_amount,
        extra_duration=extra_duration,
        mode="avalanche"
    )

    # Helper to compute summary stats
    def summarize(amort, months):
        total_paid = sum(row["payment"] + row["extra"] for row in amort)
        total_interest = sum(row["interest_added"] for row in amort)
        total_principal = sum(row["starting_balance"] - row["ending_balance"] for row in amort)
        avg_payment = total_paid / months
        highest_payment = max(row["payment"] + row["extra"] for row in amort)
        lowest_payment = min(row["payment"] + row["extra"] for row in amort)
        return {
            "months": months,
            "total_paid": total_paid,
            "principal": total_principal,
            "interest": total_interest,
            "avg": avg_payment,
            "high": highest_payment,
            "low": lowest_payment
        }

    s = summarize(s_amort, s_months)
    a = summarize(a_amort, a_months)

    # Alignment helper
    def pad(text, width):
        return f"{text:<{width}}"

    left_width = 32
    right_width = 32

    # Build aligned output
    output = (
f"""
──────────────────────────────────────────────────────────────────────────────
                           AVALANCHE                     |       SNOWBALL
──────────────────────────────────────────────────────────────────────────────
 Total Months:           {pad(str(a['months']), left_width)} | {pad(str(s['months']), right_width)}
 Total Paid:             {pad(f"${a['total_paid']:,.2f}", left_width)} | {pad(f"${s['total_paid']:,.2f}", right_width)}
 Total Principal:        {pad(f"${a['principal']:,.2f}", left_width)} | {pad(f"${s['principal']:,.2f}", right_width)}
 Total Interest:         {pad(f"${a['interest']:,.2f}", left_width)} | {pad(f"${s['interest']:,.2f}", right_width)}
 Total Extra Applied:    {pad("$0.00", left_width)} | {pad("$0.00", right_width)}
 Avg Monthly Payment:    {pad(f"${a['avg']:,.2f}", left_width)} | {pad(f"${s['avg']:,.2f}", right_width)}
 Highest Payment:        {pad(f"${a['high']:,.2f}", left_width)} | {pad(f"${s['high']:,.2f}", right_width)}
 Lowest Payment:         {pad(f"${a['low']:,.2f}", left_width)} | {pad(f"${s['low']:,.2f}", right_width)}
──────────────────────────────────────────────────────────────────────────────

 Payments Remaining (by debt)
──────────────────────────────────────────────────────────────────────────────
"""
    )

    # Pair debts side-by-side
    max_len = max(len(a_timeline), len(s_timeline))
    for i in range(max_len):
        left = f"{a_timeline[i][0]}: {a_timeline[i][1]} months" if i < len(a_timeline) else ""
        right = f"{s_timeline[i][0]}: {s_timeline[i][1]} months" if i < len(s_timeline) else ""
        output += f" {pad(left, left_width)} | {pad(right, right_width)}\n"

    output += (
f"""
──────────────────────────────────────────────────────────────────────────────

 Total Payment This Month
──────────────────────────────────────────────────────────────────────────────
 Avalanche:   ${a['high']:,.2f}
 Snowball:    ${s['high']:,.2f}
──────────────────────────────────────────────────────────────────────────────
"""
    )

    console.print(output)


# ---------------------------------------------------------
# Simulation Wizard
# ---------------------------------------------------------
def run_simulation_wizard(debts, simulate_callback):
    """
    debts: list of Debt objects
    simulate_callback: function to call when user selects 'Run simulation'
                       simulate_callback(debts, snowball_pct, extra_amount, extra_duration, mode)
    """

    # Remembered settings
    snowball_pct = 1.0
    extra_amount = None
    extra_duration = None
    mode = "snowball"

    while True:
        console.print("\n[bold cyan]Simulation Setup[/]")
        console.print("----------------")
        console.print(f"1. Set snowball rollover percentage (current: {int(snowball_pct * 100)}%)")

        if extra_amount is None:
            console.print("2. Add extra payment to smallest debt (current: none)")
        else:
            if extra_duration == "life_of_smallest":
                console.print(f"2. Add extra payment to smallest debt (current: ${extra_amount} for life of smallest loan)")
            else:
                console.print(f"2. Add extra payment to smallest debt (current: ${extra_amount} for {extra_duration} months)")

        console.print("3. Clear extra payments")
        console.print(f"4. Set payoff method (current: {mode.upper()})")
        console.print("5. Compare Snowball vs Avalanche")
        console.print("6. Run simulation")
        console.print("7. Back")

        choice = input("\nChoose an option: ")

        # 1. Set snowball rollover %
        if choice == "1":
            pct = input("\nEnter snowball rollover percentage (e.g., 100 for full): ")
            try:
                snowball_pct = float(pct) / 100
                console.print(f"[bold green]Snowball rollover set to {pct}%[/]\n")
            except ValueError:
                console.print("[bold red]Invalid percentage.[/]\n")

        # 2. Extra payment setup
        elif choice == "2":
            yn = input("\nApply extra money to smallest debt? (y/n): ").lower()
            if yn != "y":
                console.print("[yellow]Extra payment cancelled.[/]\n")
                continue

            amt = input("Enter extra amount: ")
            try:
                extra_amount = float(amt)
            except ValueError:
                console.print("[bold red]Invalid amount.[/]\n")
                continue

            dur = input("For how long? (enter number of months or 0 for 'life of smallest loan'): ")
            try:
                dur_val = int(dur)
                if dur_val == 0:
                    extra_duration = "life_of_smallest"
                else:
                    extra_duration = dur_val
                console.print("[bold green]Extra payment settings updated.[/]\n")
            except ValueError:
                console.print("[bold red]Invalid duration.[/]\n")

        # 3. Clear extra payments
        elif choice == "3":
            extra_amount = None
            extra_duration = None
            console.print("[bold yellow]Extra payments cleared.[/]\n")

        # 4. Set payoff method
        elif choice == "4":
            console.print("\n[bold cyan]Choose payoff method:[/]")
            console.print("1. Snowball (smallest balance first)")
            console.print("2. Avalanche (highest interest rate first)")
            m = input("Choose: ").strip()

            if m == "1":
                mode = "snowball"
            elif m == "2":
                mode = "avalanche"
            else:
                console.print("[yellow]Invalid choice. Keeping current method.[/]\n")

            console.print(f"[bold green]Payoff method set to {mode.upper()}[/]\n")

        # 5. Compare Snowball vs Avalanche
        elif choice == "5":
            compare_strategies(debts, snowball_pct, extra_amount, extra_duration)

        # 6. Run simulation
        elif choice == "6":
            simulate_callback(
                debts,
                snowball_pct,
                extra_amount,
                extra_duration,
                mode
            )

        # 7. Back
        elif choice == "7":
            return

        else:
            console.print("[bold red]Invalid choice.[/]\n")
