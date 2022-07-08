import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
#import streamlit as st


def make_radar_plot():
    cluster_centers = pd.read_csv("C:/Users/rhfny/OneDrive - McGill University/3. Winter22/INSY 695 - Enterprise Data Science/EDS-Group-Project/Clustering/cluster_centers.csv")

    # change total_sales to percentage
    cluster_centers['TOTAL SALES'] = cluster_centers['total_sales'] * 100

    # drop first column
    cluster_centers.drop(['Unnamed: 0','total_sales'], axis = 1, inplace=True)

    # normalize across rows
    #scaler = MinMaxScaler()
    #cluster_centers=pd.DataFrame(scaler.fit_transform(cluster_centers.T).T,columns=cluster_centers.columns)

    categories = list(cluster_centers.columns)

    # get row values as lists
    value_list = cluster_centers.values.tolist()

    # assign list to each cluster
    cluster0_val = value_list[0]
    cluster1_val = value_list[1]
    cluster2_val = value_list[2]
    cluster3_val = value_list[3]
        
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=cluster0_val,
        theta=categories,
        fill='toself',
        name='Hypermarket'
    ))
    fig.add_trace(go.Scatterpolar(
        r=cluster1_val,
        theta=categories,
        fill='toself',
        name='Convenience Store'
    ))
    fig.add_trace(go.Scatterpolar(
        r=cluster2_val,
        theta=categories,
        fill='toself',
        name='Grocery Store'
    ))
    fig.add_trace(go.Scatterpolar(
        r=cluster3_val,
        theta=categories,
        fill='toself',
        name='Supermarket'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        #range=[0, 50]
        )),
    showlegend=True
    )

    return fig

def make_bar_chart():
    stores = pd.read_csv('clustering_df.csv')
    stores = stores.drop(columns = ['Unnamed: 0', 'store_nbr'])
    my_dict = {}
    for i in stores.columns:
        my_dict[i] = stores[i].mean()
        
    df = pd.DataFrame(my_dict, index = [0])
    df = df.drop(columns = ['transactions', 'total_sales'])
    return df
    