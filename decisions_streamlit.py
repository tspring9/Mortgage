import streamlit as st

# === Helper Function ===
def future_value(principal, rate, years):
    return principal * ((1 + rate) ** years)

# === Streamlit App ===
st.set_page_config(page_title="Mortgage Comparison Tool", layout="centered")
st.title("🏠 Mortgage Comparison Tool")

# === Input Section ===
st.header("📋 New Mortgage Info")
house_price = st.number_input("House Price", value=600000.0)
down_payment = st.number_input("Down Payment", value=100000.0)
interest_rate = st.number_input("Annual Interest Rate (e.g. 0.07 = 7%)", value=0.07)
property_tax = st.number_input("Annual Property Tax", value=8420.0)
income = st.number_input("Household Income (Annual)", value=228287.21)

st.header("📋 Current Mortgage Info")
current_balance = st.number_input("Current Principal Balance", value=111518.09)
remaining_payments = st.number_input("Remaining Payments", value=314, format="%d")
current_payment = st.number_input("Current Monthly Payment", value=878.60)

if st.button("🔍 Compare Mortgages"):
    # === Calculations ===
    loan_amount = house_price - down_payment
    total_payments = 30 * 12
    monthly_interest = interest_rate / 12
    monthly_tax = property_tax / 12

    if monthly_interest == 0:
        monthly_payment = loan_amount / total_payments
    else:
        monthly_payment = (
            loan_amount * (monthly_interest * (1 + monthly_interest) ** total_payments)
        ) / ((1 + monthly_interest) ** total_payments - 1)

    true_monthly_payment = monthly_payment + monthly_tax
    total_payment_sum = monthly_payment * total_payments

    # === Income Analysis ===
    monthly_income_pre_tax = income / 12
    monthly_income_post_tax = monthly_income_pre_tax * 0.70
    payment_ratio = true_monthly_payment / monthly_income_post_tax

    # === Time Horizon Comparison ===
    horizons = {"1 Year": 12, "3 Years": 36, "5 Years": 60, "20 Years": 240}
    st.subheader("📊 Payment Comparisons")

    for label, months in horizons.items():
        current_total = min(months, remaining_payments) * current_payment
        new_total = months * true_monthly_payment
        diff = new_total - current_total
        invested_value = future_value(down_payment, 0.08, months / 12)

        st.markdown(f"**{label}**")
        st.write(f"Current Total Payments: ${current_total:,.2f}")
        st.write(f"New Total Payments: ${new_total:,.2f}")
        st.write(f"Difference: ${diff:,.2f}")
        st.write(f"Down Payment Value if Invested @8%: ${invested_value:,.2f}")
        st.divider()

    # === Summary
    st.subheader("📌 Summary")
    st.write(f"Loan Amount: ${loan_amount:,.2f}")
    st.write(f"Monthly Mortgage Payment (P&I): ${monthly_payment:,.2f}")
    st.write(f"Monthly Property Tax: ${monthly_tax:,.2f}")
    st.write(f"**True Monthly Payment (All-in): ${true_monthly_payment:,.2f}**")
    st.write(f"Total Loan Cost (Excl. Taxes): ${total_payment_sum:,.2f}")
    st.write(f"Monthly Post-Tax Income: ${monthly_income_post_tax:,.2f}")
    st.write(f"Affordability Ratio: **{payment_ratio:.2%}**")

