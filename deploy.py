import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
from urllib.request import urlopen
import urllib.request
import requests
import streamlit as st
from streamlit_cropper import st_cropper



# metric to evaluate the model
def dice_coeff(y_true: tf.Tensor, y_pred: tf.Tensor, smooth: float=1.0) -> tf.Tensor:
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    intersection = tf.reduce_sum(y_true * y_pred, axis=[1, 2, 3])
    union = tf.reduce_sum(y_true, axis=[1, 2, 3]) + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    dice = tf.reduce_mean((2.0 * intersection + smooth) / (union + smooth), axis=0)

    return tf.cast(dice, tf.float32)

# Register the custom metric
custom_objects = {'dice_coeff': dice_coeff}
tf.keras.utils.get_custom_objects().update(custom_objects)


# read the shareable link for the model file from a text file
with open('model_url.txt', 'r') as f:
    model_url = f.read().strip()

@st.cache_resource
def load_cached_model(model_url):
    '''Download and cash the model from the model_url'''

    # download the model file from Google Drive
    url = 'https://drive.google.com/uc?id=' + model_url.split('/')[-2]
    model_filename, headers = urllib.request.urlretrieve(url)

    # load the model from the downloaded file
    loaded_model = keras.models.load_model(model_filename)

    return loaded_model


# load the cached model
model = load_cached_model(model_url)

def load_original_image(path):
    '''load the original image '''
    img = path.resize((256, 256))
    img = np.array(img) / 255.0
    return img

def image_process_for_model(path):
    '''load the image and make preprocess for the model '''
    img = path.resize((256, 256))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def prepare_image_to_download(path):
    '''prepare image to download by make range(0, 255) '''
    path = (path * 255).astype(np.uint8)
    path = Image.fromarray(path)
    buffered = BytesIO()
    path.save(buffered, format="JPEG")
    return buffered.getvalue()

def remove_background(path, model=model):
    '''For make model prediction and return the result image'''
    predicted_mask = model.predict(image_process_for_model(path))[0]
    result = predicted_mask * load_original_image(path)
    return result

def main():
    '''main function for Streamlit app'''
    html_temp="""
                <div style="background: linear-gradient(to right, #ff5f6d, #ffc371);">
                <h2 style="color:white;text-align:center; font-family:unset">Selfie Background Remover</h2>
                </div>
              """
    st.markdown(html_temp,unsafe_allow_html=True)
    # upload image
    option = st.sidebar.radio('Select input type:', ('Upload', 'URL'))
    if option == 'Upload':
        uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            # display uploaded image
            image = st.image(uploaded_file, caption="original image",use_column_width=True)
            pil_img = Image.open(uploaded_file)
            newimg = pil_img.copy()
            #cropping box
            with st.expander('Crop'):
                cropped_image = st_cropper(newimg, realtime_update=True, box_color="red")
                if cropped_image is not None:
                    st.image(cropped_image.resize((256,256)), caption="Cropped Image", width=200)
    elif option == 'URL':
        url = st.text_input('Enter an image URL')
        if url:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                image = st.image(img, caption="original image", width=400)
                newimg = img.copy()
                with st.expander('Crop'):
                    cropped_image = st_cropper(newimg, realtime_update=True, box_color="red")
                    if cropped_image is not None:
                        st.image(cropped_image.resize((256,256)), caption="Cropped Image", width=200)
            except:
                st.warning('URL is invalid', icon="🚨")
    done_btn_original = st.button('Remove Background from original image 🧙‍♂️', use_container_width=True)
    done_btn_cropped = st.button('Remove Background from cropped image ✂️', use_container_width=True)
    if done_btn_original:
        try:
            result = remove_background(newimg)
            st.image(result, width=400)
            st.success('Done !', icon="✅")
            st.download_button(
                    label='Download 💾',
                    data=prepare_image_to_download(result), 
                    file_name='SelfieBackgroundRemover_image.png',
                    mime=f'image/png')
        except:
            st.warning('Image is invalid', icon="⚠️")
    elif done_btn_cropped:
        try:
            result = remove_background(cropped_image)
            st.image(result, width=400)
            st.success('Done !', icon="✅")
            st.download_button(
                        label='Download 💾',
                        data=prepare_image_to_download(result), 
                        file_name='SelfieBackgroundRemover_image.png',
                        mime=f'image/png')
        except:
            st.warning('Image is invalid', icon="⚠️")


    
if __name__ == '__main__':
    main()

