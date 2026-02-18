import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from sqlalchemy import create_engine, text
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(
    layout="wide", 
    page_title="Ola Analytics 2026",
    initial_sidebar_state="expanded" 
)

# --- STEP 1: DATABASE INITIALIZATION ---
def initialize_db():
    engine = create_engine("mysql+pymysql://root:dm3879%40D@127.0.0.1")
    
    setup_commands = [
        "CREATE DATABASE IF NOT EXISTS Ola",
        "USE Ola",
        """CREATE TABLE IF NOT EXISTS book (
            Booking_ID VARCHAR(50) PRIMARY KEY,
            Booking_Status VARCHAR(50),
            Vehicle_Type VARCHAR(50),
            Ride_Distance DECIMAL(10,2),
            Customer_ID VARCHAR(50),
            Canceled_Rides_by_Driver VARCHAR(100),
            Driver_Ratings DECIMAL(3,1),
            Customer_Rating DECIMAL(3,1),
            Payment_Method VARCHAR(50),
            Booking_Value INT,
            Incomplete_Rides VARCHAR(5),
            Incomplete_Rides_Reason VARCHAR(255)
        )""",
        # The view for top 5 customers is created in the DB but we will use
        # the filtered DataFrame in the dashboard logic for dynamic filtering.
        "CREATE OR REPLACE VIEW Success_Booking AS SELECT * FROM book WHERE Booking_Status = 'Success'",
        "CREATE OR REPLACE VIEW average_ride_distance_for_each_vehicle AS SELECT Vehicle_Type, AVG(Ride_Distance) AS avg_distance FROM book GROUP BY Vehicle_Type",
        "CREATE OR REPLACE VIEW number_of_cancelled_rides AS SELECT COUNT(*) AS total_cancelled FROM book WHERE Booking_Status = 'Canceled by Customer'",
        "CREATE OR REPLACE VIEW top_5_customers AS SELECT Customer_ID, COUNT(Booking_ID) AS total_rides FROM book GROUP BY Customer_ID ORDER BY total_rides DESC LIMIT 5",
        "CREATE OR REPLACE VIEW rides_cancelled_by_drivers AS SELECT COUNT(*) AS cancelled_count FROM book WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'",
        "CREATE OR REPLACE VIEW Max_Min_Driver_Rating AS SELECT MAX(Driver_Ratings) AS max_rating, MIN(Driver_Ratings) AS min_rating FROM book WHERE Vehicle_Type = 'Prime Sedan'",
        "CREATE OR REPLACE VIEW UPI_payments AS SELECT * FROM book WHERE Payment_Method = 'UPI'",
        "CREATE OR REPLACE VIEW avg_rating_for_v_type AS SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 1) AS avg_rating FROM book GROUP BY Vehicle_Type",
        "CREATE OR REPLACE VIEW total_booking_value_rides_completed AS SELECT SUM(Booking_Value) AS total_successful_value FROM book WHERE Booking_Status = 'Success'",
        "CREATE OR REPLACE VIEW Incomplete_Rides_Reason_View AS SELECT Booking_ID, Incomplete_Rides_Reason FROM book WHERE Incomplete_Rides = 'Yes'"
    ]
    try:
        with engine.connect() as conn:
            for cmd in setup_commands:
                conn.execute(text(cmd))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Database Initialization Error: {e}")
        return False

db_ready = initialize_db()

# --- STEP 2: SIDEBAR FILTERS & NAVIGATION ---
st.sidebar.title("🔍 OLA CONTROL PANEL")

page = st.sidebar.radio(
    "Navigation",
    ["Main Dashboard", "Vehicle Analysis", "Revenue & Payments", "Cancellations", "Power BI Deep Dive"]
)

st.sidebar.divider()
st.sidebar.subheader("Global Data Filters")

if db_ready:
    try:
        conn = st.connection("mysql", type="sql")

        def get_options(column):
            try:
                query = f"SELECT DISTINCT {column} FROM book"
                res = conn.query(query)
                return ["All"] + res[column].dropna().tolist()
            except:
                return ["All"]

        bs = st.sidebar.selectbox("Filter by Booking Status", get_options("Booking_Status"))
        vt = st.sidebar.selectbox("Filter by Vehicle Type", get_options("Vehicle_Type"))
        pm = st.sidebar.selectbox("Filter by Payment Method", get_options("Payment_Method"))

        if st.sidebar.button("Clear Cache & Refresh"):
            st.cache_data.clear()
            st.rerun()

        # --- STEP 3: DATA PROCESSING ---
        base_query = "SELECT * FROM book WHERE 1=1"
        if bs != "All": base_query += f" AND Booking_Status = '{bs}'"
        if vt != "All": base_query += f" AND Vehicle_Type = '{vt}'"
        if pm != "All": base_query += f" AND Payment_Method = '{pm}'"

        df = conn.query(base_query, ttl="5m")

        # --- STEP 4: MAIN CONTENT ROUTING ---
        st.title(f"OLA DATA ANALYTICS - {page.upper()}")

        if page == "Main Dashboard":
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Bookings", len(df))
                col2.metric("Total Revenue", f"₹{df['Booking_Value'].sum():,}")
                col3.metric("Avg Ride Distance", f"{round(df['Ride_Distance'].mean(), 2)} km")

                st.divider()
                
                # Use two columns for the main data and the new top customers list
                col_main_table, col_top_customers = st.columns([2, 1])

                with col_main_table:
                    st.subheader("Booking Overview Table")
                    st.dataframe(df, use_container_width=True)
                
                with col_top_customers:
                    st.subheader("🏆 Top 5 Customers (Filtered)")
                    # Calculate top 5 customers from the filtered dataframe
                    top_customers_df = df.groupby("Customer_ID").size().reset_index(name='Total_Rides')
                    top_customers_df = top_customers_df.sort_values(by='Total_Rides', ascending=False).head(5)
                    st.dataframe(top_customers_df, use_container_width=True, hide_index=True)


            else:
                st.info("No data matches the selected filters.")

        elif page == "Vehicle Analysis":
            st.subheader("Average Distance by Category (Filtered)")
            if not df.empty:
                avg_dist_filtered = df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index()
                st.bar_chart(avg_dist_filtered.set_index("Vehicle_Type"))
                st.dataframe(avg_dist_filtered)
            else:
                st.info("No vehicle data found for current filters.")

        elif page == "Revenue & Payments":
            st.subheader("Revenue Breakdown (Filtered)")
            if not df.empty:
                rev_data = df.groupby("Payment_Method")["Booking_Value"].sum().reset_index()
                st.table(rev_data)
            else:
                st.info("No revenue data found for current filters.")

        elif page == "Cancellations":
            st.subheader("Incomplete Rides Reason Analysis")
            # Note: This view query ignores global filters except for the default 'book' table data
            inc = conn.query("SELECT * FROM Incomplete_Rides_Reason_View")
            st.dataframe(inc, use_container_width=True)

        elif page == "Power BI Deep Dive":
            st.subheader("Interactive Report (Filtered by Vehicle Type)")
            pbi_url = "https://app.powerbi.com/reportEmbed?reportId=05950598-9e8b-4e9e-9a57-57cf1e7cbe0e&autoAuth=true&ctid=f3c9ebc3-0543-43d8-9cac-9db513a7c000"
            
        
            if vt != "All":
                pbi_filter = f"&$filter=book/Vehicle_Type eq '{vt}'" 
                encoded_filter = urllib.parse.quote(pbi_filter, safe="&$=")
                pbi_url += encoded_filter

            components.iframe(pbi_url, height=800, scrolling=True)

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")
        st.info("Ensure your database table 'book' contains data.")
else:
    st.warning("Please check your MySQL connection settings.")

            
            
           