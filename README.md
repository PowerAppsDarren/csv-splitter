# CSV Splitter

A memory-efficient utility for splitting large CSV files into smaller chunks.

## Overview

This utility helps you split a large CSV file into smaller CSV files, each containing a specified number of rows. It processes data in chunks to minimize memory usage, making it suitable for very large files.

## Features

- Split CSV files by number of rows
- Memory-efficient processing using pandas chunks
- Command-line interface for easy customization
- Timestamped output files for easy tracking
- Docker support for containerized execution
- Error handling for common issues (file not found, permissions, etc.)

## Installation

### Standard Installation

1. Clone the repository:

```sh
git clone https://github.com/your-username/csv-splitter.git
cd csv-splitter
```

2. Install dependencies:

```sh
pip install -r requirements.txt
```

### Docker Installation

Build the Docker image:

```sh
docker build -t csv-splitter .
```

## Usage

### Command Line Options

```sh
python splitter.py [-h] [-i INPUT] [-o OUTPUT_DIR] [-s SIZE]
```

Options:
- `-i, --input`: Input CSV file path (default: `pws.csv`)
- `-o, --output_dir`: Output directory for split files (default: `data`)
- `-s, --size`: Number of rows per output file (default: 100)

### Examples

Split a file with default settings:
```sh
python splitter.py
```

Customize input file, output directory, and chunk size:
```sh
python splitter.py --input large_file.csv --output_dir output_chunks --size 500
```

### Docker Usage

Run with default settings:
```sh
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output csv-splitter
```

Customize parameters:
```sh
docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output csv-splitter --input /app/input/large_file.csv --output_dir /app/output --size 500
```

## Project Structure

```
csv-splitter/
├── splitter.py        # Main script for splitting CSV files
├── requirements.txt   # Python dependencies
├── dockerfile         # Docker configuration
├── README.md          # Project documentation
├── LICENSE            # MIT license
└── .gitignore         # Git ignore rules
```

## Output File Format

Split files are saved with the naming pattern: `yyyy-mm-dd--hh-mm-ss--##.csv`, where:
- `yyyy-mm-dd--hh-mm-ss` is the timestamp
- `##` is a sequential number (starting at 01)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.