import requests

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {"Authorization": "Bearer "}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


image_bytes = query({
    "inputs": "A Monster truck with Swamp deer sitting inside and a big bird sitting on it"
})
# You can access the image with PIL.Image for example
import io
from PIL import Image

image = Image.open(io.BytesIO(image_bytes))
image.save("hippo.png")
print("Image saved...")