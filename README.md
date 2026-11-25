# Apparel Export Costing (FOB) Calculator

**Roll No:** 25TE065  
**Department:** Textile Engineering  
**Framework:** Streamlit

## Project overview

A Streamlit web application for estimating apparel order costs and garment FOB value. Users enter fabric, trims, stitching, washing, packing, and optional additional charges. The app calculates estimated total order FOB and per-garment FOB in PKR and USD, with a configurable profit margin and exchange rate.

## Features

- Fabric cost input
- Trims cost input
- Stitching cost input
- Washing cost input
- Packing cost input
- Optional other production and FOB/export charges
- Order quantity input
- USD exchange-rate input
- Profit margin calculation
- Total order FOB in PKR and USD
- Per-garment FOB in PKR and USD
- Detailed cost breakdown
- Downloadable CSV costing report
- Costing guide with formulas

## Project files

- `app.py` — Main Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

## Run locally

1. Install Python 3.9 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start the application:

```bash
streamlit run app.py
```

Streamlit will display a local URL, usually `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload `app.py`, `requirements.txt`, and `README.md`.
3. Sign in to Streamlit Community Cloud using GitHub.
4. Create an app and select your repository and `app.py`.
5. Click Deploy.

## Calculation method

```text
Production Cost = Fabric + Trims + Stitching + Washing + Packing + Other Costs
Cost Before Profit = Production Cost + Other FOB Charges
Profit = Cost Before Profit × Profit Margin / 100
Total FOB (PKR) = Cost Before Profit + Profit
FOB per Garment = Total FOB / Order Quantity
Total FOB (USD) = Total FOB (PKR) / Exchange Rate
```

## Important note

This is a simplified educational costing tool. Commercial export quotations can involve additional costs, taxes, commissions, adjustments, freight-related terms, and buyer-specific requirements. Confirm the applicable Incoterms and cost scope before using any result as a commercial quotation.
