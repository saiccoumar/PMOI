#imports
from imutils.video import VideoStream
from imutils.video import FPS
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import os
import tensorflow as tf
from tensorflow.keras.models import load_model
from scipy.spatial import distance as dist

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
maskNet=load_model('masknet2.h5')
print("Loaded model")
face_model = cv2.CascadeClassifier('lbpcascade_frontalface_improved.xml')
labels_dict={0:'MASK',1:'NO MASK'}
res = 128
color_dict={0:(0,255,0),1:(0,0,255)}


current_directory = os.getcwd()
print(current_directory)
statDir = current_directory+'/static/'
templateDir = current_directory+'/templates/'
# initialize a flask object
app = Flask(__name__,static_folder=statDir,
            template_folder=templateDir)
# initialize the video stream and allow the camera sensor to
# warmup

vs = VideoStream(src=0).start()
time.sleep(2.0)




def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
    global vs
    global outputFrame
    global lock
    print("debugger")
    total = 0
    while(True):
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)
        # grab the current timestamp and draw it on the frame
        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame'
        faces=face_model.detectMultiScale(frame)
        if total > frameCount:
            for (x,y,w,h) in faces:
                face_img=frame[y:y+w,x:x+w]
                face_img=cv2.resize(face_img,(res,res))
                face_img=img_to_array(face_img)
                reshaped=np.reshape(face_img/255,[1,res,res,3])
                #print(reshaped)
                result=maskNet.predict(reshaped)
                label=0 if result[0][0]>0.8 else 1
      
                cv2.rectangle(frame,(x,y),(x+w,y+h),color_dict[label],2)
                cv2.rectangle(frame,(x,y-40),(x+w,y),color_dict[label],-1)
                cv2.putText(frame, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        #cv2.imshow('frame',frame)
        #print('lol' + str(total))
        total += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
	# acquire the lock, set the output frame, and release the
	# lock
        with lock:
            outputFrame = frame.copy()

        #cv2.imwrite('test/lol.png', outputFrame)
		
def generate():
	# grab global references to the output frame and lock variables
    global outputFrame, lock
	# loop over frames from the output stream
    while(True):
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
			# encode the frame in JPEG format
            flag, encodedImage = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
            if not flag:
                continue
		# yield the output frame in the byte format
        flag, encodedImage = cv2.imencode(".jpg", outputFrame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

# replace with our python model

@app.route("/video_feed")
def video_feed():
    print("video")
    return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


	# update the background model and increment the total number
		# of frames read thus far
		



# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--ip", type=str, required=True,
	# 	help="ip address of the device")
	# ap.add_argument("-o", "--port", type=int, required=True,
	# 	help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	# start the flask app
	app.run(port=8000, debug=True,
		threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()


# run to start the webstreaming on port 8000
# $ python webstreaming.py --port 8000