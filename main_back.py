import os
import glob
import time
from gpiozero import DigitalInputDevice
from time import sleep
import time
from gpiozero import Button
from gtts import gTTS
import pygame
from imutils.video import VideoStream
import cv2
import numpy as np

pygame.mixer.init()

pygame.mixer.music.set_volume(1)

ldr_pin = 21
temp_button_pin = 1
ldr_button_pin = 7
object_pin = 8

temp_button = Button(temp_button_pin)
ldr_button = Button(ldr_button_pin)
object_button = Button(object_pin)

ldr = DigitalInputDevice(pin = ldr_pin)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


args = {"confidence":0.5, "threshold":0.3}
labelsPath = "./yolo-coco/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")
weightsPath = os.path.abspath("./yolo-coco/yolov3-tiny.weights")
configPath = os.path.abspath("./yolo-coco/yolov3-tiny.cfg")

net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def tts(content):
     myobj = gTTS(text=content, lang='en', slow=False)
     myobj.save("read.mp3")
     pygame.mixer.music.load("read.mp3")
     pygame.mixer.music.play()

def read_ir(ldr):
    return ldr.is_active

def temp():
    temperature_celsius, temperature_fahrenheit = read_temp()
    print(f'Temperature: {temperature_celsius:.2f} °C')
    tts(f'Temperature is {temperature_celsius:.2f} °C')
    # print(f'Temperature: {temperature_fahrenheit:.2f} °F')

def recognize_object():
    detected = False
    vs = cv2.VideoCapture(0)
    vs.set(cv2.CAP_PROP_FRAME_WIDTH,320)
    vs.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
    (W, H) = (None, None)

    while True:
        (grabbed, frame) = vs.read()
        if not grabbed:
            break
        
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (320, 320),
            swapRB=True, crop=False)
        net.setInput(blob)
        layerOutputs = net.forward(ln)
        
        boxes = []
        confidences = []
        classIDs = []

        
        for output in layerOutputs:
            
            for detection in output:
                
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if confidence > args["confidence"]:
                    
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
            args["threshold"])

        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])
                color = [int(c) for c in COLORS[classIDs[i]]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                obj_name = "{}".format(LABELS[classIDs[i]])
                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                    confidences[i])
                cv2.putText(frame, text, (x, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                

                print("Detected object: ",text)
                tts(obj_name+" Detected")
                time.sleep(1)
                detected = True
        
        cv2.imshow("Output", frame)
        
        if object_button.is_pressed:
            tts("exiting")
            time.sleep(3)
            break

        if cv2.waitKey(1) == ord('q'):
            break
        
    cv2.destroyAllWindows()
    vs.release()

def ldr_status():
    val = read_ir(ldr)
    if val:
        print("Night")
        status = "Night"
        tts("Its Night")
    else:
        print("Day")
        status = "Day"
        tts("its Day")
def main():
    tts("System initialized")
    while True:
        if temp_button.is_pressed:
            print("temp Please wait")
            temp()
        elif ldr_button.is_pressed:
            print("LDR button")
            ldr_status()

        elif object_button.is_pressed:
            print("Object detection button pressed. Please wait")
            tts("Object detection button pressed. Please wait")
            recognize_object()
        sleep(0.2)
    
main()