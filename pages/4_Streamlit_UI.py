import streamlit as st
import mysql.connector
import pandas as pd
import base64
from datetime import date

# =================================================================
# 1. PAGE CONFIG (Must be first)
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics | Project Summary", layout="wide")

from pathlib import Path

# =================================================================
# 2. ASSETS & IMAGE ENCODING (Fixed for Deployment)
# =================================================================
def get_base64_image(image_path):
    try:
        # Check if path is a Path object or string
        if isinstance(image_path, Path) and not image_path.exists():
            return ""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# Get path relative to the root of your GitHub Repo
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
root_dir = current_dir.parent 
logo_path = root_dir / "ola.png"  # Assumes ola.png is in your main repository folder

logo_base64 = get_base64_image(logo_path)

# =================================================================
# 3. SIDEBAR LOGO (Protected from Crashing)
# =================================================================
if logo_path.exists():
    st.sidebar.image(str(logo_path), use_container_width=True)
else:
    st.sidebar.warning("Logo 'ola.png' not found in root folder.")


# =================================================================
# 4. CUSTOM STYLING (Poppins Medium & Increased Result Size)
# =================================================================
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"], .stMarkdown p {{ 
        font-family: 'Poppins', sans-serif; 
        font-weight: 500; /* MEDIUM FONT WEIGHT */
    }}

    /* Increase Result Table Font Size */
    [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th, .stTable td {{
        font-size: 18px !important;
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
    }}
    </style>
""", unsafe_allow_html=True)

# Ola Signature Colors
OLA_LIME = "#D2EF1A"
OLA_BG = "#0B0F14"
OLA_CARD = "#121821"
OLA_BORDER = "#2A2F3A"

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
    <div class="sub-title"> Streamlit UI </div>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. MYSQL CONNECTION & LOGIC(CSV ONLY)
# =================================================================

def load_data():
    try:
        current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
        root_dir = current_dir.parent 
        # Verify this exact name is on GitHub
        csv_path = root_dir / "Ola_Rides_Cleaned_File.csv" 
        
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            # Basic cleaning
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        else:
            st.error(f"⚠️ File NOT found: {csv_path.name}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return pd.DataFrame()

# =================================================================
# 7. EXECUTION & FILTERS
# =================================================================
df = load_data()

if not df.empty:
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("🔍 Navigation")
    page = st.sidebar.radio("Select View", ["Dashboard", "Ratings"])
    
    st.sidebar.markdown("---")
    st.sidebar.header("Global Filters")

    # Dynamic Filters using the loaded DataFrame (No SQL needed)
    booking_status = ["All"] + sorted(df['Booking_Status'].unique().tolist())
    vehicle_type = ["All"] + sorted(df['Vehicle_Type'].unique().tolist())
    
    bs = st.sidebar.selectbox("Booking Status", booking_status)
    vt = st.sidebar.selectbox("Vehicle Type", vehicle_type)

    # Apply Filters to the DataFrame
    filtered_df = df.copy()
    if bs != "All":
        filtered_df = filtered_df[filtered_df['Booking_Status'] == bs]
    if vt != "All":
        filtered_df = filtered_df[filtered_df['Vehicle_Type'] == vt]

    # --- DISPLAY ---
    st.subheader("📊 Dataset Overview")
    st.dataframe(filtered_df.head(10), use_container_width=True)
    
    if page == "Dashboard":
        st.title("🚖 OLA Executive Dashboard")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Revenue", f"₹{filtered_df['Booking_Value'].sum():,.0f}")
        m2.metric("Total Rides", len(filtered_df))
        m3.metric("Avg Distance", f"{filtered_df['Ride_Distance'].mean():.2f} km")
else:
    st.error("Please ensure 'Ola_Rides_Cleaned_File.csv' is in your GitHub root folder.")
# =================================================================
#           SIDEBAR NAVIGATION & FILTERS
# =================================================================

st.sidebar.title("🔍 Navigation & Filters")
# 1. Navigation
page = st.sidebar.radio(
    "Select Dashboard View",
    ["Dashboard", "Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"]
)

st.sidebar.markdown("---")
st.sidebar.header("Global Filters")

# 2. Date Filter (Fixed Range: Jan 1 to Jan 31, 2024)
start_date_val = date(2024, 7, 1)
end_date_val = date(2024, 7, 31)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [start_date_val, end_date_val],
    min_value=date(2024, 1, 1),
    max_value=date(2024, 12, 31)
)

# 3. Dynamic Dropdown Filters
booking_status = ["All"] + run_query("SELECT DISTINCT Booking_Status FROM ola_ride_cleaned_file")["Booking_Status"].tolist()
vehicle_type = ["All"] + run_query("SELECT DISTINCT Vehicle_Type FROM ola_ride_cleaned_file")["Vehicle_Type"].tolist()
pm_list = ["All"] + run_query("SELECT DISTINCT Payment_Method FROM ola_ride_cleaned_file")["Payment_Method"].tolist()

bs = st.sidebar.selectbox("Booking Status", booking_status)
vt = st.sidebar.selectbox("Vehicle Type", vehicle_type)
pm = st.sidebar.selectbox("Payment Method", pm_list)

# 4. SQL WHERE Clause Construction
filters = []
if isinstance(date_range, list) and len(date_range) == 2:
    filters.append(f"Date BETWEEN '{date_range[0]}' AND '{date_range[1]}'")
elif isinstance(date_range, date):
    filters.append(f"Date = '{date_range}'")

if bs != "All": filters.append(f"Booking_Status = '{bs}'")
if vt != "All": filters.append(f"Vehicle_Type = '{vt}'")
if pm != "All": filters.append(f"Payment_Method = '{pm}'")
where = " WHERE " + " AND ".join(filters) if filters else ""


# =================================================================
#           1. DASHBOARD PAGE
# =================================================================
if page == "Dashboard":
    st.title("🚖 OLA Executive Dashboard")
    
    # --- KPI Metrics Row ---
    st.subheader("Key Performance Indicators")
    m1, m2, m3, m4, m5 = st.columns(5)

    try:
        kpi_data = run_query(f"""
            SELECT 
                COALESCE(SUM(Booking_Value), 0) as total_rev,
                COUNT(CASE WHEN Booking_Status = 'Success' THEN 1 END) as success_bookings,
                COALESCE(SUM(Ride_Distance), 0) as total_dist,
                COALESCE(AVG(Customer_Rating), 0) as avg_ctat, 
                COALESCE(AVG(Driver_Ratings), 0) as avg_vtat  
            FROM ola_ride_cleaned_file
            {where}
        """).iloc[0]

        m1.metric("Total Revenue", f"₹{kpi_data['total_rev']/1000000:.1f}M")
        m2.metric("Successful Bookings", f"{int(kpi_data['success_bookings']/1000)}K")
        m3.metric("Distance Travelled", f"{int(kpi_data['total_dist']/1000)}Km")
        m4.metric("Avg CTAT Time", f"{int(kpi_data['avg_ctat'])}")
        m5.metric("Avg VTAT Time", f"{int(kpi_data['avg_vtat'])}")
    except Exception as e:
        st.error(f"KPI Error: {e}")

    st.divider()

    # --- Charts Row 1: Side-by-Side ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Avg Booking Value by Vehicle Type")
        df_avg_val = run_query(f"SELECT Vehicle_Type, ROUND(AVG(Booking_Value), 2) as avg_value FROM ola_ride_cleaned_file {where} GROUP BY Vehicle_Type")
        st.bar_chart(df_avg_val.set_index("Vehicle_Type"), color=OLA_LIME)

    with col2:
        st.markdown("### Ride Distribution by Date")
        df_dist = run_query(f"SELECT Date, SUM(Ride_Distance) as sum_distance FROM ola_ride_cleaned_file {where} GROUP BY Date ORDER BY Date")
        st.bar_chart(df_dist.set_index("Date"), color=OLA_LIME)

    st.divider()

    # --- Charts Row 2: 3-Column Section ---
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<h3 style='text-align: center;'>Most Preferable Vehicle Type</h3>", unsafe_allow_html=True)
        df_pref = run_query(f"SELECT Vehicle_Type, COUNT(*) as ride_count FROM ola_ride_cleaned_file {where} GROUP BY Vehicle_Type ORDER BY ride_count DESC")
        st.bar_chart(df_pref.set_index("Vehicle_Type"), horizontal=True, color=OLA_LIME)

    with c2:
        st.markdown("<h3 style='text-align: center;'>Avg Customer Rating</h3>", unsafe_allow_html=True)
        df_rating = run_query(f"SELECT Vehicle_Type, AVG(Customer_Rating) as avg_rating FROM ola_ride_cleaned_file {where} GROUP BY Vehicle_Type")
        st.area_chart(df_rating.set_index("Vehicle_Type"), color=OLA_LIME)

    with c3:
        st.markdown("<h3 style='text-align: center;'>Top Pickup Locations</h3>", unsafe_allow_html=True)
        loc_where = where + " AND Booking_Status = 'Success'" if "WHERE" in where else " WHERE Booking_Status = 'Success'"
        df_loc = run_query(f"SELECT Pickup_Location, COUNT(*) as SuccessCount FROM ola_ride_cleaned_file {loc_where} GROUP BY Pickup_Location ORDER BY SuccessCount DESC LIMIT 6")
        st.table(df_loc)

# =================================================================
#           2. OVERALL PERFORMANCE PAGE
# =================================================================
elif page == "Overall":
    st.title("📊 Overall Performance")
    
    # --- KPI Metrics Row ---
    c1, c2, c3, c4 = st.columns(4)
    metrics = run_query(f"""
        SELECT COUNT(*) as rides, SUM(Booking_Value) as rev, 
        AVG(Customer_Rating) as rat, SUM(Ride_Distance) as dist 
        FROM ola_ride_cleaned_file {where}
    """).iloc[0]

    c1.metric("TOTAL RIDES", f"{int(metrics['rides']):,}")
    c2.metric("REVENUE (₹)", f"₹{float(metrics['rev'] or 0):,.0f}")
    c3.metric("AVG RATING", f"{round(float(metrics['rat'] or 0), 2)} ⭐")
    c4.metric("DISTANCE (KM)", f"{round(float(metrics['dist'] or 0), 1)} km")

    st.divider()

        # --- Charts Row ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Ride Volume Over Time")
        df_time = run_query(f"SELECT Date, COUNT(*) as c FROM ola_ride_cleaned_file {where} GROUP BY Date ORDER BY Date")
        st.line_chart(df_time.set_index("Date"), color=OLA_LIME)

    with col_right:
        st.subheader("Booking Status Breakdown")
        import matplotlib.pyplot as plt
        
        # Fetching status counts
        df_status = run_query(f"SELECT Booking_Status, COUNT(*) as c FROM ola_ride_cleaned_file {where} GROUP BY Booking_Status")
        
        if not df_status.empty:
            fig, ax = plt.subplots(figsize=(6, 6))
            # OLA Branding Colors: Lime for Success, Red for Canceled, Greys for others
            colors = [OLA_LIME, '#FF4B4B', '#444444', '#888888', '#AAAAAA']
            
            # Creating the Pie Chart
            ax.pie(df_status['c'], labels=df_status['Booking_Status'], 
                   autopct='%1.1f%%', startangle=140, colors=colors,
                   textprops={'color':"white", 'fontsize': 10})
            
            # Make background transparent to match OLA UI
            fig.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            st.pyplot(fig)
        else:
            st.info("No status data available.")

# =================================================================
#           3. VEHICLE TYPE PERFORMANCE PAGE
# =================================================================
elif page == "Vehicle Type":
    st.title("🚗 Vehicle Type Performance")

    # 1. DATA RETRIEVAL
    df_vehicle_stats = run_query(f"""
        SELECT 
            Vehicle_Type,
            SUM(Booking_Value) as total_val,
            SUM(CASE WHEN Booking_Status = 'Success' THEN Booking_Value ELSE 0 END) as success_val,
            ROUND(AVG(Ride_Distance), 2) as avg_dist,
            SUM(Ride_Distance) as total_dist
        FROM ola_ride_cleaned_file {where}
        GROUP BY Vehicle_Type
    """)

    if not df_vehicle_stats.empty:
        # 2. KPI GRID (Custom Table Layout)
        st.subheader("Vehicle Metrics Overview")
        
        # Header Row
        h1, h2, h3, h4, h5 = st.columns([1.5, 1, 1, 1, 1])
        h1.write("**Vehicle Type**")
        h2.write("**Total Value**")
        h3.write("**Success Value**")
        h4.write("**Avg Dist**")
        h5.write("**Total Dist**")
        st.divider()

        # Data Rows
        vehicle_list = ["Prime Sedan", "Prime SUV", "Prime Plus", "Mini", "Auto", "Bike", "eBike"]
        for vehicle in vehicle_list:
            row = df_vehicle_stats[df_vehicle_stats['Vehicle_Type'].str.lower() == vehicle.lower()]
            if not row.empty:
                c1, c2, c3, c4, c5 = st.columns([1.5, 1, 1, 1, 1])
                c1.write(f"**{vehicle}**")
                c2.write(f"{row['total_val'].values[0]/1e6:.2f}M")
                c3.write(f"{row['success_val'].values[0]/1e6:.2f}M")
                c4.write(f"{row['avg_dist'].values[0]}")
                c5.write(f"{int(row['total_dist'].values[0]/1000)}K")
        
        st.divider()

        # 3. VISUALIZATION
        st.subheader("📊 Top 5 Vehicle Types by Ride Distance")
        df_top5 = df_vehicle_stats.sort_values(by='total_dist', ascending=False).head(5)
        st.bar_chart(df_top5.set_index("Vehicle_Type")["total_dist"], color=OLA_LIME, horizontal=True)
    else:
        st.info("No vehicle data found for the current filters.")

# =================================================================
#           4. REVENUE ANALYSIS PAGE
# =================================================================
elif page == "Revenue":
    st.title("💰 Revenue Analysis")
    
    # --- KPI Metrics Row ---
    st.subheader("Financial Highlights")
    rev_metrics = run_query(f"""
        SELECT 
            SUM(Booking_Value) as total_rev,
            AVG(Booking_Value) as avg_rev,
            MAX(Booking_Value) as max_rev
        FROM ola_ride_cleaned_file {where}
    """).iloc[0]

    r1, r2, r3 = st.columns(3)
    r1.metric("Total Revenue", f"₹{rev_metrics['total_rev']/1e6:.2f}M")
    r2.metric("Avg Booking Value", f"₹{int(rev_metrics['avg_rev'])}")
    r3.metric("Highest Booking", f"₹{int(rev_metrics['max_rev'])}")

    st.divider()

    # --- ROW 1: Revenue by Payment ---
    st.subheader("Revenue by Payment Method")
    df_payment = run_query(f"SELECT Payment_Method, SUM(Booking_Value) as v FROM ola_ride_cleaned_file {where} GROUP BY 1")
    st.bar_chart(df_payment.set_index("Payment_Method"), color=OLA_LIME)

    st.divider()

    # --- ROW 2: SIDE-BY-SIDE CHARTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Daily Distance Distribution")
        df_daily = run_query(f"SELECT Date, SUM(Ride_Distance) as dist FROM ola_ride_cleaned_file {where} GROUP BY 1 ORDER BY 1")
        if not df_daily.empty:
            st.bar_chart(df_daily.set_index("Date"), color=OLA_LIME)
        else:
            st.info("No distance data available.")

    with col2:
        st.subheader("Top 5 High-Value Customers")
        df_top_cust = run_query(f"SELECT Customer_ID, SUM(Booking_Value) as v FROM ola_ride_cleaned_file {where} GROUP BY 1 ORDER BY 2 DESC LIMIT 5")
        if not df_top_cust.empty:
            st.bar_chart(df_top_cust.set_index("Customer_ID"), color=OLA_LIME)
        else:
            st.info("No customer data available.")


# =================================================================
#           5. CANCELLATION ANALYSIS PAGE
# =================================================================
elif page == "Cancellation":
    st.title("🚫 Cancellation Analysis")

    # --- KPI Metrics Row ---
    st.subheader("Cancellation Overview")
    m1, m2, m3, m4 = st.columns(4)
    
    kpi_q = f"""
        SELECT 
            COUNT(Booking_ID) as total,
            COUNT(CASE WHEN Booking_Status = 'Success' THEN 1 END) as success,
            COUNT(CASE WHEN Booking_Status LIKE '%Canceled%' THEN 1 END) as canceled,
            COUNT(CASE WHEN Incomplete_Rides = 'Yes' THEN 1 END) as incomplete
        FROM ola_ride_cleaned_file {where}
    """
    kpis = run_query(kpi_q).iloc[0]

    m1.metric("Total Bookings", f"{int(kpis['total']/1000)}K")
    m2.metric("Total Success", f"{int(kpis['success']/1000)}K")
    m3.metric("Total Cancelled", f"{int(kpis['canceled']/1000)}K")
    m4.metric("Total Incomplete", f"{int(kpis['incomplete']/1000)}K")

    st.divider()

    # --- Incomplete Rides Section ---
    st.subheader("📝 Incomplete Rides Detail")
    inc_filter = f"{where} AND Incomplete_Rides = 'Yes'" if where else "WHERE Incomplete_Rides = 'Yes'"
    inc_data = run_query(f"SELECT Booking_ID, Customer_ID, Incomplete_Rides_Reason FROM ola_ride_cleaned_file {inc_filter}")

    if not inc_data.empty:
        st.dataframe(inc_data, use_container_width=True)
    else:
        st.info("No incomplete rides found.")

    st.divider()

        # --- Cancellation Reasons Breakdown (Consistent Custom Colors) ---
    col1, col2 = st.columns(2)
    import matplotlib.pyplot as plt

    # Your requested professional color palette
    custom_colors = ['#FF3131', '#FF66B2', "#33B8FF", "#87EB91", '#9932CC', '#8B4513', "#5132CD"]

    with col1:
        st.subheader("📊 Reasons: Canceled by Customer")
        cust_clause = f"{where} AND Booking_Status = 'Canceled by Customer' AND Canceled_Rides_by_Customer <> 'Unknown'" if where else "WHERE Booking_Status = 'Canceled by Customer' AND Canceled_Rides_by_Customer <> 'Unknown'"
        df_cust = run_query(f"SELECT Canceled_Rides_by_Customer as Reason, COUNT(*) as Count FROM ola_ride_cleaned_file {cust_clause} GROUP BY 1 ORDER BY 2 DESC")
        
        if not df_cust.empty:
            fig1, ax1 = plt.subplots(figsize=(5, 5)) 
            # autopct for clear values, startangle for better alignment
            ax1.pie(df_cust['Count'], labels=df_cust['Reason'], 
                    autopct='%1.1f%%', startangle=140, 
                    colors=custom_colors, 
                    textprops={'color':"white", 'fontsize':10, 'fontweight':'bold'})
            
            fig1.patch.set_facecolor('none') # Matches dark theme
            st.pyplot(fig1)
        else:
            st.info("No customer cancellations found.")

    with col2:
        st.subheader("📊 Reasons: Canceled by Driver")
        driv_clause = f"{where} AND Booking_Status = 'Canceled by Driver' AND Canceled_Rides_by_Driver <> 'Unknown'" if where else "WHERE Booking_Status = 'Canceled by Driver' AND Canceled_Rides_by_Driver <> 'Unknown'"
        df_driver = run_query(f"SELECT Canceled_Rides_by_Driver as Reason, COUNT(*) as Count FROM ola_ride_cleaned_file {driv_clause} GROUP BY 1 ORDER BY 2 DESC")
        
        if not df_driver.empty:
            fig2, ax2 = plt.subplots(figsize=(5, 5)) 
            ax2.pie(df_driver['Count'], labels=df_driver['Reason'], 
                    autopct='%1.1f%%', startangle=140, 
                    colors=custom_colors, 
                    textprops={'color':"white", 'fontsize':10, 'fontweight':'bold'})
            
            fig2.patch.set_facecolor('none') # Matches dark theme
            st.pyplot(fig2)
        else:
            st.info("No driver cancellations found.")



# =================================================================
#           6. RATINGS ANALYSIS PAGE
# =================================================================
elif page == "Ratings":
    st.title("⭐ Rating Analysis")

    # --- Vehicle Rating Metrics ---
    df_ratings = run_query(f"SELECT Vehicle_Type, ROUND(AVG(Customer_Rating), 2) as cust_avg, ROUND(AVG(Driver_Ratings), 2) as drv_avg FROM ola_ride_cleaned_file {where} GROUP BY 1")

    st.subheader("Avg Customer Rating (Per Vehicle)")
    if not df_ratings.empty:
        cols = st.columns(7)
        vehicle_order = ["Prime Sedan", "Prime SUV", "Prime Plus", "Mini", "Auto", "Bike", "eBike"]
        for i, v_name in enumerate(vehicle_order):
            row = df_ratings[df_ratings['Vehicle_Type'].str.lower() == v_name.lower()]
            val = row['cust_avg'].values[0] if not row.empty else "-"
            cols[i].metric(v_name, val)

    st.divider()

    # --- Distribution Row ---
    st.subheader("📊 Rating Distribution Analysis")
    c1, c2 = st.columns(2)

    with c1:
        st.write("**Customer Rating Frequency**")
        df_c = run_query(f"SELECT Customer_Rating as Rating, COUNT(*) as Count FROM ola_ride_cleaned_file {where} GROUP BY 1")
        st.bar_chart(df_c.set_index("Rating"), color=OLA_LIME)

    with c2:
        st.write("**Driver Rating Frequency**")
        df_d = run_query(f"SELECT Driver_Ratings as Rating, COUNT(*) as Count FROM ola_ride_cleaned_file {where} GROUP BY 1")
        st.bar_chart(df_d.set_index("Rating"), color=OLA_LIME)

    st.divider()

    # --- Horizontal Summary ---
    st.subheader("Avg Customer Rating by Category")
    st.bar_chart(df_ratings.set_index("Vehicle_Type")["cust_avg"], color=OLA_LIME, horizontal=True)
