# Use Python 3.10+ (instead of 3.9)
FROM python:3.12.1

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Start the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
