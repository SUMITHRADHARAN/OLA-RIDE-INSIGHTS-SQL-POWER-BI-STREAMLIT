import streamlit as st
import base64
from pathlib import Path

# =================================================================
# 1. PAGE CONFIG
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics | Project Summary", layout="wide")

# =================================================================
# 2. PATHS & IMAGE ENCODING
# =================================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# Get the absolute path to the directory this script is in (the 'pages' folder)
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()

# Move up to root directory to find the image
root_dir = current_dir.parent 
logo_path = root_dir / "ola.png"

# --- THE FIX: Create the missing variable ---
logo_base64 = get_base64_image(logo_path)

# =================================================================
# 3. SIDEBAR LOGO
# =================================================================
if logo_path.exists():
    # Use the variable you just created
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.sidebar.warning("Logo file 'ola.png' not found.")

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
    <div class="sub-title">📝 Project Summary & Dataset Overview</div>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. PROJECT CONTENT
# =================================================================

with st.container():
    st.markdown("""
    ### **Introduction**
    The **Ola Ride Data Analysis** project is an end-to-end data initiative designed to analyze ride patterns, customer behavior, and operational efficiency. By transforming raw ride data into actionable intelligence, this project helps optimize pricing strategies and enhance service delivery.
    
    ### **The Tech Stack**
    *   **SQL:** Used for robust data cleaning and complex querying of booking trends.
    *   **Power BI:** Utilized for high-level visual reporting and KPI tracking.
    *   **Streamlit:** Provides an interactive web interface to explore findings in real-time.
    
    ### **Key Objectives**
    *   **Identify Demand:** Tracking peak hours and popular vehicle categories.
    *   **Operational Insights:** Analyzing cancellation reasons and booking success rates.
    *   **Customer Trends:** Evaluating rating distributions and preferred payment methods.
    """)

st.divider() 

# Problem Statement & Objectives Section
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🎯 Problem Statement")
    st.write("""
    Effectively utilizing vast ride data for strategic improvements is challenging. This project:
    - Analyzes ride data for actionable insights.
    - Develops a complete data pipeline (Cleaning -> EDA -> Visualization).
    - Provides a Power BI & Streamlit ecosystem for monitoring.
    """)

with col_b:
    st.subheader("📍 Objectives")
    st.markdown("""
    - Analyze customer preferences.
    - Identify peak hours & popular routes.
    - Evaluate driver performance.
    - Determine pricing & revenue factors.
    - Optimize operational strategies.
    """)

st.header("🛠️ Project Approach")

with st.expander("Step 1: Data Understanding & Exploration"):
    st.markdown("- Load and examine dataset structure.\n- Identify key variables (status, payment, ratings).\n- Perform initial EDA.")

with st.expander("Step 2: Data Cleaning & Preprocessing"):
    st.markdown("- Handle missing values.\n- Standardize formats/types.\n- Create derived features.")

with st.expander("Step 3: SQL Query Development"):
    st.markdown("- Extract trends and cancellations.\n- Optimize for performance.\n- Validate results.")

with st.expander("Step 4: Power BI Dashboard Creation"):
    st.markdown("- Design interactive visuals.\n- Use dynamic slicers.\n- Integrate business KPIs.")

with st.expander("Step 5: Streamlit Application Development"):
    st.markdown("- Create user-friendly UI.\n- Implement interactive filters.\n- Embed Power BI visuals.")

# Dataset Overview Section
st.header("📊 Dataset Overview")
st.info("**Scope:** 103,025 rows of ride-booking data for **Bengaluru** over one month.")

tab1, tab2 = st.tabs(["🚗 Ride Details", "⚙️ Operational Metrics"])

with tab1:
    st.markdown("""
    - **Booking ID:** Unique identifier prefixed by "CNR".
    - **Booking Status:** Successful or Cancelled.
    - **Vehicle Type:** Auto, Prime Plus, etc.
    - **Locations:** 50 dummy areas in Bengaluru.
    - **Ride Distance:** Distance in kilometers.
    - **Booking Value:** Total fare amount.
    """)

with tab2:
    st.markdown("""
    - **Avg VTAT/CTAT:** Vehicle and Customer arrival times.
    - **Cancellations:** Reasons provided by both Customers and Drivers.
    - **Incomplete Rides:** Breakdowns or specific demands.
    - **Ratings:** Feedback scores for both parties.
    - **Payment Method:** Cash, UPI, Card, or Wallet.
    """)
