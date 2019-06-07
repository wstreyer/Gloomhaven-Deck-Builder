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

#Enhancement list
enhancements = []
def find_enchancements(data):
    img = cv2.medianBlur(data, 5)

    #Detection parameters
    (p1, p2, minr, maxr) = (30, 12, 1, 4)
    params = {'mdist': 10, 
            'p1': p1, 
            'p2': p2, 
            'minr': minr, 
            'maxr': maxr}

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,
                            params['mdist'],
                            param1 = params['p1'],
                            param2 = params['p2'],
                            minRadius = params['minr'],
                            maxRadius=  params['maxr'])
    circles = np.uint16(np.around(circles))

    #Find enhancement locations
    top = [180, 80, 150, 160]
    btm = [180, 315, 150, 150]
    for circ in circles[0,:]:
        #Dot parameters
        cx = circ[0]
        cy = circ[1]
        
        #Check Top/Btm Actions
        (xt,yt,wt,ht) = tuple(top)
        (xb,yb,wb,hb) = tuple(btm)
        if (xt < cx < xt+wt) and (yt < cy < yt+ht):
            #cv2.circle(img_rgb,(cx,cy),3,(0,255,0),2)
            enhancements.append({'xy': (cx,cy), 'action': 'top', 'type':''})
        elif (xb < cx < xb+wb) and (yb < cy < yb+hb):
            #cv2.circle(img_rgb,(cx,cy),3,(0,255,0),2)
            enhancements.append({'xy': (cx,cy), 'action': 'btm', 'type':''})
        else:
            pass

    #Find AoEs
    _, threshold = cv2.threshold(data, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hexes = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 900 < area < 1000:
            arc = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.03*arc, True)
            if len(approx) == 6:
                cv2.drawContours(img_rgb, [approx], 0, (0, 255, 0), 2)
                s = arc/6
                h = 0.5*s*np.sqrt(3)
                m = cv2.moments(approx)
                cx = m['m10']/m['m00']
                cy = m['m01']/m['m00']
                hexes.append({'xy': (cx, cy), 'length': s})

    #Mark the enhancement
    for e in enhancements:
        if len(hexes) > 0:
            for hex in hexes:
                d = distance(e['xy'], hex['xy'])
                if 34 < d < 40:
                    e['type'] = 'hex'
                    cv2.circle(img_rgb,e['xy'],3,(255,0,0),2)
                    break
            else:
                e['type'] = 'ability'
                #cv2.circle(img_rgb,e['xy'],3,(0,255,0),2)
        else:
            e['type'] = 'ability'
            #cv2.circle(img_rgb,e['xy'],3,(0,255,0),2)


###Start Here##            
#resources
ghclass = 'MT'
index = 137
pcwd = os.path.dirname(os.getcwd())
imgpath = '{}\\ghclass\\{}\\img\\{}.png'.format(pcwd, ghclass, index)
iconpath = '{}\\icons'.format(pcwd)

# Read the main image 
img_rgb = cv2.imread(imgpath)

# Convert it to grayscale 
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 

# Specify a threshold 
is_summon = False
threshold0 = 0.826
threshold1 = 0.74

#look for all known icons
icons = []
for icon in os.listdir(iconpath):   
    name = icon.split('.')[0]
    name = name.split('-')[0]
    
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
        print('{}: {} - {} - BEST'.format(name, best[1], (x,y)))
        icons.append({'xy': (x,y), 'type': name})
        #cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,0), 2)
        if name == '0summon':
            is_summon = True
    
    # Find all other matches above threshold
    loc = np.where( res >= threshold)  
    prev = (0,0)
    for pt in zip(*loc[::-1]):
        x = pt[0]
        y = pt[1]
        if distance(best[3], (x,y)) > 10 and distance(prev, (x,y)) > 10:
            print('{}: {} - {}'.format(name, res[(y,x)], (x,y)))
            icons.append({'xy': (x,y), 'type': name})
            #cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,255), 2)
        prev = (x,y)
  
#Look for enhancements
find_enchancements(img_gray)    

#Match icons with ability enhancements
for e in enhancements:
    if e['type'] == 'ability':
        for i in icons:
            dx = np.abs(e['xy'][0] - i['xy'][0])
            dy = np.abs(e['xy'][1] - i['xy'][1])
            if dx <= 90 and dy <= 17:
                e['type'] = i['type']
                print(e)
                cv2.circle(img_rgb,e['xy'],3,(0,255,0),2)
                x = i['xy'][0]
                y = i['xy'][1]
                cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,0), 2)
                break
        else:
            e['type'] = 'remove'
            print(e)
    else:
        print(e)

#Remove false enhancements
enhancements = [e for e in enhancements if not (e['type'] == 'remove')]
print(enhancements)

# Show the final image with the matched area
cv2.imshow('Detected', img_rgb)

#Close all
cv2.waitKey(0)
cv2.destroyAllWindows()