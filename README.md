# CSV Splitter

A memory-efficient utility for splitting large CSV files into smaller chunks.

This project provides a utility to split a large CSV file (`pws.csv`) into smaller CSV files. Each smaller file is saved in the `data` directory and is named using the format `yyyy-mm-dd--hh-mm-ss--##`, where `##` is a sequential number.

## Features

- Split CSV files by number of rows
- Memory-efficient processing using chunks
- Command-line interface for easy usage
- Timestamped output files
- Docker support for containerized execution
- 
## Project Structure

```
csv-splitter
├── src
│   └── splitter.py      # Main logic for splitting the CSV file
├── data/
│   └── .gitkeep         # Keeps the data directory tracked by Git
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Installation

### Standard Installation

1. Clone the repository:

## Runing

To build the docker image: 

```sh
docker build -t csv-splitter .
```

Then to run it, execute this

```sh
cd src
docker run -it -v ${PWD}:/app csv-splitter
```