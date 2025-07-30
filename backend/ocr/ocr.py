import pytesseract
import cv2
import os

img_path = os.path.join('./img', 'test2.jpg')
img = cv2.imread(img_path)
if img is None:
    print(f"Image not found: {img_path}")
else:
    text = pytesseract.image_to_string(img)
    print(text)