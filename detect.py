from ultralytics import YOLO
import cv2
import numpy as np
import os
from ocsort_tracker.ocsort import OCSort
import torch
import argparse

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
def track(video_path, model_path, txt_path):
    tracker = OCSort(
        det_thresh=0,
        max_age=10000,
        min_hits=1,
        iou_threshold=0.22136877277096445,
        delta_t=1,
        asso_func="giou",
        inertia=0.3941737016672115,
        use_byte=False,
    )
    outputs_track = [None, None, None]

    model = YOLO(model_path, task='pose')  # load an official model

    cap = cv2.VideoCapture(video_path)
    count = 0

    while True:
        # 从摄像头读取帧
        ret, frame = cap.read()

        # 检查帧读取是否成功
        if not ret:
            print("无法读取摄像头帧")
            break
        results = model.predict(frame, conf=0.6, device="0", verbose=False)

        # 准备跟踪器输入
        jieguo = []
        for i, box in enumerate(results[0]):
            box_conf = round(box.boxes.conf.item(), 4)
            box_xyxy = box.boxes.xyxy[0].tolist()
            jieguo.append([box_xyxy[0], box_xyxy[1], box_xyxy[2], box_xyxy[3], box_conf, i])

        conf = results[0].boxes.conf.cpu()
        clss = results[0].boxes.cls.cpu()
        keypoints = results[0].keypoints.data.tolist()
        xywh = xyxy_to_xywh(results[0].boxes.xyxy.cpu())
        nose = np.array(keypoints)[:, 0:1]
        right = np.array(keypoints)[:, 1:2]
        left = np.array(keypoints)[:, 2:3]
        bozi = np.array(keypoints)[:, 3:4]
        center = np.array(keypoints)[:, 4:5]
        tail = np.array(keypoints)[:, 5:6]
        outputs_track = tracker.update(jieguo)
        xytl = xywh_to_tlwh(xywh.cpu()).cpu().numpy().tolist()
        # 将边界框从 (top-left x, top-left y, width, height) 格式转换为 (top-left x, top-left y, bottom-right x, bottom-right y) 格式
        xyxy = xywh_to_xyxy(xytl)
        # 初始化鼠标数据列表
        mouse_1 = []
        mouse_2 = []
        mouse_3 = []

        for ii, output_track in enumerate(outputs_track):
            bboxes = output_track[0:4]
            id = int(output_track[4])
            
            # 初始化关键点坐标
            nose_txt_x, nose_txt_y = None, None
            left_txt_x, left_txt_y = None, None
            right_txt_x, right_txt_y = None, None
            bozi_txt_x, bozi_txt_y = None, None
            center_txt_x, center_txt_y = None, None
            tail_txt_x, tail_txt_y = None, None

            # 找到每一帧中每个框对应的6个关键点
            for jjj in range(len(xyxy)):
                if (int(xyxy[jjj][0]) == int(output_track[0]) or abs(
                        int(xyxy[jjj][0]) - int(output_track[0])) <= 2) and (
                        int(xyxy[jjj][1]) == int(output_track[1]) or abs(
                    int(xyxy[jjj][1]) - int(output_track[1])) <= 2) and (
                        int(xyxy[jjj][2]) == int(output_track[2]) or abs(
                    int(xyxy[jjj][2]) - int(output_track[2])) <= 2) and (
                        int(xyxy[jjj][3]) == int(output_track[3]) or abs(
                    int(xyxy[jjj][3]) - int(output_track[3])) == 1):

                    # 提取关键点坐标
                    nose_txt_x = int(nose[jjj][0][0])
                    nose_txt_y = int(nose[jjj][0][1])
                    left_txt_x = int(left[jjj][0][0])
                    left_txt_y = int(left[jjj][0][1])
                    right_txt_x = int(right[jjj][0][0])
                    right_txt_y = int(right[jjj][0][1])
                    bozi_txt_x = int(bozi[jjj][0][0])
                    bozi_txt_y = int(bozi[jjj][0][1])
                    center_txt_x = int(center[jjj][0][0])
                    center_txt_y = int(center[jjj][0][1])
                    tail_txt_x = int(tail[jjj][0][0])
                    tail_txt_y = int(tail[jjj][0][1])

            # 处理数据并存储到相应的列表
            if id == 1:
                mouse_one = [bboxes[0], bboxes[1], bboxes[2], bboxes[3], nose_txt_x, nose_txt_y,
                                left_txt_x, left_txt_y, right_txt_x, right_txt_y,
                                bozi_txt_x, bozi_txt_y, center_txt_x, center_txt_y,
                                tail_txt_x, tail_txt_y]
                mouse_1.append(mouse_one)
                valid_length_1 = len([value for value in mouse_1[0] if value is not None])            
                if len(mouse_1) > 3:
                    mouse_1 = mouse_1[-2:]
                if valid_length_1 > 4:
                    last_mouse1 = mouse_1  
                else:

                    mouse_1 = last_mouse1
            elif id == 2:
                mouse_two = [bboxes[0], bboxes[1], bboxes[2], bboxes[3], nose_txt_x, nose_txt_y,
                                left_txt_x, left_txt_y, right_txt_x, right_txt_y,
                                bozi_txt_x, bozi_txt_y, center_txt_x, center_txt_y,
                                tail_txt_x, tail_txt_y]
                mouse_2.append(mouse_two)
                valid_length_2 = len([value for value in mouse_2[0] if value is not None])
                if len(mouse_2) > 3:
                    mouse_2 = mouse_2[-2:]
                if valid_length_2 > 4:
                    last_mouse2 = mouse_2 
                else:
                    mouse_2 = last_mouse2
            elif id == 3:
                mouse_three = [bboxes[0], bboxes[1], bboxes[2], bboxes[3], nose_txt_x, nose_txt_y, left_txt_x, left_txt_y, right_txt_x, right_txt_y, bozi_txt_x, bozi_txt_y, center_txt_x, center_txt_y, tail_txt_x, tail_txt_y]
                mouse_3.append(mouse_three)
                valid_length_3 = len([value for value in mouse_3[0] if value is not None])
                if len(mouse_3) > 3:
                    mouse_3 = mouse_3[-2:]
                if valid_length_3 > 4:
                    last_mouse3 = mouse_3 
                else:  
                    mouse_3 = last_mouse3
                   
        with open(txt_path, 'a', encoding='utf-8') as f:
            data1 = ','.join([str(count + 1 ), '1'] + [str(int(x)) for x in mouse_1[0]])
            data2 = ','.join([str(count + 1), '2'] + [str(int(x)) for x in mouse_2[0]])
            data3 = ','.join([str(count + 1), '3'] + [str(int(x)) for x in mouse_3[0]])
            f.write(f'{data1}\n')
            f.write(f'{data2}\n')
            f.write(f'{data3}\n')
        count += 1

    # 释放摄像头、关闭输出视频和关闭窗口
    cap.release()
    cv2.destroyAllWindows()


def xywh_to_tlwh(bbox_xywh):
    if isinstance(bbox_xywh, np.ndarray):
        bbox_tlwh = bbox_xywh.copy()
    elif isinstance(bbox_xywh, torch.Tensor):
        bbox_tlwh = bbox_xywh.clone()
    bbox_tlwh[:, 0] = bbox_xywh[:, 0] - bbox_xywh[:, 2] / 2.
    bbox_tlwh[:, 1] = bbox_xywh[:, 1] - bbox_xywh[:, 3] / 2.
    return bbox_tlwh

def xywh_to_xyxy(xytl):
    result = []
    for bbox in xytl:
        x, y, w, h = bbox
        bottom_right_x = x + w
        bottom_right_y = y + h
        # 将左上角和右下角坐标组合成新的列表
        result.append([int(x), int(y), int(bottom_right_x), int(bottom_right_y)])
    return result

def xyxy_to_xywh(bbox_xyxy):
    """
    支持 torch.Tensor 或 np.ndarray，输入为(N,4)[x1, y1, x2, y2]，输出为(N,4)[xc, yc, w, h]
    """
    if isinstance(bbox_xyxy, torch.Tensor):
        x1, y1, x2, y2 = bbox_xyxy[:, 0], bbox_xyxy[:, 1], bbox_xyxy[:, 2], bbox_xyxy[:, 3]
        w = x2 - x1
        h = y2 - y1
        xc = x1 + w / 2
        yc = y1 + h / 2
        return torch.stack([xc, yc, w, h], dim=1)
    else:
        bbox_xyxy = np.array(bbox_xyxy)
        x1, y1, x2, y2 = bbox_xyxy[:, 0], bbox_xyxy[:, 1], bbox_xyxy[:, 2], bbox_xyxy[:, 3]
        w = x2 - x1
        h = y2 - y1
        xc = x1 + w / 2
        yc = y1 + h / 2
        return np.stack([xc, yc, w, h], axis=1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', type=str, default='', help='视频文件路径')
    parser.add_argument('--model', type=str, default='weights\yolov8s.pt', help='模型文件路径')
    parser.add_argument('--txt', type=str, default='mouse_output.txt', help='保存txt文件路径')
    args = parser.parse_args()
    track(args.video, args.model, args.txt)
