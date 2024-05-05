import traceback
import sys
import numpy as np
from fastapi import FastAPI, HTTPException, Request, File
import uvicorn
import io
import base64
import time
import Style_transform_algorithm
from PIL import Image
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/style_transfer")
async def apply_style_transfer(payload_received: dict):
    try:
        print("request recived")
        print("np.array(payload_received[content_image]):",np.array(payload_received["content_image"]).shape)
        print("np.array(payload_received[style_image])",np.array(payload_received["style_image"]).shape)
        content_image = np.array(payload_received["content_image"])
        style_image = np.array(payload_received["style_image"])
        content_image = content_image.astype(np.uint8)
        style_image = style_image.astype(np.uint8)
        # content_image = Image.fromarray(content_image)
        # style_image = Image.fromarray(style_image)
        # print("content_image",content_image.shape)
        # print("style_image",style_image.shape)
        numepochs = 1500
        styleScaling = payload_received["style_strength"]
        learning_rate = 0.005
        layers4content = ['ConvLayer_1', 'ConvLayer_4']
        layers4style = ['ConvLayer_1', 'ConvLayer_2', 'ConvLayer_3', 'ConvLayer_4', 'ConvLayer_5']
        weights4style = [1, .5, .5, .2, .1]
        start_time = time.time()
        styleobject = Style_transform_algorithm.Style_transfer(content_image=content_image, style_image=style_image)
        print("images send to the style transfer")
        styleobject.load_vgg19_model_and_freez_weights()
        print("model loaded")
        styleobject.prepare_images()
        print("prepare the target image")
        styleobject.image_transformations()
        print("do the image transformations")

        styleobject.select_layers(layers4content=layers4content,
                                  layers4style=layers4style,
                                  weights4style=weights4style)

        styleobject.train_the_image(numepochs=numepochs,
                                    styleScaling=styleScaling,
                                    learning_rate=learning_rate)
        target_image = styleobject.get_trained_image()
        #print("app target_image",target_image)
        end_time = time.time()
        print(f"Execution time for {numepochs} is {end_time - start_time} seconds")

        # Assume you have processed and obtained the target image as a numpy array
        target_image_array = np.array(target_image)

        # Return the target image as a numpy array
        #print("target_image_array.tolist():",target_image_array.tolist())
        return {"target_image": target_image_array.tolist()}  # Convert to list for JSON serialization
    except Exception as e:
        # Get the traceback information
        tb = traceback.format_exc()
        # Include the traceback in the detail of the HTTPException
        return HTTPException(status_code=500, detail=f"{str(e)}\n\n{tb}")



