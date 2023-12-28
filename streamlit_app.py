from pathlib import Path
import json
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.let_it_rain import rain
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from vnstock import * #import all functions, including functions that provide OHLC data for charting
from vnstock.chart import *
from datetime import datetime, timedelta
from vnstock import * #import all functions
from tvDatafeed import TvDatafeed, Interval
from vnstock_data.trading_insights import *
from vnstock_data.ohlc import *
from plotly.subplots import make_subplots
st.set_page_config(layout="wide")

# Directories and file paths
THIS_DIR = Path(__file__).parent
CSS_FILE = THIS_DIR / "style" / "style.css"
ASSETS = THIS_DIR / "assets"
LOTTIE_ANIMATION = ASSETS / "animation_holiday.json"


# Function to load and display the Lottie animation
def load_lottie_animation(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


# Function to apply snowfall effect
def run_snow_animation():
    rain(emoji="⚽", font_size=20, falling_speed=8, animation_length="infinite")


# Function to get the name from query parameters
def get_person_name():
    query_params = st.experimental_get_query_params()
    return query_params.get("name", ["Friend"])[0]


# Page configuration")

# Run snowfall animation
run_snow_animation()

# Apply custom CSS
with open(CSS_FILE) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Display header with personalized name
PERSON_NAME = get_person_name()
st.header(f"Happy Holidays, {PERSON_NAME}! 🎄", anchor=False)

# Display the Lottie animation
lottie_animation = load_lottie_animation(LOTTIE_ANIMATION)
st_lottie(lottie_animation, key="lottie-holiday", height=300)

# Personalized holiday message
st.markdown(
    f"Dear {PERSON_NAME}, wishing you a wonderful holiday season filled with joy and peace. 🌟"
)