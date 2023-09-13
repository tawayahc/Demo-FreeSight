import streamlit as st
from gtts import gTTS
from io import BytesIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

def convert_str_to_audio_data(audio_text):
    audio_data = BytesIO()
    tts = gTTS(audio_text, lang = "th")
    tts.write_to_fp(audio_data)

    return audio_data

st.title("Environment Scan👀")
st.header("โปรแกรมสแกนสิ่งแวดล้อม📃")
st.divider()
input_image = st.camera_input("📸กดถ่ายรูปเพื่อประมวลผล...", key = "firstCamera")

if input_image is not None:
    audio_text = "นี่เป็นการตรวจสอบเบื้องต้น ถ้าเป็นไปได้กรุณาตรวจสอบให้แน่ใจอีกครั้ง ผลลัพธ์คือ: "

    endpoint = "https://descriptivevision.cognitiveservices.azure.com/"
    subscription_key = "04006ca2373b48299415d41cbfaf2d22"

    credentials = CognitiveServicesCredentials(subscription_key)
    client = ComputerVisionClient(endpoint, credentials)

    max_candidates = 100

    result = client.describe_image_in_stream(input_image, max_candidates=max_candidates)

    captions = [caption.text for caption in result.captions]

    st.divider()
    st.subheader("ผลลัพธ์📑")
    if captions is not None:
        for caption in captions:
            st.write(caption)
            audio_text = audio_text + caption
    
    else:
        st.write("❌กรุณาถ่ายรูปอีกครั้งเพื่อประมวลผลใหม่")
        audio_text = "กรุณาถ่ายรูปอีกครั้ง เพื่อประมวลผลใหม่"

    audio_data = convert_str_to_audio_data(audio_text)

    st.subheader("เสียง🔊")
    st.audio(audio_data)