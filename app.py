import streamlit as st
from PIL import Image
import boto3

st.title('Celebrity Face Recognition')
img_file=st.file_uploader('Upload celebrity face',type=['png','jpg','jpeg'])

def load_img(img):
    img=Image.open(img)
    return img

if img_file is not None:
    file_details={}
    file_details['name']=img_file.name
    file_details['size']=img_file.size
    file_details['type']=img_file.type
    st.write(file_details)
    st.image(load_img(img_file),width=255)

    with open('inputsrc.jpg','wb') as f:
        f.write(img_file.getbuffer())
    
    st.success('Image Saved')
    client=boto3.client('rekognition')
    image=open('inputsrc.jpg','rb')
    response=client.recognize_celebrities(
        Image={'Bytes': image.read()}
    )
    st.write(response)
    try:
        st.success(response['CelebrityFaces'][0]['Name'])
        st.warning(response['CelebrityFaces'][0]['Urls'][0])
    except:
        st.error('No Celebrity Found')