import os
import pandas as pd
import numpy as np
import math
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import random

random_numbers = random.sample(range(100000, 1000000), 899998)

def getLocationFiles():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    location_dir = os.path.join(parent_dir, 'allData')
    location_files = []
    for file in os.listdir(location_dir):
        if file.endswith('_locations.csv'):
            location_files.append(file)
    return location_files

def generateClusters(file):
    global random_numbers

    df = pd.read_csv('../allData/' + file)
    X = df[['Longitude', 'Latitude']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    num_locations = len(X_scaled)
    optimal_clusters = math.ceil(num_locations / 10)
    kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(X_scaled)
    df['Cluster'] = kmeans.labels_

    unique_clusters = np.unique(df['Cluster'])
    cluster_mapping = dict(zip(unique_clusters, [str(num) for num in random_numbers]))
    df['Cluster'] = df['Cluster'].replace(cluster_mapping)

    return df

def generateClustersCentroids(all_data, all_locations_df):
    all_data['Cluster'] = all_data['Cluster'].astype(int)
    grouped = all_data.groupby('Cluster')
    result_df = pd.DataFrame(columns=['Name', 'geonameId', 'Latitude', 'Longitude', 'First Order', 'Second Order', 'Third Order', 'Cluster'])
    
    for cluster, group in grouped:
        centroid_longitude = group['Longitude'].mean()
        centroid_latitude = group['Latitude'].mean()
        closest_coordinate_idx = ((group['Longitude'] - centroid_longitude)**2 + (group['Latitude'] - centroid_latitude)**2).idxmin()
        closest_coordinate = group.loc[closest_coordinate_idx]

        info_row = all_locations_df[(all_locations_df['Latitude'].eq(closest_coordinate['Latitude'])) & (all_locations_df['Longitude'].eq(closest_coordinate['Longitude']))]
        
        result_df = result_df._append({'Name': info_row['Name'].values[0],
                                    'geonameId': info_row['geonameId'].values[0],
                                    'Latitude': info_row['Latitude'].values[0],
                                    'Longitude': info_row['Longitude'].values[0],
                                    'First Order': info_row['First Order'].values[0],
                                    'Second Order': info_row['Second Order'].values[0],
                                    'Third Order': info_row['Third Order'].values[0],
                                    'Cluster': cluster},
                                    ignore_index=True)
    
    result_df.to_csv('../allData/all_clusters_centroids.csv', index=False)
    print("\033[92mClusters and centroids generated successfully.\033[0m")

def main():
    location_files = getLocationFiles()
    all_data = pd.DataFrame()
    all_locations_df = pd.DataFrame()
    
    for file in location_files:
        location_df = pd.read_csv('../allData/' + file)
        all_locations_df = all_locations_df._append(location_df)
        cluster_df = generateClusters(file)
        all_data = all_data._append(cluster_df)
    
    all_locations_df.to_csv('../allData/all_locations.csv', index=False)
    all_data.to_csv('../allData/all_clusters.csv', index=False)

    generateClustersCentroids(all_data, all_locations_df)

if __name__ == "__main__":
    main()