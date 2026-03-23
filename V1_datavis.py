import pandas as pd
import streamlit as st
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import altair as alt


def data_vis_engine(file_uploaded, key="visualise"):
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
                    st.warning("X and Y columns can't be the same! Pick different columns.")
                else:
                    non_numeric = [col for col in y_label if not pd.api.types.is_numeric_dtype(df[col])]
                    if non_numeric:
                        st.warning(f"These columns are not numeric and can't be plotted: {non_numeric}")
                        st.info("Select a numeric column for y axis")
                    else:
                        st.subheader("Visualising your data...")
                        tab1, tab2, tab3, tab4 = st.tabs(["Bar graph", "Line graph", "Scatter graph", "📈 ML: Linear Regression"])
                        chart_data = df.set_index(x_label)[y_label]

                        with tab1:
                            st.bar_chart(chart_data)

                        with tab2:
                            st.line_chart(chart_data)

                        with tab3:
                            st.scatter_chart(chart_data)

                        # ── ML TAB ──────────────────────────────────────────
                        with tab4:
                            st.markdown("### 📈 Linear Regression — Trend Predictor")
                            st.write("Uses **scikit-learn** to fit a regression line and forecast future values.")

                            # Only works when X is numeric
                            if not pd.api.types.is_numeric_dtype(df[x_label]):
                                st.info("💡 Linear Regression needs a **numeric X column** (e.g. year, index, temperature). "
                                        "Your current X column is text-based. Try picking a numeric column as X.")
                            else:
                                # Pick one Y column for regression
                                reg_y = st.selectbox(
                                    "Pick ONE Y column to regress on:",
                                    y_label,
                                    key="reg_y_select"
                                )

                                X = df[[x_label]].values
                                y = df[reg_y].values

                                # Fit model
                                model = LinearRegression()
                                model.fit(X, y)
                                y_pred = model.predict(X)

                                r2 = r2_score(y, y_pred)
                                rmse = np.sqrt(mean_squared_error(y, y_pred))

                                # ── Model stats ──
                                col1, col2, col3 = st.columns(3)
                                col1.metric("R² Score", f"{r2:.4f}", help="Closer to 1.0 = better fit")
                                col2.metric("RMSE", f"{rmse:.2f}", help="Root Mean Squared Error — lower is better")
                                col3.metric("Slope (m)", f"{model.coef_[0]:.4f}")
                                st.caption(f"**Equation:** {reg_y} = {model.coef_[0]:.4f} × {x_label} + {model.intercept_:.4f}")

                                # ── Forecast section ──
                                st.markdown("#### 🔮 Predict Future Values")
                                x_min = float(df[x_label].min())
                                x_max = float(df[x_label].max())
                                x_range = x_max - x_min

                                future_x = st.number_input(
                                    f"Enter a value for **{x_label}** to predict **{reg_y}**:",
                                    value=round(x_max + x_range * 0.1, 2)
                                )
                                predicted_val = model.predict([[future_x]])[0]
                                st.success(f"📌 Predicted **{reg_y}** at {x_label} = **{future_x}** → **{predicted_val:.2f}**")

                                # ── Chart: actual vs regression line ──
                                st.markdown("#### 📊 Actual vs Regression Line")

                                # Extend line slightly beyond data for visual effect
                                x_extended = np.linspace(x_min - x_range * 0.05, x_max + x_range * 0.1, 200).reshape(-1, 1)
                                y_line = model.predict(x_extended)

                                actual_df = pd.DataFrame({
                                    x_label: df[x_label].values,
                                    reg_y: y,
                                    "type": "Actual"
                                })

                                line_df = pd.DataFrame({
                                    x_label: x_extended.flatten(),
                                    reg_y: y_line,
                                    "type": "Regression Line"
                                })

                                combined = pd.concat([actual_df, line_df], ignore_index=True)

                                scatter = alt.Chart(actual_df).mark_circle(size=80, opacity=0.8).encode(
                                    x=alt.X(x_label, title=x_label),
                                    y=alt.Y(reg_y, title=reg_y),
                                    color=alt.value("#FF4B4B"),
                                    tooltip=[x_label, reg_y]
                                )

                                line = alt.Chart(line_df).mark_line(strokeWidth=2.5).encode(
                                    x=alt.X(x_label),
                                    y=alt.Y(reg_y),
                                    color=alt.value("#00C8FF")
                                )

                                # Future point
                                future_point_df = pd.DataFrame({x_label: [future_x], reg_y: [predicted_val]})
                                future_mark = alt.Chart(future_point_df).mark_point(
                                    shape="diamond", size=200, filled=True
                                ).encode(
                                    x=alt.X(x_label),
                                    y=alt.Y(reg_y),
                                    color=alt.value("#FFD700"),
                                    tooltip=[x_label, reg_y]
                                )

                                chart = (scatter + line + future_mark).properties(height=400).interactive()
                                st.altair_chart(chart, use_container_width=True)

                                st.caption("🔴 Actual data  |  🔵 Regression line  |  🟡 Your predicted point")

                                # ── Interpretation ──
                                st.markdown("#### 🧠 What does this mean?")
                                if r2 >= 0.85:
                                    quality = "**Strong fit** ✅ — the model explains the data well."
                                elif r2 >= 0.5:
                                    quality = "**Moderate fit** ⚠️ — some trend is captured but there's noise."
                                else:
                                    quality = "**Weak fit** ❌ — the data may not follow a linear trend."

                                direction = "increases" if model.coef_[0] > 0 else "decreases"
                                st.info(
                                    f"{quality}\n\n"
                                    f"For every 1-unit increase in **{x_label}**, "
                                    f"**{reg_y}** {direction} by **{abs(model.coef_[0]):.4f}**."
                                )

                        st.button("RESET", on_click=reset_all)

            else:
                st.warning("Pick at least one Y column to see the magic!")

    except pd.errors.ParserError:
        st.error("Could not parse the file. Make sure it's a valid CSV.")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
