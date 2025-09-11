import cv2

def preprocess_image(img_path):
    try: 
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        mean = cv2.mean(img)[0]
        img = cv2.bilateralFilter(img, 15, 75, 75)
        _, img = cv2.threshold(img, mean - 20, 255, cv2.THRESH_BINARY)
        img = cv2.GaussianBlur(img, (1, 1), 0)
        return img
    except Exception as e: 
        print(f"Error processing image: {e}")
        return None
