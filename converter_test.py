import os
from pdf2image import convert_from_path

# 1. Configuration
# REPLACE THIS PATH with the actual path to your Poppler 'bin' folder!
POPPLER_PATH = r"C:\Users\Kalas\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin" 
PDF_PATH = "uploads/downloadfile.PDF" # Make sure a PDF exists here
OUTPUT_FOLDER = "processed"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def convert_pdf_to_images(pdf_path):
    print(f"--- Converting {pdf_path} ---")
    try:
        # 2. Convert PDF to list of PIL Image objects
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        
        image_paths = []
        for i, image in enumerate(images):
            # 3. Save each page as a JPEG
            image_name = f"page_{i+1}.jpg"
            save_path = os.path.join(OUTPUT_FOLDER, image_name)
            image.save(save_path, "JPEG")
            image_paths.append(save_path)
            print(f"Saved: {save_path}")
            
        return image_paths
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []

# Run the test
if __name__ == "__main__":
    # Ensure you have a PDF in your uploads folder to test this!
    test_pdf = os.path.join("uploads", os.listdir("uploads")[0]) if os.listdir("uploads") else None
    
    if test_pdf:
        convert_pdf_to_images(test_pdf)
    else:
        print("Please upload a PDF via your Flask app first so we have something to convert!")