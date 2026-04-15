import streamlit as st
import base64

# =================================================================
# 1. PAGE CONFIG
# =================================================================
st.set_page_config(page_title="OLA Ride Analytics | EDA & Conclusion", layout="wide")

# =================================================================
# 2. ASSETS & IMAGE ENCODING
# =================================================================
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception: return ""

logo_path = r"C:\Users\dhara\Documents\Interns\Labmentix\2. Ola Ride insights\ola.png"
logo_base64 = get_base64_image(logo_path)
OLA_LIME = "#D2EF1A"

# =================================================================
# 3. CUSTOM STYLING (Poppins Medium & Table Design)
# =================================================================
st.markdown(f"""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"], .stMarkdown p {{ 
        font-family: 'Poppins', sans-serif; 
        font-weight: 500; 
    }}

    /* Branding Header Styling */
    .title-box {{
        display: flex; align-items: center; justify-content: center; gap: 30px; 
        padding: 25px; background-color: #121821; border-radius: 15px; 
        border: 5px solid {OLA_LIME}; box-shadow: 0px 0px 20px rgba(210, 239, 26, 0.4);
        margin: 10px 0px 20px 0px;
    }}
    .ola-text {{ font-size: 40px; color: {OLA_LIME}; font-weight: 800; text-transform: uppercase; margin: 0; }}
    .sub-title {{ font-size: 24px; color: #ffffff; font-weight: 600; border-bottom: 3px solid {OLA_LIME}; display: inline-block; }}
    .dev-info {{ text-align: right; color: white; }}

    /* Custom Data Table for Column 2 */
    .eda-table {{
        width: 100%; border-collapse: collapse; background-color: #121821;
        border-radius: 10px; overflow: hidden; color: white;
    }}
    .eda-table th {{ background-color: #1c242d; padding: 15px; text-align: left; border-bottom: 2px solid {OLA_LIME}; }}
    .eda-table td {{ padding: 15px; border-bottom: 1px solid #2c343d; vertical-align: top; font-size: 15px; }}
    .cat-col {{ color: {OLA_LIME}; font-weight: 600; width: 30%; }}
    </style>
""", unsafe_allow_html=True)

# =================================================================
# 4. BRANDING HEADER
# =================================================================
st.markdown(f"""
<div class="dev-info"><b>Name: SUMITHRA D</b><br>Roll Number: 28552 | BATCH: E332</div>
<div class="title-box">
    <img src="data:image/png;base64,{logo_base64}" height="70px">
    <h1 class="ola-text">OLA RIDE INSIGHTS</h1>
</div>
<div style="text-align: center; margin-bottom: 30px;"><div class="sub-title">📑 EDA & Conclusion</div></div>
""", unsafe_allow_html=True)

# =================================================================
# 5. SIDEBAR
# =================================================================
st.sidebar.image(logo_path, use_container_width=True)

# =================================================================
# 6. MAIN CONTENT - TWO COLUMN LAYOUT
# =================================================================
st.header("Exploratory Data Analysis:")
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown(f"<h2 style='color:{OLA_LIME};'>🔍 Qualitative Analysis</h2>", unsafe_allow_html=True)
    
    st.subheader("👤 Customer Behavior Analysis:")
    st.write("• The most active customers book multiple rides per day, with some completing over 50 rides per month.")
    st.write("• The busiest hours for bookings are between 6 PM and 9 PM.")
    st.write("• The top 5 customers collectively booked over 1,200 rides.")
    st.write("• Weekend rides saw a 15% increase compared to weekdays.")

    st.subheader("🏎️ Driver Performance Analysis:")
    st.write("• Out of 103,025 bookings, approximately 62% were successfully completed.")
    st.write("• 18,434 bookings were canceled by customers.")
    st.write("• Driver cancellations: 65% personal reasons, 35% vehicle issues.")

    st.subheader("💰 Revenue Insights:")
    st.write("• Avg fare: Short (<5km) ₹120 | Med (5-15km) ₹250 | Long (>15km) ₹600+.")
    st.write("• Payment: 45% Digital, 30% UPI/Cash, 25% Cards.")
    st.write("• Surge pricing applied to 12% of rides, increasing fares by 35%.")

    st.subheader("⚙️ Operational Efficiency:")
    st.write("• Peak hours (6 PM - 9 PM) require maximum driver availability.")
    st.write("• Rush hour rides took 25% longer than off-peak times.")

with col2:
    st.markdown(f"<h2 style='color:{OLA_LIME};'>📊 Quantitative Data Summary</h2>", unsafe_allow_html=True)
    
    # Custom HTML Table based on your provided image
    st.markdown(f"""
    <table class="eda-table">
        <tr><th>Category</th><th>Details</th></tr>
        <tr>
            <td class="cat-col">Volume & Revenue</td>
            <td>Total Rides: 103,000; Total Booking Value: 57,000,000; Successfully Completed Rides: 64,000; Daily Ride Volume: 3,200-3,400 rides/day</td>
        </tr>
        <tr>
            <td class="cat-col">Cancellations & Issues</td>
            <td>Driver Cancellations: 18,000; Customer Cancellations: 10,000; Driver Not Found: 10,000; Operational Issues: 10,000+; Non-successful Bookings: 28,000</td>
        </tr>
        <tr>
            <td class="cat-col">Ratings & Satisfaction</td>
            <td>Average Customer Rating: 4.0; Prime Plus: 4.01; Prime Sedan: 4.00; Bike/eBike: 3.99</td>
        </tr>
        <tr>
            <td class="cat-col">Payment Methods</td>
            <td>Cash: 19,000,000; UPI: 14,000,000; Credit Card: 1,000,000; Debit Card: ~0</td>
        </tr>
        <tr>
            <td class="cat-col">Operational Distance</td>
            <td>Peak Daily Distance: 51,000 km/day; Prime Sedan: 235,000 km; eBike: 231,000 km</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

st.divider()

# =================================================================
# 7. CONCLUSION & SUMMARY
# =================================================================
st.header("💡 CONCLUSION:")
st.markdown("""
* **Better driver scheduling** is required during peak hours to reduce wait times.
* **Incentives for top-rated drivers** could improve service quality.
* **Predictive maintenance** can reduce incomplete rides due to vehicle issues.
""")

st.success("**Overall Summary:** This project analyzed Bengaluru’s ride-hailing patterns using SQL and Power BI to derive actionable insights on booking trends and revenue metrics.")
