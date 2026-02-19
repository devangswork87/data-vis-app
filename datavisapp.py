import pandas as pd
import streamlit as st

if "visulaise" not in st.session_state:
    st.session_state.visulaise = False


def visgen():
    st.session_state.visulaise = True


def reset_all():
    st.session_state.visulaise = False


st.title("📊 Built-in Data Viz")
file_uploade = st.file_uploader("Upload your file here:", type="csv")

if file_uploade is not None:
    try:
        df = pd.read_csv(file_uploade)
        original_rows = len(df)
        df = df.drop_duplicates()
        df = df.dropna()
        cleaned_rows = len(df)

        if cleaned_rows != original_rows:
            st.info( f"🧹 Cleaned {original_rows - cleaned_rows} problematic rows. {cleaned_rows} rows remaining.") # fmt:skip

        cols = df.columns.tolist()
        x_label = st.selectbox("Pick the X column (Labels):", cols)
        y_label = st.multiselect("Pick the Y columns (Values):", cols)

        st.button("Visualise your data:", on_click=visgen)

        if st.session_state.visulaise:
            st.divider()
            if y_label:
                if x_label in y_label:
                    st.warning("X and Y columns can't be the same! Pick different columns.")# fmt:skip
                else:
                    non_numeric = [
                        col
                        for col in y_label
                        if not pd.api.types.is_numeric_dtype(df[col])
                    ]
                    if non_numeric:
                        st.warning(f"These columns are not numeric and can't be plotted: {non_numeric}")  # fmt: skip
                        st.snow()
                    else:
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
