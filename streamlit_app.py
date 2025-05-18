
import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Hotel Scraper Results", layout="wide")
st.title("🏨 Google Maps Hotel Data Viewer")

st.info("Fetching data from the database...")

# Replace with your hosted DB info
DB_HOST = st.secrets["DB_HOST"]
DB_NAME = st.secrets["DB_NAME"]
DB_USER = st.secrets["DB_USER"]
DB_PASS = st.secrets["DB_PASS"]

@st.cache_data
def load_data():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port="5432"
        )
        df = pd.read_sql("SELECT * FROM hotels", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.success(f"Loaded {len(df)} records.")
    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "hotels.csv")
else:
    st.warning("No data found.")
