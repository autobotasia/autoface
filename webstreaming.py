# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from imutils.video import VideoStream
from flask import Flask, Response, make_response
from flask import render_template
from utils.insightface_utils import InsightfaceUtils
from bunch import Bunch
from utils.config import process_config
from utils.utils import get_args
from trainer import Trainer
import threading
import argparse
import datetime
import imutils
import time
import cv2
import sys

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
staffClsName = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(src="rtsp://admin:12345678a@@172.16.110.2:554/Streamming/channels/101").start()
vs = VideoStream(src=0).start()
time.sleep(2.0)

sys.path.append('./models/insightface/deploy/')
args = get_args()
config = process_config(args.config)
util = InsightfaceUtils(Bunch(config.pretrained_model))
trainer = Trainer(config)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, staffClsName, lock

	# initialize the motion detector and the total number of frames
	# read thus far	
	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		try:
			predictimg, points = util.get_embedding(frame)
			predictimg = predictimg.reshape(1, 512)
			for best_idx, clsname, prob, result_top3 in trainer.predict(predictimg, batch_size=1):
				#face = {'point': points[0], 'name': clsname}
				staffClsName = "%s - %f"%(clsname,prob)

				print("=====%s: %f=====" % (clsname, prob))
				#if os.path.exists('./data/cls/%s'%clsname) == False:
				#    os.makedirs('./data/cls/%s'%clsname)
				
			# save prediction to database
			#if max_prob > 0.7 and datetime.now() > next_time_can_save_img:
			#    db.save_and_noti(frame, face['name'], max_prob, saved_day)
		
		except Exception as e:
			print("ignore this frame", e)
		total += 1

		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()
			cv2.putText(outputFrame, staffClsName, (50, 50),
							cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                            thickness=1, lineType=2)
		
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)			

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
#if __name__ == '__main__':
# construct the argument parser and parse command line arguments
'''ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, required=True,
	help="ip address of the device")
ap.add_argument("-o", "--port", type=int, required=True,
	help="ephemeral port number of the server (1024 to 65535)")
ap.add_argument("-f", "--frame-count", type=int, default=32,
	help="# of frames used to construct the background model")
args = vars(ap.parse_args())'''

# start a thread that will perform motion detection
t = threading.Thread(target=detect_motion, args=(
	20,))
	#args["frame_count"],))
t.daemon = True
t.start()

# start the flask app
app.run(host="0.0.0.0", port="6006", debug=True,
	threaded=True, use_reloader=False)

# release the video stream pointer
#vs.stop()