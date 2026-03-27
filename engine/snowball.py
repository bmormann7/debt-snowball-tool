from copy import deepcopy
from datetime import datetime

def simulate_snowball(
    debts,
    snowball_pct=1.0,
    extra_amount=None,
    extra_duration=None
):
    """
    debts: list of Debt objects (originals are not modified)
    snowball_pct: decimal (1.0 = 100%, 0.5 = 50%, etc.)
    extra_amount: float or None
    extra_duration: int (months) or "life_of_smallest" or None

    Returns:
        months_to_debt_free,
        payoff_timeline (list of tuples: (debt_name, months_remaining)),
        amortization (list of dict rows)
    """

    # Work on a deep copy so original debts remain untouched
    debts = deepcopy(debts)

    # Sort smallest to largest by balance
    debts.sort(key=lambda d: d.balance)
    original_balances = {d.name: d.balance for d in debts}

    amortization = []
    month_counter = 1
    snowball = 0.0  # grows as debts are paid off
    extra_months_used = 0  # track duration for fixed extra payments

    # Track payoff timeline
    payoff_timeline = {d.name: None for d in debts}

    # -----------------------------
    # Calendar date tracking
    # -----------------------------
    start = datetime.now()
    current_month = start.month
    current_year = start.year

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    # Continue until all debts are paid
    while any(d.balance > 0 for d in debts):

        # Identify smallest active debt
        active_debts = [d for d in debts if d.balance > 0]
        active_debts.sort(key=lambda d: d.balance)
        smallest = active_debts[0]

        # Determine extra payment for this month
        extra_this_month = 0.0

        if extra_amount is not None:
            if extra_duration == "life_of_smallest":
                # Apply extra only while smallest debt exists
                extra_this_month = extra_amount
            elif isinstance(extra_duration, int):
                if extra_months_used < extra_duration:
                    extra_this_month = extra_amount
                    extra_months_used += 1

        # Process each debt
        for d in active_debts:
            starting_balance = d.balance

            # Monthly interest
            interest = d.balance * (d.interest_rate / 12)

            # Base payment = minimum + snowball (only for smallest debt)
            if d is smallest:
                payment = d.min_payment + snowball
                payment += extra_this_month
            else:
                payment = d.min_payment

            # Prevent overpayment
            total_payment = min(payment, d.balance + interest)

            # Apply payment
            principal_payment = total_payment - interest
            d.balance -= principal_payment

            # Format date label (e.g., "Mar 26")
            date_label = f"{month_names[current_month - 1]} {str(current_year)[-2:]}"

            # Record amortization row
            progress = 1 - (d.balance / original_balances[d.name]) if original_balances[d.name] > 0 else 1
            amortization.append({
                "date": date_label,
                "debt": d.name,
                "starting_balance": starting_balance,
                "interest_added": interest,
                "payment": total_payment - extra_this_month,
                "extra": extra_this_month if d is smallest else 0.0,
                "ending_balance": d.balance,
                "progress": progress
            })

            # If this debt is now paid off
            if d.balance <= 0 and payoff_timeline[d.name] is None:
                payoff_timeline[d.name] = month_counter

                # Add rollover to snowball
                rollover = d.min_payment * snowball_pct
                snowball += rollover

                # If extra was for life of smallest loan, add extra to snowball
                if d is smallest and extra_duration == "life_of_smallest" and extra_amount:
                    snowball += extra_amount
                    extra_amount = None  # stop extra payments

        # Advance calendar month
        current_month += 1
        if current_month > 12:
            current_month = 1
            current_year += 1

        month_counter += 1

    # Convert payoff timeline to ordered list
    ordered_timeline = []
    for d in debts:
        ordered_timeline.append((d.name, payoff_timeline[d.name]))

    return month_counter - 1, ordered_timeline, amortization
