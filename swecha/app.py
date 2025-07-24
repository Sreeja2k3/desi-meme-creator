import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import io
import textwrap
import random
import datetime
import emoji

# Set page config
st.set_page_config(
    page_title="Desi Meme Creator",
    layout="centered",
    page_icon="🎭"
)

# Header with fun styling
st.markdown("""
    <h1 style='text-align: center; color: #ff6347;'> Desi Meme Creator</h1>
    <h4 style='text-align: center; color: #444;'>Meme banao, duniya hila do! 😎</h4>
""", unsafe_allow_html=True)

# Sidebar custom options
st.sidebar.title(" Customization Panel")

# Predefined desi templates
TEMPLATES = {
    "Sacred Games": "sacred_games.jpg",
    "Mirzapur": "mirzapur.jpg",
    "CID": "cid.jpg",
    "Kapil Sharma Show": "kapil.jpg",
    "Custom Upload": None
}

selected_template = st.sidebar.selectbox("🎞️ Choose Template", list(TEMPLATES.keys()))

uploaded_image = None
if selected_template == "Custom Upload":
    uploaded_file = st.sidebar.file_uploader("📤 Upload Your Image", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
else:
    default_path = os.path.join("templates", TEMPLATES[selected_template])
    if os.path.exists(default_path):
        uploaded_image = Image.open(default_path)

# Text input for meme
st.sidebar.markdown("---")
top_text = st.sidebar.text_input("🔼 Top Text", "Dekh Raha Hai Binod")
bottom_text = st.sidebar.text_input("🔽 Bottom Text", "Thoda Respect Dikhaiye")

# Font size
font_size = st.sidebar.slider("🔠 Font Size", 20, 100, 40)

# Font color
font_color = st.sidebar.color_picker("🎨 Font Color", "#FFFFFF")

# Emoji picker
emoji_list = ["😂", "🔥", "😎", "🤯", "🤡", "🥲"]
selected_emojis = st.sidebar.multiselect("😜 Add Emojis", emoji_list)

# Font style selection
fonts_dir = "fonts"
if os.path.exists(fonts_dir):
    font_files = [f for f in os.listdir(fonts_dir) if f.endswith(".ttf")]
else:
    font_files = []
selected_font = st.sidebar.selectbox("📝 Choose Font Style", font_files)

# Meme resizing options
st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 Resize Final Meme")
resize_width = st.sidebar.slider("Width (px)", 300, 1920, 640, step=10)
resize_height = st.sidebar.slider("Height (px)", 300, 1920, 640, step=10)

# Main logic to draw meme
if uploaded_image is not None and selected_font:
    img = uploaded_image.convert("RGB")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    try:
        font_path = os.path.join(fonts_dir, selected_font)
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        st.error(f"Font loading error: {e}")
        font = ImageFont.load_default()

    def draw_text(text, position):
        try:
            emoji_text = emoji.emojize(text + " " + " ".join(selected_emojis), language='alias')
        except:
            emoji_text = text + " " + " ".join(selected_emojis)
        wrapped = textwrap.fill(emoji_text, width=30)
        draw.text(position, wrapped, font=font, fill=font_color, stroke_width=2, stroke_fill="black")

    draw_text(top_text, (10, 10))
    draw_text(bottom_text, (10, height - font_size * 2))

    # Resize the final meme dynamically
    resized_img = img.resize((resize_width, resize_height))

    # Display meme
    st.image(resized_img, caption="🔥 Your Desi Meme 🔥", use_container_width=True)

    # Download button
    img_buffer = io.BytesIO()
    resized_img.save(img_buffer, format="PNG")
    st.download_button(
        label="📥 Download Meme",
        data=img_buffer.getvalue(),
        file_name=f"desi_meme_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.png",
        mime="image/png"
    )
else:
    st.info("👈 Start by customizing your meme from the sidebar!")

# Footer
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: small;'>
        Made with ❤️ by Desi Creators | Powered by Streamlit
    </div>
""", unsafe_allow_html=True)
