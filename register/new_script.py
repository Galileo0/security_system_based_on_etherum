"""
Created on Wed Jun 20 14:04:10 2018
@author: bharathiraja - https://ampersandacademy.com/tutorials/python-data-science
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string

# Path of working folder on Disk
src_path = "images/"

def get_string(img_path):
    # Read image with opencv
    img = cv2.imread(img_path)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    #cv2.imwrite(src_path + "removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    #cv2.imwrite(src_path + "thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "Card2.png"))

    # Remove template file
    #os.remove(temp)

    return result


print('--- Start recognize text from image ---')
#print(get_string(src_path + "Card1.png") )

recon_string = get_string(src_path + "Card2.png")
recon_string = recon_string.replace('\n\n', '\n')

name = recon_string[0]
age =  recon_string[1]
sex =  recon_string[2]
job =  recon_string[3]
car_num = recon_string[4]



#print recon_string

result = pytesseract.image_to_string(Image.open(src_path + "Card2.png"))
print result
print("------ Done -------")