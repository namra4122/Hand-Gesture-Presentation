import os
import numpy as np
import cv2
from cvfpsCalc import CvFpsCalc
from cvzone.HandTrackingModule import HandDetector

# ppt to png_folder
from ppt2img import PPTConverter

ppt_path = input("Enter a file path: ")
print(ppt_path)

if not os.path.exists(ppt_path):
    print("INVALID PATH")
    exit()

output_folder = "ppt2pngOutput/"

converter = PPTConverter()
converter.set_ppt_path(ppt_path)
converter.convert_to_images(output_folder)

# hand Gesture

# Variables
width, height = 1280, 720
gestureThreshold = int(height / 2)
buttonPressed = False
btnCount = 0
btnDelay = 20
annotNumber = 0
annotStart = False
annotations = [[]]

# fps calc mode
cvFpsCalc = CvFpsCalc(buffer_len=10)
# print("FPS:"+cvFpsCalc)

# camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# presentation_img path
slidePath = sorted(os.listdir(output_folder), key=len)
# print(slidePath)

# slide Number
slideNumber = 0
hs, ws = int(120 * 1), int(213 * 1)

# hand detector
detector = HandDetector(detectionCon=0.3, maxHands=1)
handFlip = False

while True:
    fps = cvFpsCalc.get()

    # webcame frames
    success, img = cap.read()
    img = cv2.flip(img, 1)  # mirror cam frame

    # slide images
    currentSlidePath = os.path.join(output_folder, slidePath[slideNumber])
    currentSlide = cv2.imread(currentSlidePath)

    # hand detection
    hands, img = detector.findHands(img, flipType=handFlip)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 1)

    # find no. of figures
    if hands and not handFlip and not buttonPressed:

        finger = detector.fingersUp(hands[0])
        finger[0] = 1 - finger[0]

        cx, cy = hands[0]["center"]

        lmList = hands[0]["lmList"]

        # pointer plan limiting
        xVal = int(np.interp(lmList[8][0], [width // 2, w], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal
        indexThickness = int(lmList[8][2] / 5) * -1
        # print("INDEX LIST: ",lmList[8])
        print("FINGER: ", finger)

        if cy <= gestureThreshold:  # if hand iske height pr hai toh
            # Gesture-1: left:
            if finger == [1, 0, 0, 0, 0]:
                annotStart = False
                print("left")
                if slideNumber > 0:
                    buttonPressed = True
                    annotNumber = 0
                    annotStart = False
                    annotations = [[]]
                    slideNumber -= 1

            # Gesture-2: right:
            if finger == [0, 0, 0, 0, 1]:
                annotStart = False
                print("right")
                if slideNumber < len(slidePath) - 1:
                    buttonPressed = True
                    annotNumber = 0
                    annotStart = False
                    annotations = [[]]
                    slideNumber += 1

        # Gesture-3: tracking_pointer:
        if finger == [0, 1, 1, 0, 0] or finger == [1, 1, 1, 0, 0]:
            cv2.circle(
                currentSlide, indexFinger, 5, (0, 0, 255), indexThickness, cv2.FILLED
            )
            annotStart = False

        # Gesture-4: tracking_pointer:
        if finger == [0, 1, 0, 0, 0] or finger == [1, 1, 0, 0, 0]:
            if annotStart is False:
                annotStart = True
                annotNumber += 1
                annotations.append([])
            cv2.circle(
                currentSlide, indexFinger, 5, (0, 0, 255), indexThickness, cv2.FILLED
            )
            annotations[annotNumber].append(indexFinger)
        else:
            annotStart = False

        # Gesture-4: tracking_pointer:
        if finger == [0, 1, 1, 1, 0] or finger == [1, 1, 1, 1, 0]:
            if annotations:
                if annotNumber > 0:
                    annotations.pop(-1)
                    annotNumber -= 1
                    buttonPressed = True
    else:
        annotStart = False

    # button press loop
    if buttonPressed:
        btnCount += 1
        if btnCount > btnDelay:
            btnCount = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(
                    currentSlide, annotations[i][j - 1], annotations[i][j], (0, 0, 0), 5
                )

    # adding wedcam on slide images
    camSmall = cv2.resize(img, (ws, hs))
    h, w, _ = currentSlide.shape
    currentSlide[0:hs, w - ws : w] = camSmall

    cv2.putText(
        img,
        "FPS:" + str(fps),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 0, 0),
        4,
        cv2.LINE_AA,
    )
    cv2.putText(
        img,
        "FPS:" + str(fps),
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    cv2.imshow("WEB CAM", img)
    cv2.imshow("Slides", currentSlide)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
