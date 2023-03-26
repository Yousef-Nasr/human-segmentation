import numpy as np
import tensorflow as tf
from tensorflow import keras
from io import BytesIO
from PIL import Image
import urllib.request
import requests
import streamlit as st
st.set_page_config(layout="wide",page_icon="🖼️", page_title="Selfie Background Remover")
from streamlit_cropper import st_cropper



# metric to evaluate the model
def dice_coeff(y_true, y_pred, smooth=1.0):
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
    '''prepare image to download '''
    buffered = BytesIO()
    path.save(buffered, format="JPEG")
    return buffered.getvalue()

def remove_background(path, size_img ,model=model):
    '''For make model prediction and upsample image to original size then return the result image'''
    predicted_mask = model.predict(image_process_for_model(path))[0]
    result = predicted_mask * load_original_image(path)
    #for upsampling image to original size
    result = (result * 255).astype(np.uint8)
    result = Image.fromarray(result.astype(np.uint8))
    result = result.resize(size_img, resample=Image.Resampling.LANCZOS) 
    return result


def main():
    '''main function for Streamlit app'''
    header_temp="""
                <div style="background: linear-gradient(to right, #ff5f6d, #ffc371); margin-bottom:20px;">
                <h2 style="color:white;text-align:center; font-family:unset;">Selfie Background Remover </h2>
                </div>
              """
    repo_temp="""
                <div style="background: linear-gradient(to left, #ff5f6d, #ffc371); margin-top:50px" >
                <h4 style="color:white;text-align:center; font-family:unset;">
                <a style="color:black; text-decoration:none; font-size:30px" href="https://github.com/Yousef-Nasr/human-segmentation">🚀 Git repository</a>
                </h4>
                </div>
              """
    st.markdown(header_temp,unsafe_allow_html=True)
    r_image, l_image = st.columns(2)
    option = st.sidebar.radio('Select input type:', ('Upload', 'URL'))
    if option == 'Upload':
        uploaded_file = st.sidebar.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            # display uploaded image
            r_image.image(uploaded_file, caption="original image", width=500)
            img = Image.open(uploaded_file)
            newimg = img.copy()
            real_size = img.copy()
            if newimg.size > (500, 500):
                newimg = newimg.resize((500, 500))
            #cropping box
            with st.expander('Crop'):
                r_crop, l_crop = st.columns(2, gap='large')
                with r_crop:
                    cropped_image = st_cropper(newimg, realtime_update=True, box_color="red", should_resize_image=False)
                    original_size_crop = cropped_image.size
                with l_crop:
                    if cropped_image is not None:
                        st.image(cropped_image.resize((256,256)), caption="Cropped Image", width=400)
    elif option == 'URL':
        url = st.sidebar.text_input('Enter an image URL')
        if url:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                r_image.image(img, caption="original image", width=500)
                newimg = img.copy()
                real_size = img.copy()
                if newimg.size > (500, 500):
                    newimg = newimg.resize((500, 500))
                with st.expander('Crop'):
                    r_crop, l_crop = st.columns(2, gap='large')
                    with r_crop:
                        cropped_image = st_cropper(newimg, realtime_update=True, box_color="red", should_resize_image=False)
                        original_size_crop = cropped_image.size
                    with l_crop:
                        if cropped_image is not None:
                            st.image(cropped_image, caption="Cropped Image", width=400)
            except:
                st.warning('URL is invalid', icon="🚨")
    done_btn_original = st.button('Remove Background from original image 🧙‍♂️', use_container_width=True)
    done_btn_cropped = st.button('Remove Background from cropped image ✂️', use_container_width=True)

    if done_btn_original:
        try:
            result = remove_background(newimg, size_img=real_size.size)
            l_image.image(result)
            st.success('Done !', icon="✅")
            download_btn = st.sidebar.download_button(
                        label='Download 💾',
                        data=prepare_image_to_download(result), 
                        file_name='SelfieBackgroundRemover_image.png',
                        mime=f'image/png')
            if download_btn:
                st.sidebar.success('Image downloaded', icon="✅")
        except:
            st.warning('Image is invalid', icon="⚠️")
    elif done_btn_cropped:
        try:
            result = remove_background(cropped_image.resize((256,256)), size_img=original_size_crop)
            l_image.image(result, width=400)
            st.success('Done !', icon="✅")
            download_btn = st.sidebar.download_button(
                        label='Download 💾',
                        data=prepare_image_to_download(result), 
                        file_name='SelfieBackgroundRemover_image.png',
                        mime=f'image/png')
            if download_btn:
                st.sidebar.success('Image downloaded', icon="✅")

        except:
            st.warning('Image is invalid', icon="⚠️")
    
    st.sidebar.markdown(repo_temp,unsafe_allow_html=True)

    
if __name__ == '__main__':
    main()
