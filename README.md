# CSV Splitter

A memory-efficient utility for splitting large CSV files into smaller chunks.

## Features

- Split CSV files by number of rows
- Memory-efficient processing using chunks
- Command-line interface for easy usage
- Timestamped output files

## Installation

1. Clone the repository:
2. Install required dependencies:

## Usage

### Command Line Interface

Arguments:
- `-i`, `--input`: Input CSV file path (default: pws.csv)
- `-o`, `--output_dir`: Output directory for split files (default: data)
- `-s`, `--size`: Number of rows per output file (default: 100)

### Example

Split a large CSV file into chunks of 500 rows each:

### As a Module

You can also use the splitter in your own Python scripts:

```python
from splitter import split_csv

# Split a CSV file into chunks of 1000 rows
split_csv("input.csv", "output_directory", 1000)
