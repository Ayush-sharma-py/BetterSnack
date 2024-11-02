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
        df = pd.read_csv("Files//filtered.csv")
        
        df = df[df["product_name"].notna()]

        df['product_name'] = df['product_name'].str.lower()
        df['brands'] = df['brands'].str.lower()

    return df[["product_name", "nova_group", "brands", 
            "quantity", "categories", "nutriscore_score", "nutriscore_grade",
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
    if(len(dfWithNova) != 0):
        return dfWithNova.iloc[0]
    elif(len(df) != 0):
        return df.iloc[0]
    else:
        # Sends back empty df to compare
        return df


def printRow(df):
    backGroundColor = ["#4CAF50", "#A8D500", "#FFEB3B", "#FF9820", "#696969"]
    foreGroundColor = ["#A8E6CF", "#D0E4A7", "#FFF9C4", "#FFCCBC", "#D3D3D3"]
    novaGroup = df["nova_group"]
    nutriScore = df["nutriscore_score"]
    nutriGrade = df["nutriscore_grade"]

    
    if(not pd.isna(df["brands"])):
        productName = str(df["product_name"]).title()
        brandName = str(df["brands"]).title()
        st.html(f'''
                <div style='display: flex; justify-content: center;'>
                    <h1 style="color: #0072B8; margin-right: 10px"> {brandName} </h1>
                    <h1> {productName} </h1>
                </div>    
                ''')
    else:
        productName = str(df["product_name"]).title()
        st.html(f'''<center> <h1 style="color: #00000;"> {productName} </h1> </center>''')

    if(not pd.isna(novaGroup)):
        novaGroup = int(novaGroup)
        novaTag = str(novaGroup)
    else:
        novaGroup = 0
        novaTag = '- - -'

    if(not pd.isna(nutriScore)):  
        nutriScoreTag = str(int(nutriScore)) + " / 100"
        nutriScore = int((100 - nutriScore) / 20)
    else:
        nutriScore = 0
        nutriScoreTag = '- - -'
    
    # WHO PUTS UNKNOWN IN A DATASET JUST BE NORMAL AND PUT None or Null
    if(not (pd.isna(nutriGrade) or nutriGrade == "unknown")):
        nutriGradeTag = str(nutriGrade).upper()
        print(nutriGrade)
        nutriGrade = (ord(nutriGrade) - 96) % len(backGroundColor)
    else:
        nutriGrade = 0
        nutriGradeTag = '- - -'

    st.html(f'''
    <div style="display: flex; justify-content: center;">
        <div style="width: 100px; height: 100px; background-color: {backGroundColor[novaGroup - 1]}; 
                    color: white; display: flex; align-items: center; 
                    justify-content: center; border: 4px solid {foreGroundColor[novaGroup - 1]}; 
                    border-radius: 20px; margin: 20px;">
            {novaTag}
        </div>
        <div style="width: 100px; height: 100px; background-color: {backGroundColor[nutriScore - 1]}; 
                    color: white; display: flex; align-items: center; 
                    justify-content: center; border: 4px solid {foreGroundColor[nutriScore - 1]}; 
                    border-radius: 20px; margin: 20px;">
            {nutriScoreTag}
        </div>
        <div style="width: 100px; height: 100px; background-color: {backGroundColor[nutriGrade - 1]}; 
                    color: white; display: flex; align-items: center; 
                    justify-content: center; border: 4px solid {foreGroundColor[nutriGrade - 1]}; 
                    border-radius: 20px; margin: 20px;">
            {nutriGradeTag}
        </div>
    </div>
    ''')

    tags = df['categories']
    #print(tags)

    # Sanitation when tags is nan
    if(not pd.isna(tags)):
        tags = tags.split(',')

        # Display tags santize
        colors = ['#7cb37e', '#B3FFB3', '#B3D1FF', '#FFE1B3', '#d85831']  # Example colors for each tag

        tag_html = "<div style='display: flex; flex-wrap: wrap; gap: 5px;'>"
        for i in range(len(tags)):
            color = colors[i % len(colors)]  # Cycle through colors
            tag_html += f'''<span style='color: #0072B8; background-color: {color}; border-radius: 10px;
            padding: 5px; display: inline-block; margin-right: 0px;'>{tags[i]}</span>'''

        # Render the tags side by side
        st.html(tag_html)



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