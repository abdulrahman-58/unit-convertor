import streamlit as st
import pandas as pd
import requests
from pint import UnitRegistry

# Initialize Pint Unit Registry
ureg = UnitRegistry()
Q_ = ureg.Quantity  # Shortcut for easier usage

# Streamlit App Title
st.title("🔄 Advanced Unit Converter")

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")

# Apply Dark Mode if enabled
if dark_mode:
    st.markdown(
        """
        <style>
            html, body, [class*="st"] {
                background-color: #121212;
                color: white;
            }
            .stSelectbox, .stNumber_input, .stButton {
                background-color: #333;
                color: white;
                border-radius: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Unit Categories
categories = {
    "Length": ["meter", "kilometer", "mile", "yard", "foot", "inch"],
    "Weight": ["gram", "kilogram", "pound", "ounce"],
    "Temperature": ["degC", "degF", "kelvin"],
    "Speed": ["meter/second", "kilometer/hour", "mile/hour"]
}

# Select Category
category = st.selectbox("Select a Category", list(categories.keys()))

# Select Units
unit_options = categories[category]
from_unit = st.selectbox("From Unit", unit_options)
to_unit = st.selectbox("To Unit", unit_options)
value = st.number_input("Enter Value", value=1.0, step=0.1)

# Initialize session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Perform Conversion
if st.button("Convert"):
    try:
        # Convert using Pint
        result = Q_(value, from_unit).to(to_unit)
        converted_value = result.magnitude
        converted_unit = result.units

        st.success(f"✅ {value} {from_unit} = {converted_value} {converted_unit}")

        # Store structured data instead of a single string
        st.session_state.history.append([value, from_unit, converted_value, str(converted_unit)])
    except Exception as e:
        st.error(f"⚠️ Conversion error: {e}")

# Show Conversion History
st.sidebar.header("📜 Conversion History")
for item in st.session_state.history[-5:]:  # Show last 5 conversions
    st.sidebar.write(" | ".join(map(str, item)))

# Export Results to CSV
def save_to_csv():
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history, columns=["Value", "From Unit", "Converted Value", "To Unit"])
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.sidebar.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="conversion_results.csv",
            mime="text/csv",
        )

# Automatically show the download button if history exists
save_to_csv()
