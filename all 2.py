from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
from ultralytics import YOLO
import cvzone
import math
import time
from sort import *
# cap = cv2.VideoCapture()
model = YOLO('../Yolo-Weights/yolov8n.pt')
classNames =["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                      "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                      "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                      "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                      "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                      "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                      "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                      "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                      "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                      "teddy bear", "hair drier", "toothbrush"
                      ]
tracker = Sort(max_age=20,min_hits=3,iou_threshold=0.3)
limits= [5005,80,800,160]
# def set_value (img):
#
#
#
#        success, img = cap.read()
#        results = model(img, stream=True)
#        for r in results:
#            boxes = r.boxes
#            for box in boxes:
#                x1,y1,x2,y2 =box.xyxy[0]
#                x1,y1,x2,y2 =int(x1),int(y1),int(x2),int(y2)
#                img = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                print(x1,y1,x2,y2)
#            return img
def videovisualizer():
        global cap
        ret, frame = cap.read()
        # model=YOLO("../yolo-weights/yolov8n.pt")
        # result = model(frame ,stream=True)
        detection =np.empty((0,5))
        if ret == True:
            frame = imutils.resize(frame, width=640)
            # img=set_value(img=1)
            success, frame = cap.read()
            results = model(frame, stream=True)
            for r in results:
               boxes = r.boxes
            for box in boxes:
               x1,y1,x2,y2=box.xyxy[0]
               x1,y1,x2,y2 =int(x1),int(y1),int(x2),int(y2)
               w,h =x2-x1,y2-y1
               # bbox =int(x1),int(y1),int(w),int(h)

               # frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
               # cvzone.cornerRect(frame,(x1,y1,w,h), rt=5)
               conf=math.ceil((box.conf[0]*100))/100
               #confidence

               #class name get
               cls= int(box.cls[0])
               cuurntclassGet =classNames[cls]
               if cuurntclassGet=="person" and conf>0.3:

                   # cvzone.putTextRect(frame,f'{classNames[cls]}{conf}',(max(0,x1),max(20,y1)),scale=1,thickness=2)
                   currentarray =np.array([x1,y1,x2,y2,conf])
                   detection=np.vstack((detection,currentarray))




               print(conf)
               print(x1,y1,w,h)

            resulttraker=tracker.update(detection)
            cv2.rectangle(frame, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)
            for result in resulttraker:
                x1,y1,x2,y2,id=result
                x1,y1,x2,y2 =int(x1),int(y1),int(x2),int(y2)
                print(result)
                w,h =x2-x1,y2-y1

                cvzone.cornerRect(frame,(x1,y1,w,h), rt=5,colorR=(0,255,0))

                cvzone.putTextRect(frame,f'{classNames[cls]}{conf}',(max(0,x1),max(20,y1)),scale=1,thickness=2)
                cx,cy =x1+w//2,y1+h//2
                cv2.circle(frame,(cx,cy),4,(255,0,0))
                def detection():

                    if limits[0]<cx<limits[2]:
                           cvzone.putTextRect(frame,f'{"Human Detected "}',(max(0,x1),max(20,y1)),scale=1,thickness=2)
                           return "Human Detected"


                def updateResult():
                    res =detection()
                    if res=="Human Detected":
                        l4.config(bg="red")
                        print("red")
                    else:
                         l4.config(bg="green")
                         print("red")
                updateResult()


                print(detection())






            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)



            lblvideo.configure(image=img)
            lblvideo.image = img
            lblvideo.after(10, videovisualizer)
        else:
            lblvideo.image = ""
            lblvideopath.configure(text="")
            rad1.configure(state="active")
            rad2.configure(state="active")
            selected.set(0)
            btnEnd.configure(state="disabled")
            cap.release()

def ckeck_detection():
    global cap
    global img
    if selected.get() == 1:
        path_video = filedialog.askopenfilename(filetypes = [
            ("all video format", ".mp4"),
            ("all video format", ".avi")])
        if len(path_video) > 0:
            btnEnd.configure(state="active")
            rad1.configure(state="disabled")
            rad2.configure(state="disabled")

            pathInputVideo = "..." + path_video[-20:]
            lblvideopath.configure(text=pathInputVideo)
            cap = cv2.VideoCapture(path_video)
            videovisualizer()
    if selected.get() == 2:
        btnEnd.configure(state="active")
        rad1.configure(state="disabled")
        rad2.configure(state="disabled")
        lblvideopath.configure(text="")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        videovisualizer()

def end():
    lblvideo.image=""
    lblvideopath.config(text="")
    rad1.config(state="active")
    rad2.config(state="active")
    selected.set(0)
    cap.release(0)
cap = None
root= Tk()
lblinfo1 =Label(text="Verse Analyze-Human detection" ,font="bold")
lblinfo1.grid(column=0,row=0, columnspan=3)

selected = IntVar()
rad1 =Radiobutton(root,text= "OPEN THE VIDEO", width=20,value=1,variable=selected,command=ckeck_detection)
rad1.grid(column=0,row=1)

rad2 =Radiobutton(root,text= "OPEN THE CAMERA VIDEO", width=20,value=2,variable=selected,command=ckeck_detection)
rad2.grid(column=1,row=1)

lblvideopath=Label(root,text="",width=20)
lblvideopath.grid(column=0,row=2)
lblvideo = Label(root)
lblvideo.grid(column=3,row=0,rowspan=9)

btnEnd =  Button(root,text="Stop Detection",state="disable",command=end)
btnEnd.grid(column=0,row=9,columnspan=2, pady=10)

l1=Label(root,text="Setup Y value here",pady=5,font=8)
l1.grid(column=0,row=4)

Text1 =Entry(root,width=20)
Text1.grid(column=1,row=4)

l2=Label(root,text="Setup x value here",font=8)
l2.grid(column=0,row=5,pady=5)
Text =Entry(root,width=20)
Text.grid(column=1,row=5,pady=5)

l3=Label(root,text="Setup W value here",font=8)
l3.grid(column=0,row=6,pady=5)
Text3 =Entry(root,width=20)
Text3.grid(column=1,row=6,pady=5)

l4=Label(root,text="Setup H value here",pady=5,font=8)
l4.grid(column=0,row=7,pady=5)
Text4 =Entry(root,width=20)
Text4.grid(column=1,row=7,pady=5)



root.mainloop()


#
# # Create a tkinter window
# window = tk.Tk()
# window.title("YOLOv3 Human Detection")
#
# # Create a label for displaying video feed
# video_label = tk.Label(window)
# video_label.pack()
#
# cap = cv2.VideoCapture(0)
#
# model = YOLO('../Yolo-Weights/yolov8n.pt')
# def detect_human(frame):
#     while True:
#         success, img =cap.read()
#         results= model(img,stream=True)
#         # cv2.imshow("image",img)
#         # cv2.waitKey(1)
#         frame = detect_human(frame)
#         cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         img = Image.fromarray(cv2image)
#         results = ImageTk.PhotoImage(image=img)
#         video_label.imgtk = results
#         video_label.config(image=results)
#
#         # Update the status label
#         # status_label.config(text="Status: Some custom detection status here")
#
#         video_label.after(1, detect_human())
#
# # detect_human()
# window.mainloop()
