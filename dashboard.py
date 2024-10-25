import streamlit as st
import numpy as np
import pandas as pd

 
def lookupProductName(df, productName):
    outputDataFrame = df[df['product_name'].str.contains(productName, case=False, na=False)]
    return outputDataFrame

st.write("# " + "Better Snack")
df = pd.read_csv("filtered.csv")

productName = st.text_input("Enter Product Name", value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="visible")
outputRow = lookupProductName(df[["product_name", "nova_group", "brands", 
                                  "quantity", "categories", "nutriscore_score", 
                                  "energy_100g"]], productName)

st.write(outputRow.iloc[0:100])