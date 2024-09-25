import os
import cv2
import pickle
import face_recognition as frec
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime



cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "ENTER YOUR URL HERE",
    'storageBucket':"ENTER YOUR URL HERE"
})

#encodeListKnown = encoded_list
#encodeListKnownIds = encoded_list_id
#studentIds = student_id
#imgS = img_smaller

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('rs/background.png')

#importing the mode images into a list
folderModePath = 'rs/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread (os.path.join (folderModePath, path)))

print("loading encoded file")
#load the encoding file
file = open('encodeFile.p', 'rb')
encoded_list_id = pickle.load(file)
file.close()
encoded_list, student_id = encoded_list_id
print(student_id)
print("encoded file loaded")


modeType = 0
counter = 0
id = -1
img_student = []


while True:
    success, img = cap.read()

    img_smaller = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_smaller = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_currFrame = frec.face_locations(img_smaller)
    encode_currFrame = frec.face_encodings(img_smaller, face_currFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    

    if face_currFrame:
        for encodeFace, faceLoc in zip(encode_currFrame, face_currFrame):
            matches = frec.compare_faces(encoded_list, encodeFace)
            faceDist = frec.face_distance(encoded_list, encodeFace)
            
            #print("matches", matches)
            #print("faceDist", faceDist)

            match_index = np.argmin(faceDist)
            #print("match_index", match_index)

            if matches[match_index]:
                
                """
                print("known face detected")
                print(student_id[match_index])
                """
                
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                #imgBackground = cvzone.cornerRect(imgBackground, bbox, rt = 0)
                #imgBackground = cv2.rectangle(imgBackground, (x1, y1), (x2, y2 - y1), (0, 255, 0), 2)
                
                id = student_id[match_index]
                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("face attendance", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1


        if counter != 0:
            if counter == 1:
                #get the data
                student_info = db.reference(f'students/{id}').get()
                print(student_info)

                #get the image from storage
                blob = bucket.get_blob(f'images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                img_student = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                #update the data of attendance
                datetimeObject = datetime.strptime(student_info['last attendance'],
                                                    "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                if secondsElapsed > 30:
                    ref = db.reference(f'students/{id}')
                    student_info['total attendance'] += 1
                    ref.child('total attendance').set(student_info['total attendance'])
                    ref.child('last attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 3
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    

            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                if counter < 10:
                    cv2.putText(imgBackground, str(student_info['total attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(student_info['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(student_info['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(student_info['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(student_info['starting year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    
                    (w, h), _ = cv2.getTextSize(student_info['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(student_info['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = img_student
            
                counter += 1
                if counter >= 20:
                    counter = 0
                    modeType = 0
                    student_info = []
                    img_student= []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]



    else:
        modeType = 0
        counter = 0

    cv2.imshow("face attendance", imgBackground)
    cv2.waitKey(1)