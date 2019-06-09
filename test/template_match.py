# Python program to illustrate  
# template matching 
import cv2 
import numpy as np
import os

#resources
ghclass = 'CH'
index = 167
pcwd = os.path.dirname(os.getcwd())
imgpath = '{}\\ghclass\\{}\\img\\{}.png'.format(pcwd, ghclass, index)
iconpath = '{}\\icons'.format(pcwd)

# Specify a threshold 
threshold = 0.8

icon = 'temp'
  
# Read the main image 
img_rgb = cv2.imread(imgpath)
  
# Convert it to grayscale 
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 
  
# Read the template
(x,y,w,h) = (223, 171, 28, 28)
template = img_gray[y:y+h,x:x+w]    
  
# Perform match operations. 
res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED) 
  
# Store the coordinates of matched area in a numpy array 
best_res = cv2.minMaxLoc(res)
print(best_res[1])
best = best_res[3]
loc = np.where( res >= threshold)  
  
# Draw a rectangle around the matched regions 
for pt in zip(*loc[::-1]): 
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 1) 

#Draw the best match
cv2.rectangle(img_rgb, best, (best[0] + w, best[1] + h), (0,255,0), 4)  

#Highlight the actual template
cv2.rectangle(img_rgb, (x,y), (x+w,y+h), (0,0,255), 2)   

# Show the final image with the matched area
cv2.imshow('XCOR',res) 
cv2.imshow('Detected',img_rgb)
cv2.imshow('Template', template)

#Save template
cv2.imwrite('{}\{}.png'.format(iconpath, icon),template)

#Close all
cv2.waitKey(0)
cv2.destroyAllWindows()