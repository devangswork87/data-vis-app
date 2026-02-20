import streamlit as st
import pandas as pd
st.title("🧪 Sample Test")
st.write("Try this app with sample data!")
sample_data = { "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Sales": [1500, 2300, 1800, 2700, 3100, 2900], "Expenses": [1200, 1800, 1400, 2100, 2400, 2200], "Profit": [300, 500, 400, 600, 700, 700]}
df=pd.DataFrame(sample_data)
st.subheader("Sample Data:")
pd.DataFrame(df)
st.divider()
cols = df.columns.tolist()
x_label = st.selectbox("Pick the X column (Labels):", cols)
y_label = st.multiselect("Pick the Y columns (Values):", cols)
if st.button("Visualise your data:"):
    st.subheader("Visualising your data...")
    tab1, tab2 = st.tabs(["Bar graph", "Line graph"])
    chart_data = df.set_index(x_label)[y_label]
    with tab1:
        st.bar_chart(chart_data)
    with tab2:
        st.line_chart(chart_data)
    
