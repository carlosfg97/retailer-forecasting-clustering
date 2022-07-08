import pandas as pd
import streamlit as st
from viz_utils import make_radar_plot


df = pd.read_csv('docker_data/outputs/cluster_summary.csv')


input_list = ['BABY CARE', 'BEVERAGES', 'BOOKS', 'BREAD/BAKERY',
       'CLEANING', 'DAIRY', 'DELI', 'FROZEN FOODS', 'GROCERIES', 'HOME CARE',
       'LADIESWEAR', 'LAWN AND GARDEN', 'LIQUOR,WINE,BEER', 'MEATS', 'OTHER',
       'PERSONAL CARE', 'POULTRY', 'PRODUCE', 'TRANSACTIONS', 'TOTAL SALES']

st.image("logo-cf-footer.png")

for i in input_list:
    i = st.sidebar.number_input(
    label=i, min_value=0.00, max_value=100.00, value=5.00, step = 0.01, format="%f")

submit = st.sidebar.button(
    label="Classify my store"
)

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

##########################################################
## This section is to include radar plot on the web app ##
fig = make_radar_plot()
st.write(fig)
##########################################################

