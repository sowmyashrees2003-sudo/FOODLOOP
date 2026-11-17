import streamlit as st
import pandas as pd

from database import (
    create_table,
    save_donation,
    get_donations,
    update_donation_status
)

from ai_matching import match_ngos
from ngo import ngo_dashboard
from volunteer import volunteer_dashboard


st.set_page_config(
    page_title="FOODLOOP",
    page_icon="🍱",
    layout="wide"
)
# FOODLOOP CUSTOM DESIGN
st.markdown("""
<style>

/* ===== PAGE ===== */
.stApp {
    background-color: #f5f8f6 !important;
    color: #26352d !important;
}

/* ===== ALL NORMAL TEXT ===== */
.stApp p,
.stApp label,
.stApp li,
.stMarkdown,
.stCaption,
.stText,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #26352d !important;
}

/* ===== HEADINGS ===== */
h1, h2, h3, h4, h5, h6 {
    color: #176b45 !important;
    font-weight: 800 !important;
}

/* ===== BUTTONS ===== */
.stButton button,
.stDownloadButton button,
button[kind="primary"],
button[kind="secondary"] {
    background-color: #176b45 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

.stButton button *,
.stDownloadButton button * {
    color: #ffffff !important;
}

/* ===== TEXT INPUTS ===== */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background-color: #ffffff !important;
    color: #222222 !important;
    border: 1px solid #9ab9a3 !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #777777 !important;
}

/* ===== FORM LABELS ===== */
.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label,
.stTimeInput label,
.stDateInput label {
    color: #17452e !important;
    font-weight: 700 !important;
}

/* ===== DROPDOWNS ===== */
.stSelectbox div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #222222 !important;
}

[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[role="listbox"] *,
[role="option"] {
    color: #222222 !important;
}

/* ===== SUCCESS / INFO / WARNING BOXES ===== */
div[data-testid="stAlert"] {
    background-color: #e8f5e9 !important;
    border: 1px solid #a5c9ae !important;
    border-radius: 10px !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span {
    color: #17452e !important;
    font-weight: 600 !important;
}

/* ===== METRIC CARDS ===== */
div[data-testid="stMetric"] {
    background-color: #ffffff !important;
    padding: 18px !important;
    border: 1px solid #dce9df !important;
    border-radius: 12px !important;
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    color: #17452e !important;
}

/* ===== TABLES ===== */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #ffffff !important;
    color: #222222 !important;
}

/* ===== EXPANDERS ===== */
[data-testid="stExpander"] {
    background-color: #ffffff !important;
    border: 1px solid #dce9df !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary span {
    color: #17452e !important;
    font-weight: 700 !important;
}

/* ===== TABS ===== */
button[data-baseweb="tab"] {
    color: #17452e !important;
    font-weight: 700 !important;
}

/* ===== CHECKBOXES AND RADIO BUTTONS ===== */
.stCheckbox label,
.stRadio label {
    color: #26352d !important;
}

/* ===== FILE UPLOAD ===== */
[data-testid="stFileUploader"] {
    background-color: #ffffff !important;
    color: #26352d !important;
    border-radius: 10px !important;
}

/* ===== DIVIDERS ===== */
hr {
    border-color: #c8d9cd !important;
}

/* ===== SUBMIT DONATION BUTTON ===== */
.stFormSubmitButton button {
    background-color: #176b45 !important;
    color: #ffffff !important;
    border: 2px solid #104d32 !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

.stFormSubmitButton button p,
.stFormSubmitButton button span {
    color: #ffffff !important;
}

/* ===== PROCESSED AND COLLECTED MESSAGES ===== */
[data-testid="stAlert"] {
    background-color: #e8f5e9 !important;
    border: 2px solid #176b45 !important;
    padding: 12px !important;
    border-radius: 10px !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: #17452e !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)

create_table()

st.title("🍱 FOODLOOP")
st.subheader("AI-Powered Surplus Food Rescue and Redistribution")

st.write(
    "Connecting food donors, NGOs and volunteers "
    "to reduce food waste."
)

st.divider()

# FOOD DONATION FORM

st.header("🍲 Donate Surplus Food")

with st.form("donation_form"):

    donor_name = st.text_input("Donor Name")
    food_name = st.text_input("Food Name")

    quantity = st.number_input(
        "Number of Portions",
        min_value=1,
        step=1
    )

    food_type = st.selectbox(
        "Food Category",
        ["Vegetarian", "Non-Vegetarian", "Vegan"]
    )

    preparation_time = st.text_input(
        "Food Preparation Time"
    )

    expiry_time = st.text_input(
        "Collection Deadline"
    )

    location = st.text_input("Pickup Location")

    storage = st.selectbox(
        "Storage / Handling",
        ["Normal", "Refrigerated", "Hot"]
    )

    submitted = st.form_submit_button("Submit Donation")

    if submitted:

        if (
            donor_name
            and food_name
            and location
            and preparation_time
            and expiry_time
        ):

            save_donation(
                donor_name,
                food_name,
                quantity,
                food_type,
                str(preparation_time),
                str(expiry_time),
                location,
                storage
            )

            st.success(
                "Food donation submitted successfully!"
            )

            matched_ngos = match_ngos(
                location,
                food_type,
                quantity
            )

            st.subheader("🤝 Matching NGOs")

            if matched_ngos:

                for ngo in matched_ngos:

                    st.write("NGO Name:", ngo["name"])
                    st.write("Location:", ngo["location"])
                    st.write("Food Type:", ngo["food_type"])
                    st.write("Capacity:", ngo["capacity"])
                    st.divider()

            else:
                st.warning(
                    "No matching NGO found for this donation."
                )

        else:
            st.error("Please fill all the required fields.")

st.divider()

# ALL FOOD DONATIONS

st.header("📋 All Food Donations")

donations = get_donations()
# FOODLOOP IMPACT DASHBOARD
st.subheader("📊 FOODLOOP Impact Dashboard")

total_donations = len(donations)

total_portions = sum(
    donation[3] for donation in donations
)

collected_donations = sum(
    1 for donation in donations
    if str(donation[9]).strip().lower() == "collected"
)

pending_donations = sum(
    1 for donation in donations
    if str(donation[9]).strip().lower() == "pending"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Donations", total_donations)
col2.metric("Food Portions", total_portions)
col3.metric("Collected", collected_donations)
col4.metric("Pending", pending_donations)
# DONATION STATUS CHART
st.subheader("📈 Donation Status Analysis")

status_data = pd.DataFrame({
    "Status": ["Collected", "Pending"],
    "Donations": [collected_donations, pending_donations]
})

st.bar_chart(
    status_data.set_index("Status")
)
# FOOD CATEGORY DISTRIBUTION
st.subheader("🍱 Food Category Distribution")

if donations:
    category_df = pd.DataFrame(
        donations,
        columns=[
            "ID", "Donor", "Food", "Quantity",
            "Food Category", "Preparation",
            "Deadline", "Location", "Storage", "Status"
        ]
    )

    category_counts = (
        category_df["Food Category"]
        .value_counts()
        .rename_axis("Food Category")
        .reset_index(name="Donations")
    )

    st.bar_chart(
        category_counts.set_index("Food Category")
    )
else:
    st.info("No food categories available yet.")
    # FOOD PORTIONS BY CATEGORY
st.subheader("🍽️ Food Portions by Category")

if donations:
    portions_data = (
        category_df.groupby("Food Category")["Quantity"]
        .sum()
        .reset_index()
    )

    st.bar_chart(
        portions_data.set_index("Food Category")
    )
    # FOODLOOP IMPACT SUMMARY
st.divider()
st.subheader("🌍 Our Environmental Impact")

if total_donations > 0:
    st.markdown(
        f"""
        <div style="
            background-color: #e8f5e9;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 12px;
        ">
            <h3 style="color: #176b45;">
                Food Rescue Impact
            </h3>
            <p style="color: #26352d;">
                Total food portions recorded:
                <b>{total_portions}</b>
            </p>
            <p style="color: #26352d;">
                Total donations:
                <b>{total_donations}</b>
            </p>
            <p style="color: #26352d;">
                Successfully collected:
                <b>{collected_donations}</b>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Start donating food to see our impact!")

st.divider()

if donations:

    df = pd.DataFrame(
        donations,
        columns=[
            "Donation ID",
            "Donor Name",
            "Food Name",
            "Quantity",
            "Food Category",
            "Preparation Time",
            "Collection Deadline",
            "Location",
            "Storage",
            "Status"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

else:
    st.info("No food donations available yet.")

st.divider()

# TEMPORARY QR TESTING

with st.expander("🛠️ QR Testing"):

    st.write(
        "Reset Donation ID 7 to Accepted "
        "for QR scanner testing."
    )

    if st.button("Reset Donation ID 7 to Accepted"):

        update_donation_status(7, "Accepted")

        st.success("Donation ID 7 is now Accepted!")

        st.rerun()

st.divider()

# NGO DASHBOARD

ngo_dashboard()

st.divider()

# VOLUNTEER DASHBOARD

volunteer_dashboard()