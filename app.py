import streamlit as st
from image_generator import generate_image
from utils import (
    save_image,
    save_history,
    load_history,
    create_download_button,
)

# ---------------- Page Configuration ---------------- #

st.set_page_config(
    page_title="🎨 AI Image Generation Studio",
    page_icon="🎨",
    layout="wide",
)

# ---------------- Header ---------------- #

st.title("🎨 AI Image Generation Studio")
st.markdown(
    """
Generate stunning AI images using **OpenAI GPT Image**.
Customize the style, aspect ratio, and number of images.
"""
)

# ---------------- Sidebar ---------------- #

st.sidebar.header("⚙️ Image Settings")

style = st.sidebar.selectbox(
    "Art Style",
    [
        "Realistic",
        "Anime",
        "Oil Painting",
        "Watercolor",
        "Sketch",
        "Fantasy",
        "Cyberpunk",
        "3D Render",
        "Pixel Art",
    ],
)

aspect_ratio = st.sidebar.selectbox(
    "Aspect Ratio",
    [
        "1:1",
        "16:9",
        "9:16",
        "4:3",
        "3:2",
    ],
)

image_count = st.sidebar.slider(
    "Number of Images",
    min_value=1,
    max_value=4,
    value=1,
)

# ---------------- Prompt ---------------- #

prompt = st.text_area(
    "Describe the image",
    height=180,
    placeholder="Example: A futuristic city at sunset with flying cars.",
)

generate = st.button(
    "🎨 Generate Images",
    use_container_width=True,
)

# ---------------- Image Generation ---------------- #

if generate:

    if prompt.strip() == "":
        st.warning("Please enter a prompt.")
        st.stop()

    final_prompt = f"{prompt}\nStyle: {style}"

    with st.spinner("Generating image..."):

        try:

            images = generate_image(
                prompt=final_prompt,
                aspect_ratio=aspect_ratio,
                number_of_images=image_count,
            )

            st.success("Images generated successfully!")

            st.divider()

            cols = st.columns(2)

            for index, image in enumerate(images):

                filename = save_image(image)

                save_history(
                    prompt=final_prompt,
                    filename=filename,
                )

                with cols[index % 2]:

                    st.image(
                        image,
                        use_container_width=True,
                    )

                    create_download_button(filename)

        except Exception as e:

            st.error(f"Error: {e}")

# ---------------- History ---------------- #

st.divider()

st.header("🕘 Generation History")

history = load_history()

if len(history) == 0:

    st.info("No images generated yet.")

else:

    cols = st.columns(3)

    for index, item in enumerate(reversed(history)):

        with cols[index % 3]:

            st.image(
                item["filename"],
                use_container_width=True,
            )

            st.caption(item["prompt"])

            create_download_button(item["filename"])