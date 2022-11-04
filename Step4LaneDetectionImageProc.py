#+++++++++********------- FINDING THE CURVE --------*******++++++++++

#First we will declare our function that will take image as an input argument. The we will simply sum all the pixels in the y direction .
#Achieving this is easier than it sounds as it requires just one line of code.

def getHistogram(img,display=False,minVal = 0.1,region= 4):

    histValues = np.sum(img, axis=0)

#Here histValues are the 480 values that contain the sum of each column.

#Now some of the pixels in our image might just be noise. So we don’t want to use them in our calculation . Therefore we will set a threshold
#value which will be the minimum value required for any column to qualify as part of the path and not noise. We can set a hard-coded value but
#it is better to get it based on the live data. So we will find the maximum sum value and multiply our user defined percentage to it to create
#our threshold value.

maxValue = np.max(histValues)  # FIND THE MAX VALUE
minValue = minPer*maxValue

#Now we can simply add all the number of pixels on each side and find left right or straight direction. But this is not what we want,
#if the curve is right we want to know how much right. To get the value of the curvature we will find the indices of all the columns that
#have value more than our threshold and then we will average our indices. This means that if our pixels indices started from 30 and ended at
#300, our average would be (300-30)/2 +30 = 165.

indexArray =np.where(histValues >= minValue) # ALL INDICES WITH MIN VALUE OR ABOVE
basePoint =  int(np.average(indexArray)) # AVERAGE ALL MAX INDICES VALUES

#The base value is now the average base point of our image. We can draw this base point to visualize better.

if display:
    imgHist = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
    for x,intensity in enumerate(histValues):
       # print(intensity)
        if intensity > minValue:color=(255,0,255)
        else: color=(0,0,255)
        cv2.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-(intensity//255//region)),color,1)
    cv2.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv2.FILLED)
