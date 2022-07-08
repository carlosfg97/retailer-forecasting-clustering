#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import numpy as np
import pandas as pd

df = pd.read_csv('/Users/hiradnourbakhsh/Desktop/Streamlit/clustering_df.csv')
df = df.drop(columns = ['Unnamed: 0', 'store_nbr'])

def main():
    st.title('Groceries Bar Chart')
    st.bar_chart(df)
if __name__ == 'main':
    main()


# In[ ]:




