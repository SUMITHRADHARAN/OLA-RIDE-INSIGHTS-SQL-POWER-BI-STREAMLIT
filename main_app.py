import streamlit as st
import base64
import os


# =================================================================
# 1. PAGE CONFIG (Must be the first Streamlit command)
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics", layout="wide")

# =================================================================
# 2. HELPER FUNCTION & ASSETS
# ================================================================

def get_base64_image(image_path):
    try:
        # Check if file exists to avoid errors
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        return ""
    except Exception as e:
        return ""

# FIX: Use a relative path for GitHub deployment
current_dir = os.path.dirname(__file__)
logo_path = os.path.join(current_dir, "ola.png")

logo_base64 = get_base64_image(logo_path)

# =================================================================
# 3. SIDEBAR LOGO
# =================================================================
if logo_base64:
    # Use the relative path directly here
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.error("Logo file 'ola.png' not found in GitHub repository.")


# =================================================================
# 4. CUSTOM STYLING (Poppins Font & Neon Flexbox Box)
# =================================================================
st.markdown(f"""
    <style>
    /* Importing Poppins correctly from Google Fonts */
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] {{ 
        font-family: 'Poppins', sans-serif; 
    }}

    /* Styled Container for Logo + Title */
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
        margin: 10px 0px 30px 0px;
    }}

    .logo-img {{
        height: 70px; 
    }}

    .ola-text {{
        font-family: 'Poppins', sans-serif;
        font-size: 40px; 
        color: #D2EF1A; 
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0;
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
# 5. BRANDING HEADER (Developer Info + Neon Box)
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
""", unsafe_allow_html=True)

# =================================================================
# 6. PAGE CONTENT
# =================================================================
st.markdown("### 🚕 Welcome to the Bengaluru Ride-Hailing Analysis Portal")
st.write("""
This application provides a comprehensive look into Bengaluru’s ride-hailing patterns using 
**SQL**, **Power BI**, and **Streamlit**. Explore data-driven insights regarding demand, 
cancellations, and revenue performance.
""")

st.markdown("""
**Use the sidebar to navigate through:**
1. **Project Summary:** Objectives and Dataset Overview.
2. **SQL Queries:** Technical data extraction and results.
3. **PowerBI View:** Interactive visual dashboards.
4. **Streamlit UI:** Live filtering and database metrics.
5. **EDA & Conclusion:** Key findings and final project summary.
""")

st.divider()
st.info("👈 **Select a page from the sidebar to begin.**")
