import streamlit as st
import pandas as pd

# Load the dataset
def load_data():
    return pd.read_csv("European_Ski_Resorts.csv")

df = load_data()

# Streamlit App Title
st.title("European Ski Resort Finder")

# Basic exploration
if st.checkbox("Show Data Summary"):
    st.write(df.describe())

if st.checkbox("Show Raw Data"):
    st.write(df.head())

# Find the cheapest ski resort
st.subheader("Cheapest Ski Resort")
st.write(df.loc[df['DayPassPriceAdult'].idxmin(), ['Resort', 'Country', 'DayPassPriceAdult']])

# Find the highest ski resort
st.subheader("Highest Ski Resort")
st.write(df.loc[df['HighestPoint'].idxmax(), ['Resort', 'Country', 'HighestPoint']])

# Find the resort with the most slopes
st.subheader("Resort with Most Slopes")
st.write(df.loc[df['TotalSlope'].idxmax(), ['Resort', 'Country', 'TotalSlope']])

# Find the resort with the most lifts
st.subheader("Resort with Most Lifts")
st.write(df.loc[df['TotalLifts'].idxmax(), ['Resort', 'Country', 'TotalLifts']])

# Find the resort with the highest lift capacity
st.subheader("Resort with Highest Lift Capacity")
st.write(df.loc[df['LiftCapacity'].idxmax(), ['Resort', 'Country', 'LiftCapacity']])

# User input to filter resorts by skill level
level = st.selectbox("Choose your ski level", ["Beginner", "Intermediate", "Difficult"])

def resorts_by_level(level):
    if level.lower() == "beginner":
        return df[df['BeginnerSlope'] > df['IntermediateSlope'] + df['DifficultSlope']][['Resort', 'Country', 'BeginnerSlope']]
    elif level.lower() == "intermediate":
        return df[df['IntermediateSlope'] > df['BeginnerSlope'] + df['DifficultSlope']][['Resort', 'Country', 'IntermediateSlope']]
    elif level.lower() == "difficult":
        return df[df['DifficultSlope'] > df['BeginnerSlope'] + df['IntermediateSlope']][['Resort', 'Country', 'DifficultSlope']]
    else:
        return "Invalid level. Choose from Beginner, Intermediate, or Difficult."

st.subheader(f"Best Resorts for {level}")
st.write(resorts_by_level(level))
