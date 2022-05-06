from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from proctor.camera import VideoCamera

import cv2
import mediapipe
import matplotlib.pyplot as plt
from datetime import datetime
import os

mp_face_detection = mediapipe.solutions.face_detection
mp_drawing = mediapipe.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5)
# Create your views here.
def index(request):
    return render(request, 'proctor/index.html')

def gen(camera):
    count = 0
    while True:
        frame,org_frame = camera.get_frame()
        # print(org_frame.shape)
        flag,org_frame, count = get_results(org_frame, count)
        if flag == True:
            print("WOOOOOOO FASSA ",flag)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')


def get_result(image, count):
    violate = False
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detection.process(image)

    now = datetime.now()
    curr_time = now.strftime("%H_%M_%S")

    if  type(results.detections) == type(None) or len(results.detections) != 1:
        if count > 10:
            print("screen shot saved ",curr_time)
            # cv2.imwrite("final_year_project/ss/ss_"+str(curr_time)+".jpg",img)
            violate = True
            count = 0
        count += 1

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)
    return image, violate, count


def get_results(frame, count):
    frame, violate, count = get_result(frame, count=count)
    return violate, frame, count