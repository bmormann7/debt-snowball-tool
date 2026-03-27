import streamlit as st
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta

from storage.file_io import load_debts, save_debts
from models.debt import Debt
from engine.snowball import simulate_snowball
from ui.summary import print_summary

st.set_page_config(page_title="Debt Snowball Tool", layout="wide")

st.title("Debt Snowball Tool")

# ---------------------------------------------------------
# LOAD DEBTS
# ---------------------------------------------------------
if "debts" not in st.session_state:
    st.session_state.debts = load_debts()

debts = st.session_state.debts

# ---------------------------------------------------------
# CURRENT DEBTS TABLE
# ---------------------------------------------------------
st.subheader("Current Debts")

if debts:
    st.table([
        {
            "Name": d.name,
            "Balance": f"${d.balance:,.2f}",
            "Rate": f"{d.interest_rate*100:.2f}%",
            "Min Payment": f"${d.min_payment:,.2f}"
        }
        for d in debts
    ])
else:
    st.info("No debts loaded yet.")

st.markdown("---")

# ---------------------------------------------------------
# ADD A NEW DEBT
# ---------------------------------------------------------
st.subheader("Add a New Debt")

with st.form("add_debt_form"):
    name = st.text_input("Debt Name")
    balance = st.number_input("Balance", min_value=0.0, step=0.01)
    rate = st.number_input("Interest Rate (e.g., 0.18 for 18%)", min_value=0.0, step=0.01)
    min_payment = st.number_input("Minimum Payment", min_value=0.0, step=0.01)

    submitted = st.form_submit_button("Add Debt")

    if submitted:
        if name and balance > 0 and min_payment > 0:
            debts.append(Debt(name, balance, rate, min_payment))
            save_debts(debts)
            st.success(f"Added {name}")
            st.experimental_rerun()
        else:
            st.error("Please fill out all fields.")

st.markdown("---")

# ---------------------------------------------------------
# REMOVE A DEBT
# ---------------------------------------------------------
st.subheader("Remove a Debt")

if debts:
    debt_names = [d.name for d in debts]
    to_remove = st.selectbox("Select a debt to remove", [""] + debt_names)

    if to_remove and st.button("Remove Selected Debt"):
        st.session_state.debts = [d for d in debts if d.name != to_remove]
        save_debts(st.session_state.debts)
        st.success(f"Removed {to_remove}")
        st.experimental_rerun()
else:
    st.info("No debts to remove.")

st.markdown("---")

# ---------------------------------------------------------
# RUN SIMULATION
# ---------------------------------------------------------
st.header("Run Simulation")

if debts:

    snowball_pct = st.slider(
        "Snowball Percentage",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05
    )

    extra_amount = st.number_input(
        "Extra Monthly Payment",
        min_value=0.0,
        value=0.0,
        step=10.0
    )

    extra_duration = st.number_input(
        "Extra Payment Duration (months)",
        min_value=0,
        value=0,
        step=1
    )

    if st.button("Run Simulation"):
        months, timeline, amortization = simulate_snowball(
            debts,
            snowball_pct=snowball_pct,
            extra_amount=extra_amount,
            extra_duration=extra_duration
        )

        st.success(f"🎉 Debt-free in **{months} months**!")

        # Payments Remaining
        st.subheader("Payments Remaining")
        for name, payoff_month in timeline:
            st.write(f"**{name}**: {payoff_month} months remaining")

        total_payment = sum(d.min_payment for d in debts)
        st.write(f"**Total Minimum Monthly Payment:** ${total_payment:,.2f}")

        st.markdown("---")

        # Summary
        st.subheader("Summary")
        summary_text = print_summary(amortization, months, return_text=True)
        st.markdown(summary_text)

        st.markdown("---")

        # ---------------------------------------------------------
        # AMORTIZATION TABLE
        # ---------------------------------------------------------
        st.subheader("Amortization Table")

        df = pd.DataFrame(amortization)

        # Add month index
        df["Month"] = df.index + 1

        # Generate Month/Year dates
        today = date.today().replace(day=1)
        df["Date"] = df["Month"].apply(lambda m: today + relativedelta(months=m - 1))
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%b %Y")

        # Convert progress to percent string
        df["Progress"] = (df["progress"] * 100).round(0).astype(int).astype(str) + "%"

        # Progress bar (20 blocks)
        df["Progress Bar"] = df["progress"].apply(
            lambda p: "█" * int((p * 100) / 5) + "░" * (20 - int((p * 100) / 5))
        )

        # Rename columns
        df = df.rename(columns={
            "debt": "Debt Name",
            "starting_balance": "Start Balance",
            "interest_added": "Interest",
            "payment": "Payment",
            "extra": "Extra Payment",
            "ending_balance": "End Balance"
        })

        # Format money columns
        money_cols = ["Start Balance", "Interest", "Payment", "Extra Payment", "End Balance"]
        for col in money_cols:
            df[col] = df[col].astype(float).apply(lambda x: f"${x:,.2f}")

        # Reorder columns
        df = df[[
            "Date", "Debt Name", "Start Balance", "Interest", "Payment",
            "Extra Payment", "End Balance", "Progress", "Progress Bar"
        ]]

        # Color styling
        def style_table(s):
            styles = pd.DataFrame("color: black;", index=s.index, columns=s.columns)

            styles["Date"] = "background-color: #cce5ff; color: black;"
            styles["Debt Name"] = "background-color: #ffffff; color: black;"
            styles["Start Balance"] = "background-color: #fff3cd; color: black;"
            styles["Interest"] = "background-color: #e2ccff; color: black;"
            styles["Payment"] = "background-color: #d4edda; color: black;"
            styles["Extra Payment"] = "background-color: #b3d1ff; color: black;"
            styles["End Balance"] = "background-color: #f8d7da; color: black;"

            # Progress + Progress Bar backgrounds
            styles["Progress"] = "background-color: #f0f0f0; color: black;"
            styles["Progress Bar"] = "background-color: #f0f0f0; color: black;"

            # Highlight final payment rows
            final_rows = s["End Balance"] == "$0.00"
            styles.loc[final_rows, :] = "background-color: #c6f6c6; color: black;"

            return styles

        styled_df = df.style.apply(style_table, axis=None)

        st.dataframe(styled_df, use_container_width=True)

        # ---------------------------------------------------------
        # DOWNLOADS
        # ---------------------------------------------------------
        st.markdown("### Download Results")

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="amortization.csv",
            mime="text/csv"
        )

        excel_writer = pd.ExcelWriter("amortization.xlsx", engine="xlsxwriter")
        df.to_excel(excel_writer, index=False, sheet_name="Amortization")
        excel_writer.close()

        with open("amortization.xlsx", "rb") as f:
            st.download_button(
                label="Download Excel",
                data=f,
                file_name="amortization.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

else:
    st.info("Add at least one debt to run a simulation.")
