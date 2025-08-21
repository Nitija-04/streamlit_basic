import streamlit as st

def details(name, cat, amt, date, op):
    st.write(f"**Name:** {name}")
    st.write(f"**Category:** {cat}")
    st.write(f"**Amount:** Rs.{amt}")
    st.write(f"**Date:** {date}")
    st.write(f"**Additional notes:** {op}")

st.title("Streamlit example")
st.write("This is a simple Streamlit app")
name = st.text_input("Enter your name:")
cat = st.selectbox("Select the expense categories",("Food","transportation","Entertainment"))
amt = st.number_input("Enter the amount:", min_value=0, max_value=16000,step=1)
date = st.date_input("Enter date:")
op = st.text_area("Additional notes:")
but = st.button("Submit", on_click=details(name,cat,amt,date,op))

