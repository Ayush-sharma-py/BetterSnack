# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid prompts during package installations
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Pandas and NumPy using pip
RUN pip3 install pandas numpy

# Set the default command to run Python
CMD ["bash"]
