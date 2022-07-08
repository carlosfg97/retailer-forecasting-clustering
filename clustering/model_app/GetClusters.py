import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.stats import f
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import silhouette_samples
from sklearn.metrics import silhouette_score
import statistics
from sklearn.preprocessing import MinMaxScaler

import joblib

def get_clusters():

    print('Starting clustering')
    # Importing the clustering dataset
    df = pd.read_csv('docker_data/data/clustering_df.csv')

    # Dropping store_nbr
    clustering_df = df.drop(columns= 'store_nbr')

    # Standardizing the transactions and total_sales columns
    scaler = MinMaxScaler()
    scaler.fit(clustering_df[['total_sales']])
    clustering_df['total_sales'] = scaler.transform(clustering_df[['total_sales']])


    # Choosing the variables
    X = clustering_df[['CLEANING', 'DAIRY', 'GROCERIES', 'PRODUCE', 'POULTRY',
    'FROZEN FOODS','DELI','BREAD/BAKERY','OTHER', 'total_sales']]

    X_cols = list(X.columns)

    # Creating a loop to vary 'k' in order to plot the elbow and silhouette plot and select the optimal no. of clusters
    list_base_model = []
    withinss=[]
    for i in range(2,20):
        kmeans = KMeans(n_clusters=i, random_state=0)
        model = kmeans.fit(X)
        labels = model.labels_
        withinss.append(model.inertia_)
        silhouette = silhouette_score(X, labels)
        list_base_model.append(silhouette)

    #pyplot.plot(list(range(2,20)), withinss, marker= 'o')

    #pyplot.plot(list(range(2,20)), list_base_model, marker= 'o')


    # Running the final K means model with k=4
    kmeans = KMeans(n_clusters=4, random_state=0)
    model = kmeans.fit(X)
    labels = model.labels_


    silhouette_sam = silhouette_samples(X, labels)

    df_100 = pd.DataFrame({'label':labels,'silhouette':silhouette_sam}) # save silhouette score
    print('Average Silhouette Score for Cluster 0: ',np.average(df_100[df_100['label'] == 0].silhouette))
    print('Average Silhouette Score for Cluster 1: ',np.average(df_100[df_100['label'] == 1].silhouette))
    print('Average Silhouette Score for Cluster 2: ',np.average(df_100[df_100['label'] == 2].silhouette))
    print('Average Silhouette Score for Cluster 3: ',np.average(df_100[df_100['label'] == 3].silhouette))


    # Creating a dataframe to store the cluster centers
    cluster_centers_df = pd.DataFrame(model.cluster_centers_)

    cluster_centers_df.columns = X_cols

    # Adding the clusters column to our original dataframe
    df['assigned_cluster'] = labels

    df.to_csv('docker_data/outputs/store_labels.csv', index=None)
    cluster_centers_df.to_csv('docker_data/outputs/cluster_summary.csv', index=None)
    df_100.to_csv('docker_data/outputs/cluster_sil_scores.csv', index = None)


    joblib.dump(kmeans, 'docker_data/outputs/kmeans.pkl')
    joblib.dump(scaler, 'docker_data/outputs/scaler.pkl')

    return None


if __name__ == '__main__':
    get_clusters()

