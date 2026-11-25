import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Apparel Export Costing (FOB) Calculator",
    page_icon="👕",
    layout="wide"
)

st.markdown("""
<style>
.hero {
    padding: 1.35rem 1.5rem;
    border-radius: 16px;
    background: linear-gradient(115deg, #153b5b, #147d83);
    color: white;
    margin-bottom: 1.2rem;
}
.hero h1 { color: white; margin: 0; }
.hero p { color: #e7f5f5; margin: .45rem 0 0 0; }
div[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,.25);
    padding: 12px;
    border-radius: 12px;
}
</style>
<div class="hero">
<h1>👕 Apparel Export Costing (FOB) Calculator</h1>
<p>Calculate garment production costs, add profit, and estimate FOB value in PKR and USD.</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("👕 Apparel Costing")
page = st.sidebar.radio("Navigation", ["Cost Calculator", "Costing Guide", "About"])
st.sidebar.divider()
st.sidebar.markdown("**Project Details**")
st.sidebar.write("Roll No: 25TE065")
st.sidebar.write("Department: Textile Engineering")

def money(value, currency="PKR"):
    return f"{currency} {value:,.2f}"

if page == "Cost Calculator":
    st.subheader("Order Information")
    info1, info2, info3 = st.columns(3)
    with info1:
        garment = st.text_input("Garment name / style", "Basic T-Shirt")
    with info2:
        order_qty = st.number_input("Order quantity (pieces)", min_value=1, value=1000, step=100)
    with info3:
        exchange_rate = st.number_input("USD exchange rate (PKR per USD)", min_value=0.01, value=280.0, step=1.0, format="%.2f")

    st.divider()
    st.subheader("Production Cost Inputs")
    st.caption("Enter the total cost for the complete order in PKR. If you have a per-piece cost, multiply it by the order quantity.")

    left, right = st.columns(2)
    with left:
        st.markdown("#### Material and processing")
        fabric = st.number_input("Total fabric cost (PKR)", min_value=0.0, value=150000.0, step=1000.0)
        trims = st.number_input("Total trims cost (PKR)", min_value=0.0, value=25000.0, step=500.0)
        stitching = st.number_input("Total stitching cost (PKR)", min_value=0.0, value=40000.0, step=500.0)
    with right:
        st.markdown("#### Finishing and export preparation")
        washing = st.number_input("Total washing cost (PKR)", min_value=0.0, value=15000.0, step=500.0)
        packing = st.number_input("Total packing cost (PKR)", min_value=0.0, value=10000.0, step=500.0)
        other = st.number_input("Other costs (PKR)", min_value=0.0, value=0.0, step=500.0,
                                help="Optional additional order costs, such as testing or documentation.")

    st.divider()
    st.subheader("FOB and Profit Settings")
    p1, p2 = st.columns(2)
    with p1:
        profit_margin = st.number_input("Profit margin (%)", min_value=0.0, value=10.0, step=0.5)
    with p2:
        extra_fob = st.number_input("Other FOB / export charges (PKR)", min_value=0.0, value=0.0, step=500.0,
                                    help="Optional charges you want to include in the FOB calculation.")

    production_cost = fabric + trims + stitching + washing + packing + other
    total_cost = production_cost + extra_fob
    profit = total_cost * profit_margin / 100
    fob_total_pkr = total_cost + profit
    fob_per_piece_pkr = fob_total_pkr / order_qty
    fob_total_usd = fob_total_pkr / exchange_rate if exchange_rate else 0
    fob_per_piece_usd = fob_total_usd / order_qty

    st.divider()
    st.subheader("Cost Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Production Cost", money(production_cost))
    m2.metric("Total Cost incl. FOB charges", money(total_cost))
    m3.metric("Profit Amount", money(profit))
    m4.metric("Profit Margin", f"{profit_margin:.2f}%")

    st.subheader("Estimated FOB Price")
    a, b = st.columns(2)
    a.metric("FOB Price per Garment (PKR)", money(fob_per_piece_pkr))
    b.metric("FOB Price per Garment (USD)", money(fob_per_piece_usd))
    c, d = st.columns(2)
    c.metric("Total Order FOB (PKR)", money(fob_total_pkr))
    d.metric("Total Order FOB (USD)", money(fob_total_usd))

    st.info("Calculation method: Total production and entered FOB charges are added first. Profit is then calculated as a percentage of that cost. USD values are estimated using the exchange rate entered above.")

    rows = [
        ["Fabric", fabric],
        ["Trims", trims],
        ["Stitching", stitching],
        ["Washing", washing],
        ["Packing", packing],
        ["Other costs", other],
        ["Other FOB / export charges", extra_fob],
        ["Profit", profit],
        ["Total estimated FOB", fob_total_pkr],
    ]
    breakdown = pd.DataFrame(rows, columns=["Cost Head", "Amount (PKR)"])
    breakdown["Cost per Garment (PKR)"] = breakdown["Amount (PKR)"] / order_qty
    breakdown["Amount (USD)"] = breakdown["Amount (PKR)"] / exchange_rate

    st.subheader("Detailed Cost Breakdown")
    st.dataframe(
        breakdown.style.format({
            "Amount (PKR)": "{:,.2f}",
            "Cost per Garment (PKR)": "{:,.2f}",
            "Amount (USD)": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    report = breakdown.copy()
    report.insert(0, "Garment / Style", garment)
    report.insert(1, "Order Quantity", order_qty)
    report.insert(2, "Exchange Rate (PKR/USD)", exchange_rate)
    csv = report.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Download Costing Report (CSV)",
        data=csv,
        file_name="apparel_export_costing_report.csv",
        mime="text/csv",
        use_container_width=True
    )

elif page == "Costing Guide":
    st.subheader("How the calculator works")
    st.write("Enter the total costs for your order. The application adds the cost heads and estimates the FOB value after adding the selected profit margin.")
    st.markdown("""
    | Cost head | What to include |
    |---|---|
    | Fabric | Main fabric consumed for the order |
    | Trims | Buttons, zippers, labels, thread and accessories |
    | Stitching | Garment sewing / stitching charges |
    | Washing | Garment washing and related processing |
    | Packing | Poly bags, cartons, tags and packing materials |
    | Other costs | Optional extra production costs |
    | FOB / export charges | Other order charges you choose to include |
    """)
    st.subheader("Formulas")
    st.code(
        "Production Cost = Fabric + Trims + Stitching + Washing + Packing + Other Costs\n"
        "Cost Before Profit = Production Cost + Other FOB Charges\n"
        "Profit = Cost Before Profit × Profit Margin / 100\n"
        "Total FOB (PKR) = Cost Before Profit + Profit\n"
        "FOB per Garment = Total FOB / Order Quantity\n"
        "FOB (USD) = FOB (PKR) / Exchange Rate",
        language="text"
    )
    st.warning("This is a simplified educational costing calculator. Actual export quotations may include additional costs, adjustments, taxes, commissions, freight-related terms, and buyer-specific requirements. Confirm the applicable Incoterms and cost scope before using a quotation commercially.")

else:
    st.subheader("About This Project")
    st.write("**Application:** Apparel Export Costing (FOB) Calculator")
    st.write("**Student Roll No:** 25TE065")
    st.write("**Department:** Textile Engineering")
    st.write("**Framework:** Python + Streamlit")
    st.markdown("""
    **Objective**

    To help textile and apparel students estimate garment order costs by entering fabric, trims, stitching, washing, and packing costs. The application calculates an estimated FOB value in Pakistani Rupees and US Dollars.

    **Included features**
    - Cost input for fabric, trims, stitching, washing, and packing
    - Optional additional costs and FOB charges
    - Order quantity and exchange-rate input
    - Profit margin calculation
    - Per-garment and total-order FOB estimate in PKR and USD
    - Detailed cost breakdown
    - CSV report download
    """)
    st.caption("Prepared for Roll No. 25TE065 | Textile Engineering")

st.divider()
st.caption("Apparel Export Costing (FOB) Calculator • Roll No. 25TE065")
