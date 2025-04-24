# tata_price_app.py
"""
Streamlit app — Tata Motors Passenger Vehicle Price Tool (Mar‑2025)
Steps:
1️⃣ Pick a **car model**
2️⃣ Choose **fuel type** (Petrol / Diesel / CNG / EV)
3️⃣ Choose **transmission** (Manual / Automatic) if available
4️⃣ See **all matching variants** and their ex‑showroom prices
5️⃣ Get instant **EMI + RTO** estimate
6️⃣ Decide if you want an **on‑road price** → calculated with insurance & misc;
   output is tagged **“Subject to Change”**
"""

import streamlit as st
from datetime import date
from math import pow

st.set_page_config(page_title="Tata Price Finder", page_icon="🚘", layout="centered")

st.title("🚘 Tata Motors Price & Finance Estimator")
st.caption("Data: CarWale / Tata Motors • Updated 31 Mar 2025")

# ------------------------------------------------------------------
# Master price list (ex‑showroom, ₹)
# ------------------------------------------------------------------
cars = {
    "Tiago": [
        {"variant": "XE", "fuel": "Petrol", "trans": "Manual", "price": 4_99_000},
        {"variant": "XM", "fuel": "Petrol", "trans": "Manual", "price": 5_70_000},
        {"variant": "XT", "fuel": "Petrol", "trans": "Manual", "price": 6_30_000},
        {"variant": "XZ", "fuel": "Petrol", "trans": "Manual", "price": 6_90_000},
        {"variant": "XZ NRG", "fuel": "Petrol", "trans": "Manual", "price": 7_20_000},
        {"variant": "XZ+", "fuel": "Petrol", "trans": "Manual", "price": 7_29_000},
        {"variant": "XTA", "fuel": "Petrol", "trans": "Automatic", "price": 6_85_000},
        {"variant": "XZA", "fuel": "Petrol", "trans": "Automatic", "price": 7_45_000},
        {"variant": "XZA NRG", "fuel": "Petrol", "trans": "Automatic", "price": 7_75_000},
        {"variant": "XZ iCNG", "fuel": "CNG", "trans": "Manual", "price": 8_74_000},
        {"variant": "XE MR", "fuel": "EV", "trans": "Automatic", "price": 8_00_000},
        {"variant": "XT MR", "fuel": "EV", "trans": "Automatic", "price": 9_00_000},
        {"variant": "XT LR", "fuel": "EV", "trans": "Automatic", "price": 10_14_000},

    ],
    "Tigor": [
        {"variant": "XE", "fuel": "Petrol", "trans": "Manual", "price": 6_30_000},
        {"variant": "XM", "fuel": "Petrol", "trans": "Manual", "price": 6_85_000},
        {"variant": "XZ+", "fuel": "Petrol", "trans": "Manual", "price": 7_90_000},
        {"variant": "XZA+", "fuel": "Petrol", "trans": "Automatic", "price": 8_45_000},
        {"variant": "XZ iCNG", "fuel": "CNG", "trans": "Manual", "price": 8_30_000},
        {"variant": "XZA+ iCNG", "fuel": "CNG", "trans": "Automatic", "price": 9_45_000},
        {"variant": "Tigor.ev XZ+ LR", "fuel": "EV", "trans": "Automatic", "price": 14_55_000},
    ],
    "Altroz": [
        {"variant": "XE", "fuel": "Petrol", "trans": "Manual", "price": 6_65_000},
        {"variant": "XM", "fuel": "Petrol", "trans": "Manual", "price": 7_25_000},
        {"variant": "XZ+ (S) LUX", "fuel": "Petrol", "trans": "Manual", "price": 10_00_000},
        {"variant": "XZA+ (O) (S)", "fuel": "Petrol", "trans": "Automatic", "price": 11_00_000},
        {"variant": "XZ+ (S) LUX CNG", "fuel": "CNG", "trans": "Manual", "price": 10_70_000},
        {"variant": "XZ+ (S) LUX Diesel", "fuel": "Diesel", "trans": "Manual", "price": 11_00_000},
    ],
    "Punch": [
        {"variant": "Pure", "fuel": "Petrol", "trans": "Manual", "price": 6_20_000},
        {"variant": "Adventure", "fuel": "Petrol", "trans": "Manual", "price": 7_17_000},
        {"variant": "Creative+", "fuel": "Petrol", "trans": "Manual", "price": 10_97_000},
        {"variant": "Creative+ AMT", "fuel": "Petrol", "trans": "Automatic", "price": 11_97_000},
        {"variant": "Adventure iCNG", "fuel": "CNG", "trans": "Manual", "price": 9_30_000},
        {"variant": "Punch.ev Empowered+ LR", "fuel": "EV", "trans": "Automatic", "price": 13_99_000},
    ],
    "Nexon": [
        {"variant": "Smart", "fuel": "Petrol", "trans": "Manual", "price": 8_00_000},
        {"variant": "Pure", "fuel": "Petrol", "trans": "Manual", "price": 9_70_000},
        {"variant": "Fearless+ S", "fuel": "Petrol", "trans": "Manual", "price": 14_90_000},
        {"variant": "Smart+  AMT 1.2", "fuel": "Petrol", "trans": "Automatic", "price": 9_60_000},
        {"variant": "Pure+  AMT 1.2", "fuel": "Petrol", "trans": "Automatic", "price": 10_40_000},
        {"variant": "Pure+  S AMT 1.2", "fuel": "Petrol", "trans": "Automatic", "price": 10_69_000},
        {"variant": "Creative  AMT 1.2", "fuel": "Petrol", "trans": "Automatic", "price": 11_70_000},
        {"variant": "Creative +S AMT 1.2", "fuel": "Petrol", "trans": "Automatic", "price": 12_00_000},
        {"variant": "Smart + 1.5", "fuel": "Diesel", "trans": "Manual", "price": 10_00_000},
        {"variant": "Smart + S 1.5", "fuel": "Diesel", "trans": "Manual", "price": 10_30_000},
        {"variant": "Pure + 1.5", "fuel": "Diesel", "trans": "Manual", "price": 11_00_000},
        {"variant": "Pure + S 1.5", "fuel": "Diesel", "trans": "Manual", "price": 11_30_000},
        {"variant": "Creative  1.5", "fuel": "Diesel", "trans": "Manual", "price": 12_40_000},
        {"variant": "Creative +S 1.5", "fuel": "Diesel", "trans": "Manual", "price": 12_69_000},
        {"variant": "Creative +PS DT 1.5", "fuel": "Diesel", "trans": "Manual", "price": 13_69_000},
        {"variant": "Pure + AMT", "fuel": "Diesel", "trans": "Automatic", "price": 11_69_000},
        {"variant": "Crative AMT 1.5", "fuel": "Diesel", "trans": "Automatic", "price": 13_09_000},
        {"variant": "Crative +S AMT 1.5", "fuel": "Diesel", "trans": "Automatic", "price": 13_39_000},
        {"variant": "Crative +PS AMT DT 1.5", "fuel": "Diesel", "trans": "Automatic", "price": 14_39_000},
        {"variant": "Fearless +PS  DT 1.5", "fuel": "Diesel", "trans": "Automatic", "price": 14_69_000},
        {"variant": "Fearless+ S Diesel AMT", "fuel": "Diesel", "trans": "Automatic", "price": 15_39_000},
        {"variant": "Nexon.ev Empowered+ LR", "fuel": "EV", "trans": "Automatic", "price": 17_19_000},
        {"variant": "Nexon.ev Creative + MR", "fuel": "EV", "trans": "Automatic", "price": 12_49_000},
        {"variant": "Nexon.ev Fearless + MR", "fuel": "EV", "trans": "Automatic", "price": 13_79_000},
        {"variant": "Nexon.ev Creative 45", "fuel": "EV", "trans": "Automatic", "price": 14_00_000},
        {"variant": "Nexon.ev Empowered +45", "fuel": "EV", "trans": "Automatic", "price": 17_00_000},

        {"variant": "Nexon.ev Empowered MR", "fuel": "EV", "trans": "Automatic", "price": 14_79_000},




    ],
    "Harrier": [
        {"variant": "Smart", "fuel": "Diesel", "trans": "Manual", "price": 15_00_000},
        {"variant": "Pure", "fuel": "Diesel", "trans": "Manual", "price": 16_85_000},
        {"variant": "Fearless+ Stealth", "fuel": "Diesel", "trans": "Manual", "price": 26_00_000},
        {"variant": "Fearless+ Stealth AT", "fuel": "Diesel", "trans": "Automatic", "price": 26_50_000},
    ],
    "Safari": [
        {"variant": "Smart 7 STR", "fuel": "Diesel", "trans": "Manual", "price": 15_50_000},
        {"variant": "Pure 7 STR", "fuel": "Diesel", "trans": "Manual", "price": 17_35_000},
        {"variant": "Accomplished+", "fuel": "Diesel", "trans": "Manual", "price": 26_75_000},
        {"variant": "Accomplished+ AT", "fuel": "Diesel", "trans": "Automatic", "price": 27_25_000},
    ],
    "Curvv (Indicative)": [
        {"variant": "Curvv Petrol MT", "fuel": "Petrol", "trans": "Manual", "price": 12_50_000},
        {"variant": "Curvv Petrol AT", "fuel": "Petrol", "trans": "Automatic", "price": 13_50_000},
        {"variant": "Curvv Diesel MT", "fuel": "Diesel", "trans": "Manual", "price": 14_50_000},
        {"variant": "Curvv.ev LR", "fuel": "EV", "trans": "Automatic", "price": 22_00_000},
    ],
}

# ------------------------------------------------------------------
# 1️⃣ Select Model
# ------------------------------------------------------------------
model = st.selectbox("Choose model", sorted(cars.keys()))
model_variants = cars[model]

# ------------------------------------------------------------------
# 2️⃣ Fuel type selector (only those available for this model)
# ------------------------------------------------------------------
available_fuels = sorted({v["fuel"] for v in model_variants})
fuel_choice = st.radio("Fuel type", available_fuels, horizontal=True)

variants_by_fuel = [v for v in model_variants if v["fuel"] == fuel_choice]

# ------------------------------------------------------------------
# 3️⃣ Transmission selector
# ------------------------------------------------------------------
avail_trans = sorted({v["trans"] for v in variants_by_fuel})
trans_choice = st.radio("Transmission", avail_trans, horizontal=True)

filtered = [v for v in variants_by_fuel if v["trans"] == trans_choice]

# ------------------------------------------------------------------
# 4️⃣ Variant selector from filtered list
# ------------------------------------------------------------------
variant_labels = [f"{v['variant']} — ₹{v['price']:,.0f}" for v in filtered]
variant_label = st.selectbox("Variant", variant_labels)
selected_variant = filtered[variant_labels.index(variant_label)]
ex_price = selected_variant["price"]

st.success(f"**{model} – {selected_variant['variant']}**  •  Ex‑showroom: ₹{ex_price:,.0f}")

# ------------------------------------------------------------------
# 5️⃣ EMI & RTO calculator (always shown)
# ------------------------------------------------------------------
st.subheader("Finance Estimator")
colA, colB, colC = st.columns(3)
with colA:
    dp_pct = st.slider("Down‑payment %", 0, 100, 10)
with colB:
    int_rate = st.number_input("Interest % p.a.", 1.0, 15.0, 9.0, 0.1)
with colC:
    tenure_yrs = st.slider("Tenure (yrs)", 1, 7, 5)

# RTO slab (Maharashtra private car)
if ex_price < 1_000_000:
    rto_pct = 0.07
elif ex_price <= 2_000_000:
    rto_pct = 0.09
else:
        rto_pct = 0.11
rto_tax = ex_price * rto_pct

loan_amt = ex_price * (100 - dp_pct) / 100
n = tenure_yrs * 12
r = int_rate / (12 * 100)
emi = 0 if loan_amt == 0 else loan_amt * r * pow(1 + r, n) / (pow(1 + r, n) - 1)

st.write(f"**Estimated EMI:** ₹{emi:,.0f}/month   •   **Approx. RTO Tax:** ₹{rto_tax:,.0f}")

# ------------------------------------------------------------------
# 6️⃣ Ask if user wants on‑road calculation
# ------------------------------------------------------------------
want_onroad = st.radio("Would you like to estimate on‑road price?", ("Yes", "No"), horizontal=True)

if want_onroad == "Yes":
    ins_pct = st.number_input("Insurance % of ex‑showroom", 1.0, 5.0, 3.0, 0.1)
    misc_fee = st.number_input("Other charges (₹)", 0, 50_000, 10_000, 1_000)
    insurance = ex_price * ins_pct / 100
    onroad = ex_price + rto_tax + insurance + misc_fee

    st.success(f"**Indicative On‑road Price:** ₹{onroad:,.0f}")
    st.caption("Subject to Change")
else:
    st.info("Thank you!")
