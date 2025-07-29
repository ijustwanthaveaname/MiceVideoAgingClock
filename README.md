# 🐭 YOLOv8 Mouse Tracking & Age Prediction

This repository provides a **complete pipeline** for:

- **Mouse detection & pose estimation** (YOLOv8)
- **Behavior analysis**
- **Body length/width measurement**
- **Biological age prediction** using three pre‑trained models:
  - **FrailtyAge**
  - **BehavAge**
  - **TSRAge**

It is designed for mouse aging intervention research, enabling high-throughput and rapid assessment of aging levels through video shooting.

---

## 📦 Installation

Create a Conda environment and install dependencies:

```bash
# Create and activate environment
conda create -n yolov8 python=3.8
conda activate yolov8

# Install PyTorch (CUDA 11.3)
conda install pytorch==1.12.1 torchvision==0.13.1 torchaudio==0.12.1 cudatoolkit=11.3 -c pytorch
# Install Sklearn
pip install scikit-learn
# Additional dependencies
pip install opencv-python==4.5.5.64
pip install PyYAML
pip install tqdm
pip install openpyxl
pip install collections
```
## 🚀 Training
Train a YOLOv8 pose model:
```bash
python train.py \
    --weights yolov8s-pose.pt \
    --cfg yolov8s-pose.yaml \
    --data coco8-pose.yaml \
    --epochs 200 \
    --imgsz 640 \
    --batch 8 \
    --workers 0 \
    --save_dir runs/train/exp2 \
    --device 0 \
    --verbose
```
## 🎯 Detection & Tracking
```bash
python detect.py \
    --video your_video.mp4 \
    --model weights/yolov8s.pt \
    --txt mouse_output.txt \
    --strong_sort_weights_path weights/osnet_x0_75_msmt17.pt \
    --device 0 \
    --cfg_path strong_sort/configs/strong_sort.yaml
```
This will generate:

mouse_output.txt: tracking results
## 📊 Behavior & Body Measurement
After detection, compute behavior metrics and body length/width.

please change input and output file in script manually.
```bash
python behavior.py
python body_length_width.py
```
## 🧠 Age prediction 
Please refer to the sample files of each type of clock for replacement.
**FrailtyAge**
```bash
python predict_age.py \
    --model FrailtyAge.joblib \
    --data FrailtyAge \
    --save_preds frailtyage_predictions.csv
```
**BehavAge**
```bash
python predict_age.py \
    --model Behav.joblib \
    --data BehavAge \
    --save_preds behaveage_predictions.csv
```
**TSRAge**
```bash
python predict_age.py \
    --model TSRAge.joblib \
    --data TSRAge \
    --save_preds tsrage_predictions.csv
```
