import streamlit as st
import replicate

# 讀取 API 金鑰（建議用 Streamlit Secrets 管理）
REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    st.error("請在 Streamlit Secrets 設定 REPLICATE_API_TOKEN")
    st.stop()

# 初始化 Replicate 客戶端
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

st.title("Replicate SDXL 圖像生成測試")

# 用戶輸入提示詞
prompt = st.text_input("請輸入圖像描述（prompt）", "A cat in a space suit, high quality, digital art")

if st.button("生成圖像"):
    with st.spinner("AI 生成中，請稍候..."):
        try:
            # 使用 SDXL 最新 tag（可至 Replicate 官網查詢）
            output = client.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 1024
                }
            )
            st.image(output[0], caption="生成結果")
        except Exception as e:
            st.error("生成失敗，請檢查 API 金鑰、模型 tag 或帳號額度。")
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
