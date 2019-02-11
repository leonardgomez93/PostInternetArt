import cv2
import time
import datetime
import pysftp
from random import *
from time import strftime


img_counter = 10
oldDate = datetime.date.today()
randomTime = ""
timeStamps = ""
#print(strftime("%H:%M:%S"))


def generateRandomTime():
    hour = randint(0, 23)
    minute = randint(0,59)
    second = randint(0,59)
    hourStr = ""
    minuteStr = ""
    secondStr = ""
    if hour < 10:
        hourStr = "0" + str(hour)
    else:
        hourStr = str(hour)

    if minute < 10:
        minuteStr = "0" + str(minute)
    else:
        minuteStr = str(minute)

    if second < 10:
        secondStr = "0" + str(second)
    else:
        secondStr = str(second)

    return hourStr + ":" + minuteStr + ":" + secondStr

def sftpUpload(count):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  
    with pysftp.Connection('vergil.u.washington.edu', username='leogomz', password='*******', port=22, cnopts=cnopts) as sftp:
        sftp.put('/Users/leonardgomez/Documents/opencv_frame_' + str(count) + '.png','/nfs/bronfs/uwfs/dw00/d30/leogomz/blog/pictures/' + str(count) + '.png')  
        sftp.put('/Users/leonardgomez/Documents/imgCount.txt','/nfs/bronfs/uwfs/dw00/d30/leogomz/blog/pictures/imgCount.txt')
        sftp.put('/Users/leonardgomez/Documents/timeStamps.txt','/nfs/bronfs/uwfs/dw00/d30/leogomz/blog/pictures/timeStamps.txt') 
        sftp.close()
        
randomTime = generateRandomTime()

while True:
    currentDate = datetime.date.today()
    currentDateString = currentDate.strftime("%m/%d/%y")
    currentTime = strftime("%H:%M:%S")
    #print (currentTime + " " + currentDateString + "     " + randomTime)
    if currentDate != oldDate:
        oldDate = currentDate
        randomTime = generateRandomTime()
    #print(randomTime)
    #print ("Current date: ", currentDate)
    #print(currentTime)
    if randomTime == currentTime:
        fo1 = open("imgCount.txt", "w+")
        fo2 = open("timeStamps.txt", "w+")
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("test")
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break    
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 2])
        print("{} written!".format(img_name))
        timeStamps = currentDateString + "  "+ currentTime + "\n" + timeStamps
        fo1.write(str(img_counter))
        fo1.close()
        fo2.write(timeStamps)
        fo2.close()
        sftpUpload(img_counter)
        img_counter += 1
        cam.release()
        cv2.destroyAllWindows()
