import os
import streamlit as st
from PIL import Image
import replicate
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 取得 Replicate API 金鑰
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    st.error("請在 .env 檔案中設定 REPLICATE_API_TOKEN")
    st.stop()

# 初始化 Replicate 客戶端
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# 預設情境模板
SCENARIOS = {
    "節慶促銷": {
        "backgrounds": ["聖誕節", "春節", "黑色星期五"],
        "styles": ["寫實攝影", "3D 渲染", "插畫風格"],
        "prompt_template": "產品放置在{background}背景，搭配{discount}折扣標籤，風格為{style}。"
    },
    "產品展示": {
        "backgrounds": ["極簡工作室", "自然戶外", "現代廚房"],
        "styles": ["商業攝影", "低多邊形", "水彩畫"],
        "prompt_template": "產品特寫在{background}環境，強調{feature}功能，風格為{style}。"
    }
}

st.title("AI 創意圖像生成器")

# 上傳去背產品圖片
uploaded_file = st.file_uploader("請上傳去背的產品圖片（PNG格式）", type=["png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="上傳的產品圖片", use_column_width=True)

    # 選擇情境
    scenario_name = st.selectbox("選擇情境類型", list(SCENARIOS.keys()))
    scenario = SCENARIOS[scenario_name]

    # 選擇背景與風格
    background = st.selectbox("選擇背景", scenario["backgrounds"])
    style = st.selectbox("選擇風格", scenario["styles"])

    # 輸入折扣或功能，根據情境不同
    discount = ""
    feature = ""
    if "折扣" in scenario["prompt_template"]:
        discount = st.text_input("請輸入折扣訊息（例如：50% OFF）", "")
    if "功能" in scenario["prompt_template"]:
        feature = st.text_input("請輸入產品功能重點", "")

    # 按鈕觸發生成
    if st.button("生成創意圖像"):
        with st.spinner("正在呼叫 AI 生成圖片，請稍候..."):
            # 組合提示詞
            prompt = scenario["prompt_template"].format(
                background=background,
                discount=discount,
                style=style,
                feature=feature
            )

            try:
                # 呼叫 Replicate 的 Stable Diffusion XL 模型（可依需求換模型）
                output_urls = client.run(
                    "stability-ai/sdxl",
                    input={
                        "prompt": prompt,
                        "width": 1024,
                        "height": 1024,
                        "samples": 1,
                        "seed": None,
                        "steps": 30
                    }
                )
                # 顯示生成圖片
                for url in output_urls:
                    st.image(url, caption="AI 生成圖像", use_column_width=True)
                    st.download_button("下載圖片", url, file_name="creative_image.png")
            except Exception as e:
                st.error(f"生成失敗，錯誤訊息：{e}")
else:
    st.info("請先上傳去背的產品圖片。")
