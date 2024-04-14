import os
import pandas as pd
import json

def read_csv_files(directory):
    columns = ['link', 'title', 'category', 'address', 'website', 'phone', 'plus_code', 'review_count', 'review_rating', 'latitude', 'longitude', 'cid', 'descriptions', 'images']
    combined_df = pd.DataFrame(columns=columns)
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join(directory, filename))
                for column in columns:
                    if column not in df.columns:
                        df[column] = ''
                # Check if 'link' column is not empty
                df = df[df['link'].notna() & (df['link'] != '')]
                
                # Extract image links, excluding those with "streetviewpixels"
                df['images'] = df['images'].apply(lambda x: json.loads(x))
                df['images'] = df['images'].apply(lambda x: [img['image'] for img in x if 'streetviewpixels' not in img['image']])
                
                combined_df = pd.concat([combined_df, df[columns]], ignore_index=True)
            except ValueError:
                print(f"Skipping file {filename} due to a value error.")
    return combined_df

def save_combined_df(combined_df, output_file):
    combined_df.to_csv(output_file, index=False)
    print('\033[92mCombined Attraction Results\033[0m')

def main():
    directory = 'Results'
    output_file = '../allData/all_attractions.csv'
    combined_df = read_csv_files(directory)
    save_combined_df(combined_df, output_file)

if __name__ == '__main__':
    main()