import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import streamlit as st
from io import BytesIO
from PIL import Image
from urllib.request import urlopen

def dice_coeff(y_true: tf.Tensor, y_pred: tf.Tensor, smooth: float=1.0) -> tf.Tensor:
    
    """Compute the Dice coefficient between predicted and true masks.

    Args:
        y_true (tf.Tensor): True masks. Shape (batch_size, height, width, num_channels).
        y_pred (tf.Tensor): Predicted masks. Shape (batch_size, height, width, num_channels).
        smooth (float): Smoothing factor to avoid division by zero.

    Returns:
        tf.Tensor: Dice coefficient score.

    """
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    union = tf.reduce_sum(y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    dice = tf.reduce_mean((2.0 * intersection + smooth) / (union + smooth), axis=0)

    return tf.cast(dice, tf.float32)

custom_objects = {'dice_coeff': dice_coeff}
tf.keras.utils.get_custom_objects().update(custom_objects)


def load_img(path):
    #img = Image.open(path)
    img = path.resize((256, 256)) # resize to the input size of your model
    img = np.array(img) / 255.0
    return img
def pre_image(path):
    #img = Image.open(path)
    img = path.resize((256, 256)) # resize to the input size of your model
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def mask_image(path):
    model = keras.models.load_model('humanSegmentationFinal.h5')
    predicted_mask = model.predict(pre_image(path))[0]
    return predicted_mask

def main():
    html_temp="""
                <div style="background-color:red">
                <h2 style="color:white;text-align:center;">Selfie Background Remover </h2>
                </div>
              """
    st.markdown(html_temp,unsafe_allow_html=True)
    # upload image
    uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])

    # check if image is uploaded
    if uploaded_file:
        # display uploaded image
        image = st.image(uploaded_file, caption="original image", width=300)

        # copy uploaded_file and display copy
        # newimg = uploaded_file
        # st.image(newimg, caption="newimg", width=100)

        # # open uploaded_file as PIL image
        pil_img = Image.open(uploaded_file)
        # image = st.image(pil_img, caption="PIL image")

        # # use PIL.Image.copy() and display copied image
        newimg = pil_img.copy() # "copy the input data in another variable"
        # st.image(newimg, caption="Copy of PIL image", width=200)
    
    result = 0
    def show():
        result = mask_image(newimg)
        image_result = st.image(result * load_img(newimg), width=400)
    r = st.button('predict', on_click=show())
    st.success('Done !')

    
if __name__ == '__main__':
    main()

