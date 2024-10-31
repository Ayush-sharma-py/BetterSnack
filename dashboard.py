import streamlit as st
from rapidfuzz import fuzz
import typing
import numpy as np
import pandas as pd

# Deltas
brandThreshold = 75
productNameThreshold = 55


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
        df = df[df['brandScore'] > threshold].sort_values(by = ['brandScore', 'score'], ascending=False)
    
    return df

def lookupBestMatch(df):
    dfWithNova = df[df["nova_group"].notna()]
    if(len(dfWithNova) == 0):
        return df.iloc[0]
    else:
        return dfWithNova.iloc[0]

def printRow(df):
    backGroundColor = ["#4CAF50", "#A8D500", "#FFEB3B", "#FF9800", "#C62828"]
    foreGroundColor = ["#A8E6CF", "#D0E4A7", "#FFF9C4", "#FFCCBC", "#FFABAB"]
    novaGroup = df["nova_group"]
    
    if(df["brands"] != None):
        productName = str(df["brands"]).title() + " " + str(df["product_name"]).title()
    else:
        productName = str(df["product_name"]).title()
    try:
        novaGroup = int(novaGroup)

        st.html(f'''
            {productName}
        <div style="display: flex; justify-content: flex-end;">
            <div style="width: 100px; height: 100px; background-color: {backGroundColor[novaGroup - 1]}; 
                        color: white; display: flex; align-items: center; 
                        justify-content: center; border: 4px solid {foreGroundColor[novaGroup - 1]}; 
                        border-radius: 20px; /* Make the corners rounded */
                        margin: 20px;">
                {novaGroup}
            </div>
        </div>
        ''')

        tags = ["Python", "Streamlit", "Data Science", "Machine Learning"]

        # Display tags santize
        for tag in tags:
            st.markdown(f"<span style='color: #0072B8; background-color: #E6F7FF; border-radius: 3px; padding: 5px;'>{tag}</span>", unsafe_allow_html=True)
    except:
        st.html(f'''
            {productName}
        <div style="display: flex; justify-content: flex-end;">
            <div style="width: 100px; height: 100px; background-color: #808080; 
                        color: white; display: flex; align-items: center; 
                        justify-content: center; border: 4px solid #5A5A5A; 
                        border-radius: 20px; /* Make the corners rounded */
                        margin: 20px;">
                - - -
            </div>
        </div>
        ''')
    return None



# Loading the cache
df = load_data()

st.write("# " + "Better Snack")


productName = st.text_input("Enter Product Name", value="", max_chars=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="Enter Product Name", disabled=False, label_visibility="visible")
brandName = st.text_input("Enter Brand Name", value="", max_chars=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="Optional", disabled=False, label_visibility="visible")

if(len(productName) > 0):
    outputRow = lookupProductName(df, productName.lower(), productNameThreshold)
    if(len(brandName) > 0):
        outputRow = filterBrand(outputRow, brandName.lower(), brandThreshold)

    bestRow = lookupBestMatch(outputRow)
    if(len(bestRow) != 0):
        printRow(bestRow)
        st.dataframe(bestRow)
    else:
        st.write("Product not found!")


st.caption(":blue[Nova Group] refers to how processed it is")