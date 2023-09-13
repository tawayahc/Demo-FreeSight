import requests
import streamlit as st
import numpy as np
import zxingcpp
from PIL import Image
from googletrans import Translator
from gtts import gTTS
from io import BytesIO

def getdetails(barcode):
    base_url = "https://world.openfoodfacts.org/api/v0/product/"
    url = f"{base_url}{barcode}.json"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        product_name = data["product"]["product_name"]
        ingredients = data["product"]["ingredients_text"]
        nutrition_facts = data["product"]["nutriments"]
        # Extract more information as required

        # Return the relevant information
        return product_name, ingredients, nutrition_facts
    else:
        # Handle request errors
        print("Request failed.")
        return None

def convert_str_to_audio_data(audio_text):
    audio_data = BytesIO()
    tts = gTTS(audio_text, lang = "th")
    tts.write_to_fp(audio_data)

    return audio_data

base_url = "https://world.openfoodfacts.org/api/v0/product/"
translator = Translator()

st.title("Smart Sight👀")
st.header("โปรแกรมช่วยการรับรู้ข้อมูลของผลิตภัณฑ์📃")
st.divider()
input_image = st.camera_input("📸กดถ่ายรูปเพื่อประมวลผล...", key = "firstCamera")

if input_image is not None:
    img = Image.open(input_image)
    img_array = np.array(img)
    
    barcodes = zxingcpp.read_barcodes(img)

    for result in barcodes:
        num_barcode = result.text

    if len(barcodes) == 0:
        st.divider()
        st.subheader("ผลลัพธ์📑")
        st.write("❌ไม่พบฉลากของผลิตภัณฑ์ กรุณาถ่ายรูปอีกครั้งเพื่อประมวลผลใหม่")
        audio_text = "ไม่พบฉลากของผลิตภัณฑ์ กรุณาถ่ายรูปอีกครั้งเพื่อประมวลผลใหม่"
    else:
        url = f"{base_url}{num_barcode}.json"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            product_name = data["product"]["product_name"]
            ingredients = data["product"]["ingredients_text"]
            nutrition_facts_dict = data["product"]["nutriments"]


            # productname_th = (translator.translate(product_name, dest="th"))
            # ingredients_th = (translator.translate(ingredients, dest="th"))
            # nutrition_facts_dict
            nutrition_facts_data = ""
            for item in nutrition_facts_dict:
                if "_" or "-" not in item:
                    nutrition_facts_data = nutrition_facts_data + item + ": " + str(nutrition_facts_dict.get(item))
                if "_unit" in item:
                    unit = nutrition_facts_dict.get(item)
                    nutrition_facts_data = nutrition_facts_data + nutrition_facts_dict.get(item) + ", "
                
                # if check != "0" and check != "" and check != "g":
                #     subtext = item + check + ', '
                #     subtext = subtext.replace("_", " ")
                #     subtext = subtext.replace("-", " ")
                #     # nutrition2 = translator.translate(string, dest="th").text
                #     # nutritionfacts_th = nutritionfacts_th + nutrition2
                #     nutrition_facts_data = nutrition_facts_data + subtext
        
            st.divider()
            st.subheader("ผลลัพธ์📑")
            st.write("Product Name: " + product_name)
            # st.write("productname_th: " + productname_th)
            st.write("Ingredients: " + ingredients)
            # st.write("ingredients_th: " + ingredients_th)
            st.write("Nutrition Facts: " + nutrition_facts_data)
            # st.write("nutritionfacts_th: " + nutritionfacts_th)
            audio_text = "Product Name: " + product_name + "Ingredients: " + ingredients

    audio_data = convert_str_to_audio_data(audio_text)

    st.subheader("เสียง🔊")
    st.audio(audio_data)