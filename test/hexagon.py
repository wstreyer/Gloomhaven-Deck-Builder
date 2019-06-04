import cv2
import numpy as np

font = cv2.FONT_HERSHEY_COMPLEX

imgpath = 'C:\\Users\\InnSight\Documents\\Github\Gloomhaven-Deck-Builder\\ghclass\\SW\\img'
imgfile = '73.png'
img = cv2.imread('{}\{}'.format(imgpath, imgfile))
print(img.shape)
gray = cv2.imread('{}\{}'.format(imgpath, imgfile), cv2.IMREAD_GRAYSCALE)
_, threshold = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 900:
        approx = cv2.approxPolyDP(cnt, 0.03*cv2.arcLength(cnt, True), True)
        cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        print('{},{} - {} - {}'.format(x, y, len(approx), area))

top = [180, 80, 180, 30]
(x,y,w,h) = tuple(top)
cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 1) 
       
cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()