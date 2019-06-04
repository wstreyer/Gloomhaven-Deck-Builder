# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os

#tesseract binaries
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#source file
imgfile = 'C:\\Users\\InnSight\\Documents\\Github\\Gloomhaven-Deck-Builder\\ghclass\\BR\\img\\1.png'

# Grayscale
image = cv2.imread(imgfile)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
# Thresholding
gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# Blur
gray = cv2.medianBlur(gray, 3)
 
# Region of interest
top = [190, 80, 150, 160]
btm = [190, 315, 150, 150]
action = 'btm'


if action == 'top':
    (x,y,w,h) = tuple(top)
elif action == 'btm':
    (x,y,w,h) = tuple(btm)
else:
    pass
gray = gray[x:x+w, y:y+h]

# Save preprocessed image
tmpfile = "{}.png".format(os.getpid())
cv2.imwrite(tmpfile, gray)

# Show original and preprocessed images
cv2.imshow("Image", image)
cv2.imshow("Output", gray)
#cv2.waitKey(0)

# load, parse, then delete preprocessed image
text = pytesseract.image_to_string(Image.open(tmpfile))
os.remove(tmpfile)
print(text)
