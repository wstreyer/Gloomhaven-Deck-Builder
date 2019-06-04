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
thres = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 
# Blur
blur = cv2.medianBlur(thres, 3)

# Region of interest
H,W = blur.shape[:2]
print('H: {}, W:{}'.format(H, W))
(x,y,w,h) = (80, 130, 180, 30)
roi = blur[y:y+h, x:x+w]

# Save preprocessed image
tmpfile = "{}.png".format(os.getpid())
cv2.imwrite(tmpfile, roi)

# Show original and preprocessed images
#cv2.imshow("Image", image)
cv2.imshow("Output", roi)
#cv2.waitKey(0)

# load, parse, then delete preprocessed image
text = pytesseract.image_to_string(Image.open(tmpfile))
os.remove(tmpfile)
print(text)
