import os
import json
from datetime import datetime

import streamlit as st

# ---------------- Constants ---------------- #

IMAGE_DIR = "generated_images"
HISTORY_FILE = "history.json"

os.makedirs(IMAGE_DIR, exist_ok=True)

# ---------------- Save Image ---------------- #

def save_image(image):

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".png"

    filepath = os.path.join(
        IMAGE_DIR,
        filename,
    )

    image.save(filepath)

    return filepath


# ---------------- History ---------------- #

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(prompt, filename):

    history = load_history()

    history.append(
        {
            "prompt": prompt,
            "filename": filename,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4,
        )


# ---------------- Download Button ---------------- #

def create_download_button(filename):

    with open(filename, "rb") as file:

        st.download_button(
            label="⬇️ Download",
            data=file,
            file_name=os.path.basename(filename),
            mime="image/png",
            use_container_width=True,
        )