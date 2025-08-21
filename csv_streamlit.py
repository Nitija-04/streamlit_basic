import streamlit as st
import requests

url = "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"

response = requests.get(url)
open("data.csv","wb").write(response.content)
print("CSV file downloaded as data.csv")