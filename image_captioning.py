from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def generate_caption(image: Image.Image) -> str:
    inputs = processor(image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def analyze_caption(caption: str) -> str:
    # Basic analysis: word count and sentence count
    words = len(caption.split())
    sentences = caption.count('.') + caption.count('!') + caption.count('?')
    analysis = f"Caption contains {words} words and {sentences} sentences."
    return analysis
