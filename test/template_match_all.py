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
def find_enchancements(data, summon = 'none'):
    img = cv2.medianBlur(data, 5)

    #Detection parameters
    (p1, p2, minr, maxr) = (30, 12, 1, 4)
    params = {'mdist': 10, 
            'p1': p1, 
            'p2': p2, 
            'minr': minr, 
            'maxr': maxr}

    cv2.imshow('', img)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,
                            params['mdist'],
                            param1 = params['p1'],
                            param2 = params['p2'],
                            minRadius = params['minr'],
                            maxRadius=  params['maxr'])
    circles = np.uint16(np.around(circles))

    print(len(circles[0,:]))

    #Find enhancement locations
    if summon == 'top':
        (xt,yt,wt,ht) = (35, 75, 300, 165)
        (xb,yb,wb,hb) = (180, 310, 150, 155)
    elif summon == 'btm':
        (xt,yt,wt,ht) = (180, 75, 150, 165)
        (xb,yb,wb,hb) = (35, 310, 300, 155)
    else:
       (xt,yt,wt,ht) = (175, 75, 155, 165)
       (xb,yb,wb,hb) = (175, 310, 155, 155)
    
    #Show bounding box
    cv2.rectangle(img_rgb, (xt,yt), (xt+wt, yt+ht), (0,255,255), 2)
    cv2.rectangle(img_rgb, (xb,yb), (xb+wb, yb+hb), (0,255,255), 2)
    
    for circ in circles[0,:]:
        #Dot parameters
        cx = circ[0]
        cy = circ[1]
        
        #Check Top/Btm Actions
        if (xt < cx < xt+wt) and (yt < cy < yt+ht):
            #cv2.circle(img_rgb,(cx,cy),3,(0,255,0),2)
            enhancements.append({'xy': (cx,cy), 'action': 'top', 'type':'ability', 'active': False})
        elif (xb < cx < xb+wb) and (yb < cy < yb+hb):
            #cv2.circle(img_rgb,(cx,cy),3,(0,255,0),2)
            enhancements.append({'xy': (cx,cy), 'action': 'btm', 'type':'ability', 'active': False})
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
                #cv2.circle(img_rgb,e['xy'],3,(0,255,0),2)
                pass
        else:
            #cv2.circle(img_rgb,e['xy'],3,(0,255,0),2)
            pass


###Start Here##            
#resources
ghclass = 'BR'
index = 3
pcwd = os.path.dirname(os.getcwd())
imgpath = '{}\\ghclass\\{}\\img\\{}.png'.format(pcwd, ghclass, index)
iconpath = '{}\\icons'.format(pcwd)

# Read the main image 
img_rgb = cv2.imread(imgpath)

# Convert it to grayscale 
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY) 

# Specify a threshold 
thresholds = [{'icons': ['attack', 'move', 'heal', 'shield', 'retaliate'], 'threshold': 0.89},
              {'icons': ['range', 'invisible', 'wound', 'immobilize'], 'threshold': 0.72},
              {'icons': ['summon', 'target', 'push', 'pull'], 'threshold': 0.86},
              {'icons': ['pierce', 'poison'], 'threshold': 0.89}]

#look for all known icons
icons = []
for icon in os.listdir(iconpath):   
    name = icon.split('.')[0]
    name = name.split('-')[0]
    
    #Choose threshold from thresholds
    for t in thresholds:
        if name in t['icons']:
            threshold = t['threshold']
            break      
    
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
        #print('{}: {} - {} - BEST'.format(name, best[1], (x,y)))
        action = 'top' if y <= 262 else 'btm'
        icons.append({'xy': (x,y), 'size': (w,h), 'type': name, 'action': action, 'match': best[1]})
        print(icons[-1])
        cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,255), 2)
    
    # Find all other matches above threshold
    loc = np.where( res >= threshold)  
    prev = (0,0)
    for pt in zip(*loc[::-1]):
        x = pt[0]
        y = pt[1]
        if distance(best[3], (x,y)) > 10 and distance(prev, (x,y)) > 10:
            #print('{}: {} - {}'.format(name, res[(y,x)], (x,y)))
            action = 'top' if y <= 262 else 'btm'
            icons.append({'xy': (x,y), 'size': (w,h), 'type': name, 'action': action, 'match': res[(y,x)]})
            print(icons[-1])
            cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,255), 2)
        prev = (x,y)        
  
#Look for enhancements
#Check if card has a summon and which action it is (top or btm)
summon = 'none'
for i in icons:
    if i['type'] == 'summon': 
        print('Summon on {} action'.format(i['action']))
        summon = i['action']    
        break
find_enchancements(img_gray, summon=summon)

#Match icons with ability enhancements
for e in enhancements:
    if e['type'] == 'ability':
        for i in icons:
            dx = e['xy'][0] - i['xy'][0]
            dy = e['xy'][1] - i['xy'][1]
            #print('({}, {})'.format(dx, dy))
            
            xmax = 60 if i['action'] == summon else 90
            if 37 <= dx <= xmax and 0 < dy <= 17:
                if i['type'] == 'heal' and i['action'] == summon:
                    e['type'] = 'health' if i['action'] == summon else i['type']
                else:
                    e['type'] = i['type']
                print(e)
                cv2.circle(img_rgb,e['xy'],3,(0,255,0),2)
                x = i['xy'][0]
                y = i['xy'][1]
                w = i['size'][0]
                h = i['size'][1]
                cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,255,0), 2)
                break
        else:
            e['type'] = 'remove'
            print(e)
    else:
        print(e)

#Remove false enhancements
enhancements = [e for e in enhancements if not (e['type'] == 'remove')]


# Show the final image with the matched area
cv2.imshow('Detected', img_rgb)

#Close all
cv2.waitKey(0)
cv2.destroyAllWindows()