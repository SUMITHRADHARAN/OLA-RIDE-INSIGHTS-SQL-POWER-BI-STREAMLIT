import streamlit as st
import mysql.connector
import pandas as pd
import base64

# =================================================================
# 1. PAGE CONFIG (Must be first)
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics | SQL Queries", layout="wide")

# =================================================================
# 2. ASSETS & IMAGE ENCODING
# =================================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# Path to your local logo
logo_path = r"C:\Users\dhara\Documents\Interns\Labmentix\2. Ola Ride insights\ola.png"
logo_base64 = get_base64_image(logo_path)

# =================================================================
# 3. SIDEBAR LOGO
# =================================================================
st.sidebar.image(logo_path, use_container_width=True)

# =================================================================
# 4. CUSTOM STYLING (Poppins Font & Neon Branding)
# =================================================================
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] {{ 
        font-family: 'Poppins', sans-serif; 
    }}

    /* Main Branding Box */
    .title-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px; 
        padding: 25px; 
        background-color: #121821; 
        border-radius: 15px; 
        border: 5px solid #D2EF1A; 
        box-shadow: 0px 0px 20px rgba(210, 239, 26, 0.4);
        margin: 10px 0px 20px 0px;
    }}

    .logo-img {{ height: 70px; }}

    .ola-text {{
        font-size: 40px; 
        color: #D2EF1A; 
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
    }}

    /* Styled Subtitle */
    .sub-title-container {{
        text-align: center;
        margin-bottom: 20px;
    }}

    .sub-title {{
        font-size: 24px;
        color: #ffffff;
        font-weight: 600;
        border-bottom: 3px solid #D2EF1A;
        display: inline-block;
        padding-bottom: 5px;
    }}

    .dev-info {{
        text-align: right; 
        line-height: 1.2; 
        margin-bottom: 5px;
        color: white;
        font-weight: 400;
    }}
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 5. BRANDING HEADER
# =================================================================
st.markdown(f"""
<div class="dev-info">
    <b>Name: SUMITHRA D</b><br>
    Roll Number: 28552 | BATCH: E332
</div>

<div class="title-box">
    <img src="data:image/png;base64,{logo_base64}" class="logo-img">
    <h1 class="ola-text">OLA RIDE INSIGHTS</h1>
</div>

<div class="sub-title-container">
    <div class="sub-title">🔍 SQL Query Analysis</div>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. DATABASE CONNECTION LOGIC
# =================================================================
def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="dm3879@D", 
        database="Ola_Rides",
        port=3306
    )

def execute_query(q):
    try:
        conn = get_db_connection()
        df = pd.read_sql(q, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Connection Error: {e}")
        return None

# =================================================================
# 7. QUERIES & UI
# =================================================================
queries = {
    "1. Retrieve all successful bookings": "SELECT * FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Success';",
    "2. Avg distance per vehicle": "SELECT Vehicle_Type, ROUND(AVG(Ride_Distance), 2) AS avg_dist FROM Ola_Ride_Cleaned_File GROUP BY Vehicle_Type;",
    "3. Total cancelled by customers": "SELECT COUNT(*) AS total FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Canceled by Customer';",
    "4. Top 5 customers": "SELECT Customer_ID, COUNT(*) AS rides FROM Ola_Ride_Cleaned_File GROUP BY Customer_ID ORDER BY rides DESC LIMIT 5;",
    "5. Cancelled by drivers (Personal/Car)": "SELECT COUNT(*) FROM Ola_Ride_Cleaned_File WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue';",
    "6. Max/Min ratings (Prime Sedan)": "SELECT MAX(Driver_Ratings), MIN(Driver_Ratings) FROM Ola_Ride_Cleaned_File WHERE Vehicle_Type = 'Prime Sedan';",
    "7. UPI Payments": "SELECT * FROM Ola_Ride_Cleaned_File WHERE Payment_Method = 'UPI';",
    "8. Avg customer rating per vehicle": "SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) FROM Ola_Ride_Cleaned_File GROUP BY Vehicle_Type;",
    "9. Total successful booking value": "SELECT SUM(Booking_Value) FROM Ola_Ride_Cleaned_File WHERE Booking_Status = 'Success';",
    "10. Incomplete rides": "SELECT Booking_ID, Incomplete_Rides_Reason FROM Ola_Ride_Cleaned_File WHERE Incomplete_Rides = 'Yes';"
}

selected_q = st.selectbox("Choose a question to analyze:", list(queries.keys()))

st.markdown("### SQL Code")
st.code(queries[selected_q], language='sql')

if st.button("Run Query"):
    st.subheader("Result")
    df_result = execute_query(queries[selected_q])
    
    if df_result is not None:
        if not df_result.empty:
            st.dataframe(df_result, use_container_width=True)
            st.success(f"✅ Successfully retrieved {len(df_result)} rows.")
        else:
            st.warning("⚠️ No records found.")
