import pandas as pd
import streamlit as st
from viz_utils import make_radar_plot
from viz_utils import make_bar_chart
from pred_utils import get_cluster_predictions

st.write(
    """
    # My Corporacion Favorita Store Type
    This web app is designed for you to know what store type your 
    store fits into. Using the information displayed in the charts, 
    you can also get yourself familiar with other store types and where
    your store fits, should you want to upgrade or downgrade your store. 
    """)

get_cluster_predictions()

##########################################################
## This section is to include radar plot on the web app ##
fig = make_radar_plot()
st.write(fig)
##########################################################


##########################################################
## This section is to give the option to see radar plot as 
## a bar chart
my_expander = st.expander(label='Average Distribution of Products Sold')
with my_expander:
    df = make_bar_chart()
    st.title('Average Sold')
    st.bar_chart(df)
##########################################################