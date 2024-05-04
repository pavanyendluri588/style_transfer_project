import streamlit as st
from PIL import Image
import requests
import numpy as np
import traceback

st.set_page_config(layout="wide")
def process_image(streamlit_image):
    img = Image.open(streamlit_image)
    img_array = np.array(img)
    return img_array
def display_images(content_image, style_image):
    """Displays the uploaded content, processed, and final images."""
    col1, col2,col3  = st.columns(3)
    if content_image is not None:
        with col1:
            # Content section
            st.subheader("Content Image")
            st.image(content_image)  # Adjust width as needed
    if style_image is not None:
        with col3:
            # style section
            st.subheader("Style Image")
            st.image(style_image)  # Adjust width as needed

st.title("Style Transfer (Content & Style)")
col1, col2,col3  = st.columns([5, 2, 5])
with col1:
    # Content section
    st.subheader("Content Image")
    content_image = st.file_uploader("Choose Content Image", type=["jpg", "png", "jpeg"])
with col3:
    # style section
    st.subheader("Style Image")
    style_image = st.file_uploader("Choose Style Image", type=["jpg", "png", "jpeg"])

if content_image is not None or style_image is not None:
  display_images(content_image, style_image)
 
def send_api_request_to_server(content_image,style_image,style_strength):
    style_strength_codes = [1e1,1e2,1e3,1e4,1e5,1e6,1e7,1e8,1e9,1e10]
    try:
        
        url = 'http://127.0.0.1:5000/style_transfer'
        # Read the images as numpy arrays
        content_image_array = np.array(process_image(content_image), dtype = np.uint8)
        style_image_array = np.array(process_image(style_image), dtype = np.uint8)
        # Create a dictionary with numpy arrays
        payload = {
            'content_image': content_image_array.tolist(),  # Convert to list for JSON serialization
            'style_image': style_image_array.tolist(),
            "style_strength": style_strength_codes[style_strength-1]
            
            }
        print("sending request to API")
        response = requests.post(url, json=payload)
        response_data = response.json()
        target_image_array = np.array(response_data["target_image"])
        st.image(target_image_array)
    except Exception as e:
        # Get the traceback information
        tb = traceback.format_exc()
        st.warning(f"Error:{str(e)}\n\n{tb}")
# Style Adjuster section
st.header("Style Adjuster")

strength = st.slider("Style applied with strength", min_value=1, max_value=10, step=1)

# Center the "Apply Style to Content Image" button
if st.button("Apply Style to Content Image"):
    if content_image is not None or style_image is not None:
        send_api_request_to_server(content_image,style_image,style_strength=strength)
        
        
        


