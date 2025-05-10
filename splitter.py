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
# - argparse: Parse command-line arguments
# - sys: System-specific parameters and functions
import pandas as pd
import os
import sys
import argparse
from datetime import datetime

def split_csv(input_file, output_dir, chunk_size):
    """
    Memory-efficient CSV file splitter.
    
    Args:
        input_file (str): Path to the input CSV file
        output_dir (str): Directory where output files will be saved
        chunk_size (int): Number of rows per output file
    
    Returns:
        int: Number of files created
    
    Raises:
        FileNotFoundError: If the input file does not exist
        PermissionError: If there are permission issues
        ValueError: If chunk_size is invalid
    """
    # Validate parameters
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer")
    
    # Create output directory if it doesn't exist
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except PermissionError:
        raise PermissionError(f"Permission denied when creating directory: {output_dir}")
    
    try:
        # Process in chunks to avoid loading entire file
        chunk_iterator = pd.read_csv(input_file, chunksize=chunk_size)
        file_count = 0
        
        for i, chunk in enumerate(chunk_iterator):
            timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            output_file = os.path.join(output_dir, f"{timestamp}--{i+1:02d}.csv")
            chunk.to_csv(output_file, index=False)
            file_count += 1
            
        return file_count
    
    except pd.errors.ParserError:
        raise ValueError("Error parsing CSV file. Please check if it's a valid CSV format.")
    except Exception as e:
        raise Exception(f"An error occurred while splitting the CSV file: {str(e)}")

def main():
    """Main function to handle command-line arguments and execute the CSV splitting process."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Split a large CSV file into smaller files with specified number of rows."
    )
    parser.add_argument(
        "-i", "--input", 
        default="pws.csv",
        help="Input CSV file path (default: pws.csv)"
    )
    parser.add_argument(
        "-o", "--output_dir", 
        default="data",
        help="Output directory for split files (default: data)"
    )
    parser.add_argument(
        "-s", "--size", 
        type=int, 
        default=100,
        help="Number of rows per output file (default: 100)"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute the split
    try:
        file_count = split_csv(args.input, args.output_dir, args.size)
        print(f"CSV split complete. Created {file_count} files in {os.path.abspath(args.output_dir)}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

# This block only executes when the script is run directly (not when imported)
if __name__ == "__main__":
    main()