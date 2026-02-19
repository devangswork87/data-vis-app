import pandas as pd
import streamlit as st
if 'visulaise'not in st.session_state:
    st.session_state.visulaise = False


def visgen():
    st.session_state.visulaise = True


def reset_all():
    st.session_state.visulaise = False


st.title("📊 Built-in Data Viz")
file_uploade = st.file_uploader("upload your file here:", type="csv")
if file_uploade is not None:

    try:
        df = pd.read_csv(file_uploade)
        cols = df.columns.tolist()
        x_label = st.selectbox("Pick the X column (Labels):", cols)
        y_label = st.multiselect("Pick the Y columns (Values):", cols)

        st.button("Visulaise your data:", on_click=visgen)
        if st.session_state.visulaise:

            st.divider()
            if y_label:

                st.subheader("Visualising your data...")
                tab1, tab2 = st.tabs(["Bar graph", "Line graph"])
                chart_data = df.set_index(x_label)[y_label]
                with tab1:

                    st.bar_chart(chart_data)
                with tab2:
                    st.line_chart(chart_data)
                st.button("RESET", on_click=reset_all)
            else:

                st.warning("Pick at least one Y column to see the magic!")
                st.snow()
    except Exception as e:
        st.error(f"Could not read your file: {e}")
