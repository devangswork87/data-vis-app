import streamlit as st
# Set a cool page config
st.set_page_config(page_title="Data Viz Pro", page_icon="📈")
st.title("📊 Data Viz, Simplified")
st.subheader("I'm Devang! 👋")

st.write("""
I'm a Class 12 student out of Jaipur, just trying to make data less of a headache. 
I built this because let's be real—nobody has time to manually clean CSVs and fight 
with Matplotlib code all day.
""")

st.divider()

st.subheader("🚀 The Game Plan")
st.write("""
Drop a file and let the app do the heavy lifting:
* **Automatic Data Cleaning:** Drops empty rows and removes duplicates so you don't have to open Excel.
* **Easy Axis Selection:** Select your X and Y axes from a dropdown and see the result instantly.
* **Multiple Chart Options:** Switch between Bar , Line charts and Scatter charts instantly.
* **Error Handling:** Added some logic to catch common formatting errors so the app doesn't crash on 'weird' files.
""")

st.divider()

st.subheader("How I built It and what I used")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Language:** Python 🐍")
with col2:
    st.markdown("**UI:** Streamlit 🎈")
with col3:
    st.markdown("**Logic:** Pandas 🐼")

st.divider()

st.subheader("🔗 Let's Connect")
st.write("Source Code: [GitHub](https://github.com/devangswork87/data-vis-app)")
st.write("Try it out: [Live App](https://data-vis-app.streamlit.app/)")


st.info("A project born from the curiosity of a 16-year-old who just wanted a better way to look at data.")



