FROM ubuntu:latest

# Update package lists and install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
