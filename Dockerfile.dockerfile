# Use a Python base image
FROM python:3.10.12

# Set the working directory
WORKDIR /mnt/c/Users/LENOVO/spot2

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code
COPY dashboard_spot.py .

# Expose the Streamlit port
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "dashboard_spot.py"]