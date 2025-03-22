import streamlit as st
import pandas as pd
import altair as alt

st.title("My Boss's Year-wise Salary Growth (in Lacs)")

# Choose the years for which you want to input increments
years = list(range(2014, 2026))  # 2014 through 2025

# 1) USER INPUTS
# -----------------------------------------------------------------------------
st.subheader("Initial Input")
initial_salary = st.number_input(
    "Enter the initial salary for 2014 (in Lacs):",
    value=8.5,  # Default
    min_value=0.0,
    step=0.1
)

st.write("---")  # Just a separator line in the UI

# 2) GET INCREMENTS FOR EACH YEAR
# -----------------------------------------------------------------------------
st.subheader("Year-wise Increment (%)")
yearly_increments = {}
for year in years:
    yearly_increments[year] = st.number_input(
        f"{year}:",
        value=8,  # Default
        min_value=0,
        max_value=100,
        step=1
    )

# 3) CALCULATE PACKAGE & POST-INCREMENT (ALL IN LACS)
# -----------------------------------------------------------------------------
records = []
current_package = initial_salary

for yr in years:
    inc_pct = yearly_increments[yr]
    post_inc = current_package * (1 + inc_pct / 100.0)
    records.append([
        yr,
        round(current_package, 2),  # Package (Lacs)
        inc_pct,                   # Increment %
        round(post_inc, 2)         # Post Increment (Lacs)
    ])
    # Next year's base becomes this year's post-increment
    current_package = post_inc

df = pd.DataFrame(
    records,
    columns=["Year", "Package (Lacs)", "Increment (%)", "Post Increment (Lacs)"]
)

# Convert Year to string for cleaner labeling in Altair
df["Year"] = df["Year"].astype(str)

st.write("---")

# 4) VISUALIZATIONS
# -----------------------------------------------------------------------------
st.subheader("Visualizations")

# A) LINE CHART: Package vs. Post Increment
line_chart = (
    alt.Chart(df)
    .transform_fold(
        fold=["Package (Lacs)", "Post Increment (Lacs)"],
        as_=["Type", "Value"]
    )
    .mark_line(point=True)
    .encode(
        x=alt.X("Year:N", sort=None, title="Year"),
        y=alt.Y("Value:Q", title="Salary (Lacs)"),
        color=alt.Color("Type:N", title="Metric"),
        tooltip=["Year:N", "Type:N", "Value:Q"]
    )
    .properties(title="Package vs. Post Increment", width=600)
)

st.altair_chart(line_chart, use_container_width=True)

# B) BAR CHART: Year-wise increment (%)
bar_chart_increment = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Year:N", sort=None, title="Year"),
        y=alt.Y("Increment (%):Q", title="Increment (%)"),
        tooltip=["Year:N", "Increment (%):Q"]
    )
    .properties(title="Year-wise Increment (%)", width=600)
)

st.altair_chart(bar_chart_increment, use_container_width=True)

# C) BAR CHART: Final "Post Increment (Lacs)" each year
bar_chart_final_salary = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("Year:N", sort=None, title="Year"),
        y=alt.Y("Post Increment (Lacs):Q", title="Final Salary (Lacs)"),
        tooltip=["Year:N", "Post Increment (Lacs):Q"]
    )
    .properties(title="Final Salary (Post Increment)", width=600)
)

st.altair_chart(bar_chart_final_salary, use_container_width=True)

# 5) DATA TABLE
# -----------------------------------------------------------------------------
st.subheader("Data Table")
st.dataframe(df)