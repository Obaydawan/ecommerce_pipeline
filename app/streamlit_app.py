import streamlit as st
import snowflake.connector
import pandas as pd

st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")

st.title("🛒 E-Commerce Analytics Dashboard (Olist)")
st.markdown("Insights built from Snowflake, dbt, and Streamlit.")

@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"]
    )

try:
    conn = init_connection()
except Exception as e:
    st.error(f"Connection error details: {e}")
    st.stop()

@st.cache_data
def load_data():
    query = "SELECT * FROM ecommerce_raw.analytics.orders_summary LIMIT 1000"
    return pd.read_sql(query, conn)

df = load_data()

st.subheader("Recent Orders Summary")
st.dataframe(df)

st.metric(label="Total Order Value Tracked", value=f"${df['TOTAL_ORDER_VALUE'].sum():,.2f}")

st.subheader("Monthly Order Revenue Trends")
df['ORDER_PURCHASE_TIMESTAMP'] = pd.to_datetime(df['ORDER_PURCHASE_TIMESTAMP'])
monthly = df.set_index('ORDER_PURCHASE_TIMESTAMP').resample('ME')['TOTAL_ORDER_VALUE'].sum()
st.line_chart(monthly)
