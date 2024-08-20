# Style Transfer Project

This project implements a style transfer algorithm using FastAPI and PyTorch. The server-side application allows users to apply a style transfer effect to images through a RESTful API. The project utilizes a pre-trained VGG19 model to perform neural style transfer, combining content and style images into a new image with the style of the reference image and the content of the target image.

## Features

* **Dockerized Environment**: The server is containerized using Docker for easy deployment and scalability.
* **FastAPI**: Provides a lightweight and high-performance web framework for building APIs.
* **PyTorch**: Utilizes a pre-trained VGG19 model for neural style transfer.
* **Image Processing**: Handles image transformations and style transfer using the PyTorch library.
* **Dynamic Configuration**: Allows setting style strength and other parameters through the API.

## Getting Started

### Prerequisites

* Docker
* Docker Compose (optional)

### Setup and Installation

1. **Clone the Repository**

   Clone the repository from GitHub using the following command:

   ```bash
   git clone https://github.com/pavanyendluri588/style_transfer_project.git
   cd style_transfer_project

2. **Build the Docker Image**

   Build the Docker container using the provided Dockerfile:
   ```bash
   docker build -t style-transfer-server .


3. **Run the Docker container:**

   ```bash
   docker run -p 8000:8000 style-transfer-server
   ```

   This command will start the FastAPI server and expose it on port 8000.


### Setup and Installation
### Project Structure
   * **Dockerfile**: Contains the instructions to build the Docker image.
   * **streamlit_app.py**: The main Streamlit application file that handles image upload, style transfer requests, and image display.
   * **requirements.txt**: Lists the Python dependencies needed to run the application.

### Dependencies
   * **numpy: 1.26.4**
   * **pandas: 2.2.2**
   * **pillow: 10.3.0**
   * **requests: 2.31.0**
   * **streamlit: 1.34.0**

### Usage
### Usage

   1.Send a POST request to /style_transfer with the required images and parameters.
   2.Receive the processed image in response.
   * **Example Request**:
    ```bash
    curl -X POST "http://localhost:8000/style_transfer" -H "Content-Type: application/json" -d '{
    "content_image": [/* Array of pixel values */],
    "style_image": [/* Array of pixel values */],
    "style_strength": 1e6
    }'
    ```


### Contributing
   
   If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.   

### License

   This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
  * **PyTorch** : For providing the deep learning framework.
  * **FastAPI** : For the high-performance web framework.
  * **VGG19** : For the pre-trained model used in style transfer.

