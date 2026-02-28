import pandas as pd
import streamlit as st
from V1_datavis import data_vis_engine as dse
st.title("📊 Built-in Data Viz")
file_uploaded = st.file_uploader("Upload a CSV file")
if file_uploaded is not None:
    dse(file_uploaded)

    

