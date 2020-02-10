import numpy as np
import cv2 as cv



def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img,(x,y),2,(255,0,0),-1)
        print('x: '+str(x)+ '   y: '+str(y))

alpha = 0.5

# Load an color image in grayscale
img = cv.imread('C:\\Users\\Kyle Bartido\\Documents\\FTP\\smallPoteka.jpg',1)
overlay = img.copy()
output = img.copy()

cv.namedWindow('image')
cv.setMouseCallback('image',draw_circle)

cv.rectangle(overlay, (420, 205), (595, 385),
		(0, 0, 255), -1)

cv.addWeighted(overlay, alpha, output, 1 - alpha,
		0, output)

while(1):
    cv.imshow('Output',output) 
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()


