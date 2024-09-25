from cvzone.FaceDetectionModule import FaceDetector
import cvzone
import cv2



cap = cv2.VideoCapture(0)

detector = FaceDetector()

while True:

    success, img = cap.read()
    img, bboxs = detector.findFaces(img)

    if bboxs:
        for bbox in bboxs:

            center = bbox["center"]
            #score = int(bbox['score'][0] * 100)
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)

    cv2.imshow("Image", img)
    cv2.waitKey(1)