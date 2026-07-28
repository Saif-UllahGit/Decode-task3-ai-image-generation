import os
import base64
from io import BytesIO

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

# ---------------- Load Environment ---------------- #

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ---------------- Aspect Ratio Mapping ---------------- #

SIZE_MAP = {
    "1:1": "1024x1024",
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "4:3": "1024x1024",
    "3:2": "1536x1024",
}

# ---------------- Image Generation ---------------- #

def generate_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    number_of_images: int = 1,
):
    """
    Generate AI images using OpenAI GPT Image.
    Returns a list of PIL Image objects.
    """

    size = SIZE_MAP.get(aspect_ratio, "1024x1024")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size=size,
        n=number_of_images,
    )

    images = []

    for item in response.data:

        image_bytes = base64.b64decode(item.b64_json)

        image = Image.open(
            BytesIO(image_bytes)
        )

        images.append(image)

    return images