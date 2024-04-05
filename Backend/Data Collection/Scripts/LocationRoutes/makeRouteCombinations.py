import csv
import os
from itertools import combinations

def createCombinations(places):
    combinations_list = []
    for combo in combinations(places, 2):
        cluster_start = int(combo[0]['Cluster'])
        cluster_stop = int(combo[1]['Cluster'])
        urlName1 = combo[0]['urlName']
        urlName2 = combo[1]['urlName']
        link = f"https://www.rome2rio.com/map/{urlName1}/{urlName2}"
        combinations_list.append((cluster_start, cluster_stop, link))
        
    return combinations_list

def main():
    csv_input_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'allData', 'all_clusters_centroids_with_urls.csv')
    csv_output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'allData', 'all_combinations_with_links.csv')
    with open(csv_input_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        places = list(reader)
    
    combinations_list = createCombinations(places)

    with open(csv_output_file, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['Cluster_Start', 'Cluster_Stop', 'Link']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for combination in combinations_list:
            writer.writerow({'Cluster_Start': combination[0], 'Cluster_Stop': combination[1], 'Link': combination[2]})
    
    print("\033[92mCombinations with links have been created successfully.\033[0m")

if __name__ == "__main__":
    main()