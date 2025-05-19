import os
import streamlit as st
from PIL import Image
import replicate

# 取得金鑰（從 secrets）
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    st.error("請在 Streamlit Cloud 設定 Secrets: REPLICATE_API_TOKEN")
    st.stop()

client = replicate.Client(api_token=REPLICATE_API_TOKEN)

st.title("AI 圖像生成器")
uploaded_file = st.file_uploader("上傳產品圖片", type=["png", "jpg", "jpeg"])
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img)
    prompt = st.text_input("請輸入生成情境描述", "產品在溫馨廚房")
    if st.button("生成圖像"):
        with st.spinner("生成中..."):
            output = client.run(
                "stability-ai/sdxl",
                input={"prompt": prompt, "width": 1024, "height": 1024}
            )
            st.image(output[0])
