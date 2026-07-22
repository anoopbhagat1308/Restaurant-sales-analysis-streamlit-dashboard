
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="Restaurant Sales Dashboard",
    page_icon="🍽️",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>

.main{
    background-color:#F8F9FA;
}

h1{
    color:#E74C3C;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Title
# ---------------------------
st.title("🍽️ Restaurant Sales Analysis Dashboard")

# ---------------------------
# File Upload
# ---------------------------
uploaded_file = st.file_uploader(
    "Upload Restaurant Sales CSV",
    type=["csv"]
)

# ---------------------------
# Run only after upload
# ---------------------------
if uploaded_file is not None:

    # Read Dataset
    df = pd.read_csv(uploaded_file)

    # Convert Date Column
    df['date'] = pd.to_datetime(df['date'], format='mixed')

    # filling nan values with 'unknown'
    df['transaction_type'] = df['transaction_type'].fillna('Unknown')

    # Create Month Column
    df["month"] = df["date"].dt.month_name()

    st.success("✅ Dataset Uploaded Successfully")

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # ---------------------------
    # Sidebar Filters
    # ---------------------------
    st.sidebar.header("🔎 Filters")

    payment = st.sidebar.multiselect(
        "Payment Type",
        options=df["transaction_type"].unique(),
        default=df["transaction_type"].unique()
    )

    filtered_df = df[df["transaction_type"].isin(payment)]

    # ---------------------------
    # KPI Cards
    # ---------------------------
    total_sales = filtered_df["transaction_amount"].sum()
    total_orders = filtered_df.shape[0]
    avg_order = filtered_df["transaction_amount"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
    col2.metric("🛒 Total Orders", total_orders)
    col3.metric("📦 Average Order", f"₹{avg_order:.2f}")

    st.markdown("---")

    # ---------------------------
    # Daily Sales Trend
    # ---------------------------
    st.subheader("📈 Daily Sales Trend")

    daily = (
        filtered_df
        .groupby("date")["transaction_amount"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        daily,
        x="date",
        y="transaction_amount",
        markers=True,
        title="Daily Sales"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Top Selling Items
    # ---------------------------
    st.subheader("🍕 Top 10 Selling Items")

    top = (
        filtered_df
        .groupby("item_name")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        top,
        x="item_name",
        y="quantity",
        color="quantity",
        title="Top Selling Items"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Revenue by Category
    # ---------------------------
    st.subheader("🥗 Revenue by Category")

    cat = (
        filtered_df
        .groupby("item_type")["transaction_amount"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        cat,
        values="transaction_amount",
        names="item_type",
        hole=0.4,
        title="Revenue by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Monthly Sales
    # ---------------------------
    st.subheader("📅 Monthly Sales")

    monthly = (
        filtered_df
        .groupby("month")["transaction_amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        monthly,
        x="month",
        y="transaction_amount",
        color="transaction_amount",
        title="Monthly Sales"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Sales by Time of Day
    # ---------------------------
    st.subheader("⏰ Sales by Time of Day")

    hour = (
        filtered_df
        .groupby("time_of_sale")["transaction_amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        hour,
        x="time_of_sale",
        y="transaction_amount",
        color="transaction_amount",
        title="Sales by Time of Day"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------------------
    # Download Filtered Dataset
    # ---------------------------
    st.subheader("⬇️ Download Filtered Data")

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="RestaurantSales.csv",
        mime="text/csv"
    )

else:

    st.info("👆 Please upload your Restaurant Sales CSV file to begin.")