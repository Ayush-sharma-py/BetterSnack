import streamlit as st
from rapidfuzz import fuzz
import typing
import numpy as np
import pandas as pd

# Deltas
brandThreshold = 75
productNameThreshold = 85


# This function is used to load data and cache it
@st.cache_resource
def load_data():
    # Load and process data here
    with st.spinner():
        df = pd.read_csv("filtered.csv")
        
        df = df[df["product_name"].notna()]

        df['product_name'] = df['product_name'].str.lower()
        df['brands'] = df['brands'].str.lower()

    return df[["product_name", "nova_group", "brands", 
            "quantity", "categories", "nutriscore_score", 
            "energy_100g"]]

# Testing better algorithms to match names
def lookupProductName(df, productName: str, threshold: int):
    # Fill NaN values with empty strings
    product_names = df["product_name"]
    
    # Calculate scores using a vectorized approach
    scores = np.vectorize(lambda e: fuzz.ratio(productName, e))(product_names)
    
    # Assign the scores back to the DataFrame
    df['score'] = scores
    return df[df['score'] > threshold].sort_values(by = ['score'], ascending=False)

def filterBrand(df, brandName: str, threshold):
    if(len(brandName) > 0):
        brand_names = df["brands"]
    
        # Calculate scores using a vectorized approach
        brandScores = np.vectorize(lambda e: fuzz.ratio(brandName, e))(brand_names)
        df['brandScore'] = brandScores
        df = df[df['brandScore'] > threshold].sort_values(by = ['brandScore'], ascending=False)
    
    return df

    
    
        
    


# Loading the cache
df = load_data()

st.write("# " + "Better Snack")


productName = st.text_input("Enter Product Name", value="", max_chars=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="Enter Product Name", disabled=False, label_visibility="visible")
brandName = st.text_input("Enter Brand Name", value="", max_chars=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="Optional", disabled=False, label_visibility="visible")

if(len(productName) > 0):
    outputRow = lookupProductName(df, productName.lower(), productNameThreshold)
    if(len(brandName) > 0):
        outputRow = filterBrand(outputRow, brandName.lower(), brandThreshold)

    st.dataframe(outputRow)


st.caption(":blue[Nova Group] refers to how processed it is")