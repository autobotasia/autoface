from flask import Flask, request, jsonify
import base64
import numpy as np
import cv2
import io
from PIL import Image
import re
from utils.insightface_utils import InsightfaceUtils
from bunch import Bunch
from utils.config import process_config
from utils.utils import get_args
from trainer import Trainer
import sys
import imutils

app = Flask(__name__)

sys.path.append('./models/insightface/deploy/')
args = get_args()
config = process_config(args.config)
util = InsightfaceUtils(Bunch(config.pretrained_model))
trainer = Trainer(config)

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    #data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, '', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += '='* (4 - missing_padding)
    return base64.b64decode(data)

@app.route('/face', methods=['POST']) 
def face():
    ret = []
    data = request.json
    for b64img in data["data"]:
        base64_data = re.sub('^data:image/.+;base64,', '', b64img["data"])
        decoded_data = base64.b64decode(base64_data)
        np_data = np.fromstring(decoded_data,np.uint8)
        img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)
        #img = imutils.resize(img, width=400)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        predictimg, _ = util.get_embedding(img)
        predictimg = predictimg.reshape(1, 512)
        for _, clsname, prob, _ in trainer.predict(predictimg, batch_size=1):
            ret.append({'cls': clsname, 'prob': '%f'%prob})
            print("=====%s: %f=====" % (clsname, prob))
        
    
    return jsonify(ret)