# Python program to illustrate  
# template matching 
import cv2 
import numpy as np 
import os

def distance(p1: tuple, p2: tuple):
    sum = 0
    if len(p1) != len(p2):
        return None
    else:
        for (a, b) in zip(p1, p2):
            sum += (b - a)**2
    return np.sqrt(sum)
    
#resources
imgpath = 'C:\\Users\\InnSight\\Documents\\Github\\Gloomhaven-Deck-Builder\\ghclass\\TI\\img\\51.png'
iconpath = 'C:\\Users\\InnSight\\Documents\\Github\\Gloomhaven-Deck-Builder\\icons'

# Specify a threshold 
is_summon = False
threshold0 = 0.826
threshold1 = 0.74
  
# Read the main image 
img_rgb = cv2.imread(imgpath)
  
# Convert it to grayscale 
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 

#look for all known icons
for icon in os.listdir(iconpath):   
    if is_summon:
        threshold = threshold1
    else:
        threshold = threshold0
    
    # Read the template icon
    template = cv2.imread(os.path.join(iconpath, icon),0)
    w, h = template.shape[::-1]
    
    # Perform match operations. 
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    
    # Find the best match above threshold 
    best = cv2.minMaxLoc(res)
    if best[1] >= threshold:
        x = best[3][0]
        y = best[3][1]
        print('{}: {} - {} - BEST'.format(icon.split('.')[0], best[1], (x,y)))
        cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,0), 2)
        if icon.split('.')[0] == '0summon':
            is_summon = True
    
    # Find all other matches above threshold
    loc = np.where( res >= threshold)  
    prev = (0,0)
    for pt in zip(*loc[::-1]):
        x = pt[0]
        y = pt[1]
        if distance(best[3], (x,y)) > 10 and distance(prev, (x,y)) > 10:
            print('{}: {} - {}'.format(icon.split('.')[0], res[(y,x)], (x,y)))
            cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,255), 2)
        prev = (x,y)
  
# Show the final image with the matched area
cv2.imshow('Detected', img_rgb)

#Close all
cv2.waitKey(0)
cv2.destroyAllWindows()