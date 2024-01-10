#!/usr/bin/env python

import pandas as pd
import os
import argparse


# Function to process individual files
def process_file(file):
    # Read the CSV file into a DataFrame, skipping rows with # as it contains metadata
    df = pd.read_csv(file, skiprows=lambda x: x < 5, comment='#')
    
    # Remove the file extension from the filename
    filename = os.path.splitext(os.path.basename(file))[0]
    
    # Create a DataFrame from the second column as headers and set values to 'yes'
    headers = df.pivot(index = "mge_no", columns = "name", values = "prediction").columns.values.tolist()
    headers = [str(header) for header in headers]
    #headers = [header for header in headers if str(header) != 'nan']
    
    new_columns = {col: 'yes' for col in headers}
    new_columns['filename'] = filename
    
    df_temp = pd.DataFrame(new_columns, index=[0])
    # move last column (that is, filename) to the first column
    df_temp = df_temp[df_temp.columns[::-1]]
    
    return df_temp

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Process CSV files and create a summary file.')
parser.add_argument('--directory', help='Directory containing CSV files')
parser.add_argument('--output_file', help='Output file name')
args = parser.parse_args()

if args.directory and args.output_file:
    directory = args.directory
    output_file = args.output_file

    # Process each file in the directory and concatenate the results into a summary DataFrame
    summary_df = pd.DataFrame()

    file_list = [f for f in os.listdir(directory) if f.endswith('.csv')]

    for file in file_list:
        file_path = os.path.join(directory, file)
        df_temp = process_file(file_path)
        summary_df = pd.concat([summary_df, df_temp], ignore_index=True)

    # Fill NaN values with 'no' in the summary DataFrame
    summary_df.fillna('no', inplace=True)

    # Create a summary tab-separated file
    summary_df.to_csv(output_file, sep='\t', index=False)
    print(f"Summary file created: {output_file}")
else:
    print("Please provide both --directory and --output_file arguments.")