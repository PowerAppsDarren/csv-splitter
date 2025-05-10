# ===============================================================================
# CSV SPLITTER UTILITY
# ===============================================================================
# Description:
#   This is a memory-efficient utility designed to split large CSV files into 
#   multiple smaller files without loading the entire dataset into memory.
#   It's particularly useful for processing CSV files that are too large to
#   open in standard spreadsheet applications or to process efficiently in memory.
#
# Design Philosophy:
#   - Memory Efficiency: Uses pandas chunk processing to handle files of any size
#   - User Friendly: Simple command-line interface with sensible defaults
#   - Robust: Comprehensive error handling for common issues
#   - Maintainable: Well-documented code with clear function responsibilities
# ===============================================================================

# Import required libraries:
# - pandas: Powerful data manipulation library used to read, process and write CSV data
#           Provides the critical 'chunksize' parameter for memory-efficient reading
# - os: Provides functions for interacting with the operating system (file paths, directories)
#       Used for path manipulation and directory creation
# - sys: System-specific parameters and functions, used for error handling and exit codes
# - argparse: Parse command-line arguments to allow customization of the script's behavior
# - datetime: Used to generate timestamps for unique file naming to prevent overwriting
import pandas as pd
import os
import sys
import argparse
from datetime import datetime

def split_csv(input_file, output_dir, chunk_size):
    """
    Memory-efficient CSV file splitter.
    
    This function reads a CSV file in chunks and writes each chunk to a separate
    output CSV file. This approach allows processing of very large files that
    would otherwise not fit into memory.
    
    Args:
        input_file (str): Path to the input CSV file to be split
        output_dir (str): Directory where output files will be saved (created if doesn't exist)
        chunk_size (int): Number of rows per output file (determines how many rows each file will contain)
    
    Returns:
        int: Number of files created during the splitting process
    
    Raises:
        FileNotFoundError: If the input file does not exist or is not accessible
        PermissionError: If there are issues with file system permissions
        ValueError: If chunk_size is invalid (must be positive) or CSV parsing fails
        Exception: For any other unexpected errors during processing
    """
    # Validate parameters to provide clear error messages before processing
    # Check if input file exists to prevent unnecessary processing attempts
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Ensure chunk size is positive to avoid infinite loops or empty files
    if chunk_size <= 0:
        raise ValueError("Chunk size must be a positive integer")
    
    # Create output directory if it doesn't exist
    # This ensures we have a place to write the output files before processing starts
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    except PermissionError:
        # Specific error for permission issues to help troubleshooting
        raise PermissionError(f"Permission denied when creating directory: {output_dir}")
    
    try:
        # Process input file in chunks to minimize memory usage
        # The chunksize parameter is crucial for memory efficiency - it determines
        # how many rows are loaded into memory at once
        chunk_iterator = pd.read_csv(input_file, chunksize=chunk_size)
        file_count = 0
        
        # Process each chunk and save to a separate file
        # The enumerate provides both the chunk and its index (used for filename numbering)
        for i, chunk in enumerate(chunk_iterator):
            # Generate a unique filename with timestamp and sequential number
            # Format: YYYY-MM-DD--HH-MM-SS--01.csv
            # This prevents overwriting existing files and provides chronological ordering
            timestamp = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            output_file = os.path.join(output_dir, f"{timestamp}--{i+1:02d}.csv")
            
            # Write the current chunk to a CSV file
            # index=False prevents adding an extra index column to the output
            chunk.to_csv(output_file, index=False)
            file_count += 1
            
        # Return the total number of files created for user feedback
        return file_count
    
    except pd.errors.ParserError:
        # Specific error for CSV parsing problems
        raise ValueError("Error parsing CSV file. Please check if it's a valid CSV format.")
    except Exception as e:
        # Catch-all for any other unexpected errors
        # This helps debugging by propagating the original error message
        raise Exception(f"An error occurred while splitting the CSV file: {str(e)}")

def main():
    """
    Main function to handle command-line arguments and execute the CSV splitting process.
    
    This function:
    1. Sets up the command-line argument parser
    2. Defines the available options and their defaults
    3. Parses user input arguments
    4. Calls the split_csv function with those arguments
    5. Provides user feedback or error messages
    
    The function is designed to be the entry point of the script when run directly.
    """
    # Set up argument parser with descriptive help text
    # This enables users to run the script with --help to see available options
    parser = argparse.ArgumentParser(
        description="Split a large CSV file into smaller files with specified number of rows."
    )
    
    # Define the input file parameter
    # Default is "pws.csv" to provide a sensible starting point
    parser.add_argument(
        "-i", "--input", 
        default="pws.csv",
        help="Input CSV file path (default: pws.csv)"
    )
    
    # Define the output directory parameter
    # Default is "data" to keep output files organized
    parser.add_argument(
        "-o", "--output_dir", 
        default="data",
        help="Output directory for split files (default: data)"
    )
    
    # Define the chunk size parameter
    # Default is 100 rows per file, which balances file size and number of files
    parser.add_argument(
        "-s", "--size", 
        type=int,  # Ensures the input is converted to integer
        default=100,
        help="Number of rows per output file (default: 100)"
    )
    
    # Parse command-line arguments into an object with attributes
    args = parser.parse_args()
    
    # Execute the CSV splitting operation
    try:
        # Call the split_csv function with the parsed arguments
        file_count = split_csv(args.input, args.output_dir, args.size)
        
        # Provide success feedback to the user, including absolute path for clarity
        print(f"CSV split complete. Created {file_count} files in {os.path.abspath(args.output_dir)}")
    except Exception as e:
        # Handle any exceptions by displaying an error message
        # Writing to stderr ensures proper error output handling
        print(f"Error: {str(e)}", file=sys.stderr)
        
        # Exit with non-zero status code to indicate failure to calling processes
        sys.exit(1)

# This conditional ensures the script only executes when run directly as a script
# When imported as a module, this block is not executed
# This allows the functions to be imported and used in other scripts without
# automatically running the main() function
if __name__ == "__main__":
    main()