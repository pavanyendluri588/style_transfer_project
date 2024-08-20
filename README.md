# Style Transfer Project

This project demonstrates a simple web application that performs neural style transfer using Streamlit. The application allows users to upload a content image and a style image, then applies the style of one image to the content of another. Users can adjust the strength of the style transfer via a slider.

## Features

* **Upload Images**: Upload a content image and a style image in JPG, PNG, or JPEG format.
* **Style Strength Adjustment**: Adjust the strength of the style transfer effect using a slider.
* **Real-time Image Display**: View the content image, style image, and the resulting styled image side by side.

## Getting Started

### Prerequisites

* Docker
* Git

### Installation

1. **Clone the Repository**

   Clone the repository from GitHub using the following command:

   ```bash
   git clone [https://github.com/pavanyendluri588/style_transfer_project.git](https://github.com/pavanyendluri588/style_transfer_project.git)
   cd style_transfer_project

2. **Build and Run the Docker Container**

   Build the Docker container using the provided Dockerfile:
   ```bash
   docker build -t style-transfer-app .

3. **Run the Docker container:**

   ```bash
   docker run -p 8000:8000 style-transfer-app

4. **Access the Application**

   Open your web browser and navigate to:

   http://localhost:8000

   You should see the Streamlit application running, ready for you to upload images and perform style transfer.

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



### Contributing
   
   If you would like to contribute to this project, please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.   

### License

   This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments

   Special thanks to the open-source community and the developers behind the libraries used in this project. 
