import streamlit as st
import base64

# =================================================================
# 1. PAGE CONFIG
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics | Power BI", layout="wide")

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
if logo_base64:
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
    <div class="sub-title">📊 Power BI Interactive Dashboard</div>
</div>
""", unsafe_allow_html=True)

# =================================================================
# 6. POWER BI CONTENT
# =================================================================

# Updated Power BI Embed URL
pbi_url = "https://app.powerbi.com/reportEmbed?reportId=05950598-9e8b-4e9e-9a57-57cf1e7cbe0e&autoAuth=true&ctid=f3c9ebc3-0543-43d8-9cac-9db513a7c000"

# Embed the dashboard
st.components.v1.iframe(pbi_url, height=850, scrolling=True)

# Full tab link
st.markdown(f"""
    <div style="text-align: center; margin-top: 15px;">
        <a href="{pbi_url}" target="_blank" style="color: #D2EF1A; text-decoration: none; font-weight: 600; font-size: 16px;">
            🔗 Open Dashboard in Full Screen Tab
        </a>
    </div>
""", unsafe_allow_html=True)
