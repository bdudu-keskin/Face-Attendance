import cv2
import face_recognition as frec
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendance-67f39-default-rtdb.firebaseio.com/",
    'storageBucket':"faceattendance-67f39.appspot.com"
})



#encodeListKnown = encoded_list
#encodeListKnownIds = encoded_list_id
#studentIds = student_id
#imgS = img_smaller



#importing the student images into a list
folderPath = 'images'
pathList = os.listdir(folderPath)
imgList = []
student_ids = []

for path in pathList:
    imgList.append(cv2.imread (os.path.join (folderPath, path)))
    #print(os.path.splitext(path)[0])
    student_ids.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)




def find_encodings(img_list):
    
    encode_list = []

    for img in img_list:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = frec.face_encodings(img)[0]
        encode_list.append(encode)

    return encode_list

print("encoding started...")
encoded_list = find_encodings(imgList)
encoded_list_id = [encoded_list, student_ids]
print("encoding complete")

file = open("encodeFile.p", 'wb')
pickle.dump(encoded_list_id, file)
file.close()
print("file saved")