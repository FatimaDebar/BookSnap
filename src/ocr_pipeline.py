import os
import cv2
import easyocr
import json

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# Paths
input_folder = 'C:\\Users\\HP\Desktop\\vscode\\BookSnap\\Book\\data\\raw_images'
output_folder = 'C:\\Users\\HP\\Desktop\\vscode\\BookSnap\\Book\\data\\ocr_results'

# Loop through images
results = {}
for filename in os.listdir(input_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        path = os.path.join(input_folder, filename)
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # OCR
        text = reader.readtext(gray, detail=0)
        results[filename] = text

# Save results
with open(os.path.join(output_folder, 'ocr_output.json'), 'w') as f:
    json.dump(results, f, indent=2)
