import cv2
import numpy as np

#resource locations
imgpath = 'C:\\Users\\InnSight\Documents\\Github\Gloomhaven-Deck-Builder\\ghclass\\BR\\img'
imgfile = '18.png'

#Load image
data = cv2.imread('{}\{}'.format(imgpath, imgfile))
gray_img = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(gray_img, 5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

#Detection parameters
params = {'mdist': 12, 'p1': 30, 'p2': 15, 'minr': 0, 'maxr':4}

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,
                           params['mdist'],
                           param1 = params['p1'],
                           param2 = params['p2'],
                           minRadius = params['minr'],
                           maxRadius=  params['maxr'])
circles = np.uint16(np.around(circles))

#Plot all circles
for i in circles[0,:]:
   # draw the outer circle
   cv2.circle(data,(i[0],i[1]),i[2],(0,255,0),2)
   # draw the center of the circle
   #cv2.circle(data,(i[0],i[1]),2,(0,0,255),3)

#Show Data
#cv2.imwrite("data_circles.jpg", data)
cv2.imshow("HoughCirlces", data)
#cv2.waitKey()
#cv2.destroyAllWindows()