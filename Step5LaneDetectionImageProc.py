#---------******++++++ OPTIMIZING THE CURVE ++++++++******-----------

#Now we can subtract this value from the center to get the curve value. If we assume the center is at 240 then the curve value is 227- 240 = -13.
#Here the minus sign indicates the curve is towards the left side and the value 13 indicates the intensity of curve. But as we discussed earlier
#his method is not accurate since the middle can change.

#So to find the middle can simply use the function we just created, but this time instead of the complete image we will apply the histogram
#technique only on the bottom 1/4 part of the image. This is because we are interested in the average of the base so we don’t want to average
#the pixels above 1/4 the image. To achieve this we can add an input argument of region and based on the input value of this we can decide
#whether to average the whole image or part of it.

if region ==1:
      histValues = np.sum(img, axis=0)
  else :
      histValues = np.sum(img[img.shape[0]//region:,:], axis=0)

#So if the region is 1 the whole image will be average and if the region is 4 then on the 4th portion at the bottom will be averaged.
#Below image show the average of the bottom part.

#Now the average value we get is 278. This means the actual center of our image is 278 instead of 240. Now we can subtract our average
#value that we got before from this middle point. so 227 – 278 = -51 . Earlier our value was -13 and now we got -51 . Looking at the warpped
#image we can tell that the intensity of the curve is high therefore this confirms that the second method gives us better result.

middlePoint = utlis.getHistogram(imgWarp,minPer=0.5)
curveAveragePoint,imgHist = utlis.getHistogram(imgWarp, True, 0.9,1)
curveRaw = curveAveragePoint-middlePoint

#------******STEP 4 – Averaging--------*******

#Once we have the curve value we will append it in a list so that we can average this value. Averaging will allow smooth motion and will
#avoid any dramatic movements.

curveList.append(curveRaw)
if len(curveList) > avgVal:
    curveList.pop(0)
curve = int(sum(curveList)/len(curveList))

#-------*****STEP 5 – Display*******-----

#Now we can add options to display the final result . We will add an input argument to our main ‘getLaneCurve’ function so that we can have
#the flexibility of turning it on and off, since raspberry pi would run at very slow speeds if we display and run at the same time.

if display != 0:
       imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT,inv = True)
       imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:hT//3,0:wT] = 0,0,0
       imgLaneColor = np.zeros_like(img)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
       midY = 450
       cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
       cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = wT // 20
           cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
       fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
       cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
   if display == 2:
       imgStacked = utlis.stackImages(0.7,([img,imgWarpPoints,imgWarp],
                                         [imgHist,imgLaneColor,imgResult]))
       cv2.imshow('ImageStack',imgStacked)
   elif display == 1:
       cv2.imshow('Resutlt',imgResult)

#Stack Images Function

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

