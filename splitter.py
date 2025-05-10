# ===============================================================================
# CSV SPLITTER UTILITY
# ===============================================================================
# This script splits a large CSV file into multiple smaller CSV files based on a
# specified chunk size (number of rows per output file).
# ===============================================================================

# Import required libraries:
# - pandas: Powerful data manipulation library used to read, process and write CSV data
# - os: Provides functions for interacting with the operating system (file paths, directories)
# - datetime: Used to generate timestamps for unique file naming
import pandas as pd
import os
from datetime import datetime

def split_csv(input_file, output_dir, chunk_size):
    """
    Splits a CSV file into multiple smaller files with a specified number of rows.
    
    Args:
        input_file (str): Path to the input CSV file to be split
        output_dir (str): Directory where output files will be saved
        chunk_size (int): Number of rows per output file
    """
    # Create the output directory if it doesn't exist
    # This ensures we have somewhere to save our output files without error
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the entire CSV file into a pandas DataFrame
    # This loads all data into memory, so be cautious with very large files
    df = pd.read_csv(input_file)
    
    # Calculate the total number of rows in the input file
    total_rows = len(df)
    
    # Calculate how many chunks (output files) we need
    # The formula handles cases where the total rows isn't perfectly divisible by chunk_size
    # For example: if total_rows=250 and chunk_size=100, we need 3 chunks (2 full chunks + 1 partial)
    num_chunks = (total_rows // chunk_size) + (1 if total_rows % chunk_size > 0 else 0)

    # Process each chunk and create separate output files
    for i in range(num_chunks):
        # Calculate the starting and ending row indices for this chunk
        start_row = i * chunk_size
        end_row = start_row + chunk_size
        
        # Extract the current chunk from the DataFrame using iloc
        # iloc is a pandas indexer that selects data by integer position
        chunk = df.iloc[start_row:end_row]

        # Generate a unique timestamp for the filename to avoid overwriting files
        # Format: YYYY-MM-DD--HH-MM-SS (year, month, day, hour, minute, second)
        timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
        
        # Create the full output filename with path
        # The {i+1:02d} part adds a two-digit sequential number (01, 02, etc.)
        output_file = os.path.join(output_dir, f"{timestamp}--{i+1:02d}.csv")
        
        # Write the chunk to a new CSV file
        # index=False prevents writing the DataFrame's index as a column in the CSV
        chunk.to_csv(output_file, index=False)

# This block only executes when the script is run directly (not when imported)
if __name__ == "__main__":
    # Configuration parameters for the CSV splitting operation
    
    # The input CSV file to process (in the current working directory)
    input_csv = 'pws.csv'
    
    # Directory where output files will be saved
    output_directory = 'data'
    
    # Number of rows per output file
    # Adjust this value based on your needs and the size of your input file
    rows_per_file = 100
    
    # Call the split_csv function with the configured parameters
    split_csv(input_csv, output_directory, rows_per_file)