from PIL import Image
import streamlit as st
import numpy as np
import zxingcpp

st.title("Smart Buy💵")
st.header("QR Scanner📷")
st.divider()

input_image_BQ = st.camera_input("📸กดถ่ายรูปเพื่อประมวลผล...", key = "firstCamera")

if input_image_BQ is not None:
    img = Image.open(input_image_BQ)
    img_array = np.array(img)

    formatted_image = (Image.fromarray(img_array)).convert('L')

    decoded_data = zxingcpp.read_barcodes(formatted_image)

    st.divider()
    st.subheader("ผลลัพธ์📑")
    if len(decoded_data) != 0:
        for data in decoded_data:
            st.write(data.text)
    else:
        st.write("❌ตรวจไม่พบ QRCode กรุณาถ่ายรูปอีกครั้งเพื่อประมวลผลใหม่")