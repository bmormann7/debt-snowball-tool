import plotly.express as px
import pandas as pd
import webbrowser
import tempfile

def show_chart(amortization):
    df = pd.DataFrame(amortization)

    # Parse month/day strings like "Mar 26"
    df["parsed_md"] = pd.to_datetime(df["date"], format="%b %d", errors="coerce")

    # Number of debts = number of rows per month
    num_debts = df["debt"].nunique()

    # Compute the true month index
    df["month_index"] = df.index // num_debts

    # Assign year based on month index
    df["year"] = 2026 + (df["month_index"] // 12)

    # Combine parsed month/day with synthetic year
    df["date"] = df.apply(
        lambda row: row["parsed_md"].replace(year=row["year"]) if pd.notnull(row["parsed_md"]) else None,
        axis=1
    )

    # ⭐ FIX: Only one point per debt per month
    df_grouped = (
        df.groupby(["month_index", "debt"])
          .agg({"date": "last", "ending_balance": "last"})
          .reset_index()
    )

    fig = px.line(
        df_grouped,
        x="date",
        y="ending_balance",
        color="debt",
        title="Balance Over Time",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Balance ($)",
        hovermode="x unified"
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        fig.write_html(f.name)
        webbrowser.open(f.name)
