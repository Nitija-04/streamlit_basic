import pandas as pd
import streamlit as st

st.title("CSV loader in streamlit")

uploaded_file=st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded file
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the data:")
    st.dataframe(df)

st.write("Let us insert dataframes:")

data = {
    "StudentID":["S101","S102","S103","S104","S105"],
    "Name":["Rahul","Sneha","Arjun","Priya","Kiran"],
    "Course":["Python Basics","Data science","Web development","AI & ML","Cyber security"],
    "Marks":[85,92,76,89,67],
    "Grade":["A","A+","B+","A","C"]
}

df= pd.DataFrame(data)

df.to_csv("data1.csv",index=False)
print("CSV file created: data1.csv")
print(df)