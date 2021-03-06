# autoface project

cd autoface
export PYTHONPATH=./models/insightface/deploy/


# manage config.json
```json
{
  "exp_name": "autoface",
  "num_epochs": 10,
  "num_iter_per_epoch": 10,
  "learning_rate": 0.001,
  "batch_size": 16,
  "number_of_class": 256,
  "input_dim": 512,
  "max_to_keep":5,
  "checkpoint_dir":"./experiments/checkpoints/",
  "summary_dir": "./experiments/summary/",
  "do_preprocess":0,
  "do_train":0,
  "do_demo": 1,
  "pretrained_mode": {
    "image_size":"112,112",
    "ga_model":"",
    "model":"./models/insightface/models/model-r100-ii/model,0",
    "gpu":0,
    "det":0,
    "flip":0,
    "threshold":1.24
  }
}
```

# Run align
python3 utils/align_face.py

# Run generate embedding
python3 utils/generate_insightface_embedding.py


# Run train/eval/predict
python3 autoface.py

# Live
python3 utils/face_detect.py

export CUDA_VISIBLE_DEVICES="0"
python3 autoface.py

