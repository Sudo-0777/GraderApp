import cv2
import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

# 1. Load Model
processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

# 2. Tight Manual Crop
img = cv2.imread('WhatsApp Image 2026-02-18 at 6.00.11 PM.jpeg')
# Standardizing size to help with the crop
img = cv2.resize(img, (1000, 500)) 

# Crop to the specific area where the text sits 
# [y_start:y_end, x_start:x_end]
# This removes the vast majority of the "distracting" notebook lines
crop_img = img[120:280, 300:900] 

# Convert to PIL
final_image = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))

# 3. Process with higher 'length_penalty' to prevent it from adding extra words
pixel_values = processor(images=final_image, return_tensors="pt").pixel_values

with torch.no_grad():
    generated_ids = model.generate(
        pixel_values, 
        num_beams=5,
        max_length=20,
        length_penalty=1.0 # Keeps the output concise
    )

generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(f"Targeted Result: {generated_text}")