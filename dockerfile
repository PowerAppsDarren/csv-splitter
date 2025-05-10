FROM python:3.9-slim

# Set metadata
LABEL maintainer="Darren Neese <darren@superpowerlabs.co>"
LABEL version="1.0"
LABEL description="CSV Splitter Utility"

# Set working directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create volume mount points for input and output data
VOLUME ["/app/input", "/app/output"]

# Set entrypoint to run the script
ENTRYPOINT ["python", "splitter.py"]
# Default arguments
CMD ["--input", "/app/input/data.csv", "--output_dir", "/app/output", "--size", "100"]
