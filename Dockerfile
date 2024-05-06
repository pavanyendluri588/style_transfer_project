# Use a slim Python 3.11 base image for efficiency
FROM python:3.9

# Set a working directory for clarity and organization
WORKDIR /app

# Clone the GitHub repository
RUN apt-get update && \
    apt-get install -y git && \
    git clone -b server_side_app https://pavanyendluri588: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@github.com/pavanyendluri588//style_transfer_project/ .


# Install dependencies from requirements.txt
#COPY . /app
RUN  pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN python install_vgg19.py

# Expose port 8000 for access to the Uvicorn application
EXPOSE 8000:8000

# Run Uvicorn as the main command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]