limport pandas as pd
import streamlit as st
from sklearn.linear_model import LinearRegression


def data_vis_engine(file_uploaded,key="visualise"):
    try:
        if key not in st.session_state:
            st.session_state[key] = False
        
        def visgen():
            st.session_state[key] = True


        def reset_all():
            st.session_state[key] = False 

        df = pd.read_csv(file_uploaded)
        original_rows = len(df)
        df = df.drop_duplicates()
        df = df.dropna()
        cleaned_rows = len(df)
        st.dataframe(df.head()) 

        if cleaned_rows != original_rows:
            st.info(f"🧹 Cleaned {original_rows - cleaned_rows} problematic rows. {cleaned_rows} rows remaining.")

        cols = df.columns.tolist()
        x_label = st.selectbox("Pick the X column (Labels):", cols)
        y_label = st.multiselect("Pick the Y columns (Values):", cols)

        st.button("Visualise your data:", on_click=visgen)

        if st.session_state[key]:
            st.divider()
            if y_label:
                if x_label in y_label:
                    st.warning("X and Y columns can't be the same! Pick different columns.")# fmt:skip
                else:
                    non_numeric = [col for col in y_label if not pd.api.types.is_numeric_dtype(df[col])]
                    if non_numeric:
                        st.warning(f"These columns are not numeric and can't be plotted: {non_numeric}")  # fmt: skip
                        st.info("Select a numeric column for y axis")
                    else:
                        st.subheader("Visualising your data...")
                        tab1, tab2, tab3 = st.tabs(["Bar graph", "Line graph","Scatter graph"])
                        chart_data = df.set_index(x_label)[y_label]
                        with tab1:
                            st.bar_chart(chart_data)
                        with tab2:
                            st.line_chart(chart_data)
                        
                        with tab3:
                            st.scatter_chart(chart_data)
                        st.button("RESET", on_click=reset_all)
                       
            else:
                st.warning("Pick at least one Y column to see the magic!")
    except pd.errors.ParserError:
        st.error("Could not parse the file. Make sure it's a valid CSV.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")




