import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Exploring Happiness Factors")

option_x = st.selectbox("Select data for the X-axis:", ("GDP", "Happiness", "Generosity"))
option_y = st.selectbox("Select data for the Y-axis:", ("GDP", "Happiness", "Generosity"))

dataframe = pd.read_csv("happy.csv")

x_column = None
match option_x:
    case "Happiness":
        x_column = "happiness"
    case "GDP":
        x_column = "gdp"
    case "Generosity":
        x_column = "generosity"

y_column = None
match option_y:
    case "Happiness":
        y_column = "happiness"
    case "GDP":
        y_column = "gdp"
    case "Generosity":
        y_column = "generosity"

st.subheader(f"Scatter Plot of {option_x} vs {option_y}")

figure1 = px.scatter(dataframe, x=x_column, y=y_column, labels={"x": option_x, "y": option_y},
                     hover_data={"country": True, "happiness": True, "gdp": True, "generosity": True},
                     title=f"{option_x} vs {option_y} with Additional Data")

st.plotly_chart(figure1)

st.write("Additional Data:")
reversed_dataframe = dataframe.sort_values(by="happiness", ascending=False)
st.dataframe(reversed_dataframe)

