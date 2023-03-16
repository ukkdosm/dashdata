import streamlit as st
import pandas as pd
import altair as alt

# Create a title and subtitle for the app
st.title("My Streamlit App")
st.subheader("A Simple Chart")

# Load some sample data
df = pd.read_csv("https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.csv")

# Create a chart using Altair
chart = alt.Chart(df).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    tooltip=['Name', 'Horsepower', 'Miles_per_Gallon']
).interactive()

# Display the chart in the Streamlit app
st.altair_chart(chart, use_container_width=True)
