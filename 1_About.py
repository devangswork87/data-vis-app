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
* **Auto-Magic Cleaning:** I’ll scrub those messy duplicates and empty rows for you.
* **Pick & Plot:** Just select your X and Y axes; no coding required.
* **Visuals that Pop:** Switch between Bar and Line charts instantly.
* **Crash-Proof:** I’ve added some defensive logic so the app won't freak out if your data is weird.
""")

st.divider()

st.subheader("🧰 The Toolkit")
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


st.info("Built with late-night coffee and a lot of debugging. ☕✨")



