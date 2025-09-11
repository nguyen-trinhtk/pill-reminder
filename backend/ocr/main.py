import os
import time
from img_proc import preprocess_image
from ocr import ocr_core
from rx_parse import parse_rx

imgs_list = ['test1.png', 'test2.jpg', 'test3.jpg', 'test4.jpg', 'test5.jpg']

for img_name in imgs_list:
    path = os.path.join(os.getcwd(), f'img/{img_name}')
    
    start = time.perf_counter()
    
    img = preprocess_image(path)  # opencv image
    text = ocr_core(img)
    result = parse_rx(text)
    
    end = time.perf_counter()
    elapsed = end - start
    
    print(f"Image: {img_name} | Runtime: {elapsed:.4f} seconds")
    print(result)
    print()
