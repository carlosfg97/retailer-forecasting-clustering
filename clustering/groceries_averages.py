#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import numpy as np
import pandas as pd

stores = pd.read_csv('/Users/hiradnourbakhsh/Desktop/Streamlit/clustering_df.csv')
stores = stores.drop(columns = ['Unnamed: 0', 'store_nbr'])
my_dict = {}
for i in stores.columns:
    my_dict[i] = stores[i].mean()
    
df = pd.DataFrame(my_dict, index = [0])
df = df.drop(columns = ['transactions', 'total_sales'])

def main():
    st.title('Average Sold')
    st.bar_chart(df)
if __name__ == 'main':
    main()


# In[ ]:




