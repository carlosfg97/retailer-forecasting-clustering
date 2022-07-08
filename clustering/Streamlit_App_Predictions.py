#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st


# In[3]:


import pandas as pd
import numpy as np


# In[4]:


import joblib as jb


# In[5]:


# Loading kmeans.pkl
kmeans = jb.load(r"C:\Users\adity\Documents\Winter Semester'22 Courses MMA McGill\Enterprise Data Science 2\Group Project\kmeans.pkl")


# In[6]:


# Loading scaler.pkl
scaler = jb.load(r"C:\Users\adity\Documents\Winter Semester'22 Courses MMA McGill\Enterprise Data Science 2\Group Project\scaler.pkl")


# In[7]:


def get_cluster_predictions():
    
    # Specifying the title of the web app
    st.title('Know Your Store Type')
    
    # Creating a sidebar where all the inputs will be taken from the user
    logo = st.sidebar.image(r"C:\Users\adity\Documents\Winter Semester'22 Courses MMA McGill\Enterprise Data Science 2\Group Project\logo-cf-footer.png")

    categories = ['CLEANING', 
                  'DAIRY', 
                  'GROCERIES', 
                  'PRODUCE', 
                  'POULTRY', 
                  'FROZEN FOODS', 
                  'DELI', 
                  'BREAD/BAKERY',
                 'OTHER']
    
    input_values = []
    
    # Taking inputs from the user
    Cleaning = st.sidebar.number_input(label='Cleaning', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Cleaning)
    Dairy = st.sidebar.number_input(label='Dairy', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Dairy)
    Groceries = st.sidebar.number_input(label='Groceries', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Groceries)
    Produce = st.sidebar.number_input(label='Produce', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Produce)
    Poultry = st.sidebar.number_input(label='Poultry', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Poultry)
    Frozen_Foods = st.sidebar.number_input(label='Frozen_Foods', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Frozen_Foods)
    Deli = st.sidebar.number_input(label='Deli', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Deli)
    Bread_Bakery = st.sidebar.number_input(label='Bread/Bakery', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Bread_Bakery)
    Other = st.sidebar.number_input(label='Other', min_value=0.00, max_value=100.00, format="%f")
    input_values.append(Other)
    
    ts = st.sidebar.number_input(label = 'Total_Sales')
    total_sales = ts
    # Standardizing total sales
    total_sales = scaler.transform([[total_sales]])
    total_sales = total_sales[0][0]
    
    # Appending total_sales to the input_values list
    input_values.append(total_sales)
    
    input_values_array = np.array([input_values])
    
    predict = st.sidebar.button(label="Classify my store")
    
    if predict:
        prediction = kmeans.predict(input_values_array)
        prediction_1 = list(prediction)
        prediction_2 = prediction_1[0]
        
        if prediction_2 == 0:
            st.success('Your store type: Hypermarket')
        elif prediction_2 == 1:
            st.success('Your store type: Convenience')
        elif prediction_2 == 2:
            st.success('Your store type: Grocery')
        elif prediction_3 == 3:
            st.success('Your store type: Supermarket')

    st.write(
    """
    # Corporacion Recommendation for Store X
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut 
    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in 
    voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    """
    )

if __name__ == '__main__':
     get_cluster_predictions()


# In[ ]:




