import streamlit as st
import pandas as pd
import base64
from datetime import date
from pathlib import Path
import matplotlib.pyplot as plt

# =================================================================
# 1. PAGE CONFIG
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics | Streamlit UI", layout="wide")

# =================================================================
# 2. ASSETS & PATHS
# =================================================================
def get_base64_image(image_path):
    try:
        if isinstance(image_path, Path) and not image_path.exists():
            return ""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception: return ""

# Streamlit Cloud runs from the root of your GitHub repo
root_dir = Path.cwd() 
logo_path = root_dir / "ola.png"
logo_base64 = get_base64_image(logo_path)

# =================================================================
# 3. CUSTOM STYLING (OLA Branding)
# =================================================================
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"], .stMarkdown p {{ 
        font-family: 'Poppins', sans-serif; 
        font-weight: 500; 
    }}

    .title-box {{
        display: flex; align-items: center; justify-content: center; gap: 30px; 
        padding: 25px; background-color: #121821; border-radius: 15px; 
        border: 5px solid #D2EF1A; box-shadow: 0px 0px 20px rgba(210, 239, 26, 0.4);
        margin: 10px 0px 20px 0px;
    }}

    .ola-text {{ font-size: 40px; color: #D2EF1A; font-weight: 800; text-transform: uppercase; margin: 0; }}
    .dev-info {{ text-align: right; color: white; line-height: 1.2; margin-bottom: 5px; }}
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 4. BRANDING HEADER
# =================================================================
st.markdown(f"""
<div class="dev-info">
    <b>Name: SUMITHRA D</b><br>
    Roll Number: 28552 | BATCH: E332
</div>
<div class="title-box">
    <img src="data:image/png;base64,{logo_base64}" height="70">
    <h1 class="ola-text">OLA RIDE INSIGHTS</h1>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 5. DATA LOADING LOGIC (CSV ONLY)
# =================================================================
@st.cache_data
def load_data():
    csv_file = "Ola_Rides_Cleaned_File.csv"
    if Path(csv_file).exists():
        df = pd.read_csv(csv_file)
        # Pre-processing
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce').fillna(0)
        df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce').fillna(0)
        df['Customer_Rating'] = pd.to_numeric(df['Customer_Rating'], errors='coerce').fillna(0)
        df['Driver_Ratings'] = pd.to_numeric(df['Driver_Ratings'], errors='coerce').fillna(0)
        return df
    return pd.DataFrame()

df = load_data()

# =================================================================
# 6. SIDEBAR NAVIGATION & FILTERS
# =================================================================
if not df.empty:
    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)

    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Select View", ["Dashboard", "Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"])
    
    st.sidebar.markdown("---")
    st.sidebar.header("Global Filters")

    # Date Filter
    start_date_val = date(2024, 7, 1)
    end_date_val = date(2024, 7, 31)
    date_range = st.sidebar.date_input("Select Date Range", [start_date_val, end_date_val])

    # Dynamic Filters
    bs_list = ["All"] + sorted(df['Booking_Status'].unique().tolist())
    vt_list = ["All"] + sorted(df['Vehicle_Type'].unique().tolist())
    pm_list = ["All"] + sorted(df['Payment_Method'].unique().tolist())
    
    selected_bs = st.sidebar.selectbox("Booking Status", bs_list)
    selected_vt = st.sidebar.selectbox("Vehicle Type", vt_list)
    selected_pm = st.sidebar.selectbox("Payment Method", pm_list)

    # Apply Filters to the dataframe
    filtered_df = df.copy()
    if isinstance(date_range, list) and len(date_range) == 2:
        filtered_df = filtered_df[(filtered_df['Date'] >= date_range[0]) & (filtered_df['Date'] <= date_range[1])]
    if selected_bs != "All":
        filtered_df = filtered_df[filtered_df['Booking_Status'] == selected_bs]
    if selected_vt != "All":
        filtered_df = filtered_df[filtered_df['Vehicle_Type'] == selected_vt]
    if selected_pm != "All":
        filtered_df = filtered_df[filtered_df['Payment_Method'] == selected_pm]

    # =============================================================
    # 7. PAGE CONTENT LOGIC
    # =============================================================
    
    # --- 1. DASHBOARD PAGE ---
    if page == "Dashboard":
        st.title("🚖 Executive Dashboard")
        m1, m2, m3, m4, m5 = st.columns(5)
        
        m1.metric("Total Revenue", f"₹{filtered_df['Booking_Value'].sum()/1e6:.1f}M")
        m2.metric("Success Rides", f"{len(filtered_df[filtered_df['Booking_Status']=='Success'])/1e3:.1f}K")
        m3.metric("Total Dist", f"{filtered_df['Ride_Distance'].sum()/1e3:.1f}K Km")
        m4.metric("Avg Rating", f"{filtered_df['Customer_Rating'].mean():.1f} ⭐")
        m5.metric("Avg Driver", f"{filtered_df['Driver_Ratings'].mean():.1f} ⭐")

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Avg Value by Vehicle")
            chart1 = filtered_df.groupby("Vehicle_Type")["Booking_Value"].mean()
            st.bar_chart(chart1, color="#D2EF1A")
        with col2:
            st.markdown("### Distance by Date")
            chart2 = filtered_df.groupby("Date")["Ride_Distance"].sum()
            st.bar_chart(chart2, color="#D2EF1A")

    # --- 2. OVERALL PAGE ---
    elif page == "Overall":
        st.title("📊 Overall Performance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL RIDES", f"{len(filtered_df):,}")
        c2.metric("REVENUE", f"₹{filtered_df['Booking_Value'].sum():,.0f}")
        c3.metric("AVG RATING", f"{filtered_df['Customer_Rating'].mean():.2f} ⭐")
        c4.metric("DISTANCE", f"{filtered_df['Ride_Distance'].sum():,.0f} km")

        st.divider()
        l_col, r_col = st.columns(2)
        with l_col:
            st.subheader("Ride Volume Over Time")
            chart3 = filtered_df.groupby("Date").size()
            st.line_chart(chart3, color="#D2EF1A")
        with r_col:
            st.subheader("Booking Status")
            status_data = filtered_df['Booking_Status'].value_counts()
            fig, ax = plt.subplots()
            ax.pie(status_data, labels=status_data.index, autopct='%1.1f%%', colors=['#D2EF1A', '#FF4B4B', '#444444', '#888888'])
            fig.patch.set_facecolor('none')
            st.pyplot(fig)

    # --- 3. VEHICLE TYPE PAGE ---
    elif page == "Vehicle Type":
        st.title("🚗 Vehicle Type Performance")
        v_stats = filtered_df.groupby("Vehicle_Type").agg({
            'Booking_Value': 'sum',
            'Ride_Distance': 'mean'
        }).reset_index()
        st.dataframe(v_stats, use_container_width=True)
        st.bar_chart(v_stats.set_index("Vehicle_Type")['Booking_Value'], color="#D2EF1A")

    # --- 4. REVENUE PAGE ---
    elif page == "Revenue":
        st.title("💰 Revenue Insights")
        st.metric("Total Portfolio Value", f"₹{filtered_df['Booking_Value'].sum():,.2f}")
        rev_chart = filtered_df.groupby("Date")["Booking_Value"].sum()
        st.area_chart(rev_chart, color="#D2EF1A")

    # --- 5. CANCELLATION PAGE ---
    elif page == "Cancellation":
        st.title("🚫 Cancellation Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Canceled by Customer")
            df_cust = filtered_df[filtered_df['Booking_Status'] == 'Canceled by Customer']
            if not df_cust.empty:
                st.bar_chart(df_cust['Canceled_Rides_by_Customer'].value_counts(), color="#FF4B4B")
        with col2:
            st.subheader("Canceled by Driver")
            df_drv = filtered_df[filtered_df['Booking_Status'] == 'Canceled by Driver']
            if not df_drv.empty:
                st.bar_chart(df_drv['Canceled_Rides_by_Driver'].value_counts(), color="#FF4B4B")

    # --- 6. RATINGS PAGE ---
    elif page == "Ratings":
        st.title("⭐ Ratings Overview")
        df_ratings = filtered_df.groupby("Vehicle_Type")[['Customer_Rating', 'Driver_Ratings']].mean()
        st.bar_chart(df_ratings, color=["#D2EF1A", "#888888"])

else:
    st.error("⚠️ 'Ola_Rides_Cleaned_File.csv' not found. Please upload it to your GitHub root folder.")
