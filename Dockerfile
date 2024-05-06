# Use a slim Python 3.9 base image for efficiency
FROM python:3.9-slim

# Set a working directory for clarity and organization
WORKDIR /app

# Clone the GitHub repository
RUN apt-get update && \
    apt-get install -y git && \
    git clone -b client_side_app https://pavanyendluri588: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@github.com/pavanyendluri588//style_transfer_project/ .


# Install dependencies from requirements.txt
#COPY requirements.txt /app
RUN pip install -r requirements.txt

# Expose port 8000 for access to the Uvicorn application
EXPOSE 8000:8000

# Run Streamlit as the main command
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8000", "server.serverAddress=0.0.0.0"]