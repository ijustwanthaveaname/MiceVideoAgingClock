import os
import math
from collections import defaultdict

def txt(folder_path, save_folder):
    try:
        # 遍历指定文件夹及其所有子文件夹
        for root, dirs, files in os.walk(folder_path):
            # 获取当前子文件夹的相对路径
            relative_path = os.path.relpath(root, folder_path)
            
            # 构建保存路径: 在目标文件夹下创建相同的子文件夹
            save_subfolder = os.path.join(save_folder, relative_path)
            os.makedirs(save_subfolder, exist_ok=True)
            print("relative_path", relative_path)

            # 遍历当前子文件夹中的所有文件
            for filename in files:
                if filename.endswith('.txt'):
                    file_path = os.path.join(root, filename)
                    print(file_path)

                    all_coordinates = []
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            line = line.strip()
                            if line:
                                numbers = list(map(int, line.split(',')))
                                all_coordinates.append(numbers)

                    # 分组数据
                    all_coordinates_3m = []
                    all_coordinates_2m = []
                    all_coordinates_1m = []

                    frame_groups = defaultdict(list)

                    # 将数据按帧号分组
                    for data in all_coordinates:
                        frame_number = data[0]  # 假设 data[0] 是帧号
                        frame_groups[frame_number].append(data)

                    # 将帧数据分为三只、两只和一只老鼠
                    for frame_number, frame_data in frame_groups.items():
                        # 通过老鼠的 ID 来判断有多少只老鼠
                        num_mice = len(set(data[1] for data in frame_data))  # 假设 data[1] 是老鼠的 ID

                        # 根据老鼠的数量，分配到对应的列表
                        if num_mice == 3:
                            all_coordinates_3m.extend(frame_data)
                        elif num_mice == 2:
                            all_coordinates_2m.extend(frame_data)
                        elif num_mice == 1:
                            all_coordinates_1m.extend(frame_data)
                    print(len(all_coordinates_3m), len(all_coordinates_2m), len(all_coordinates_1m))

                    # 计算体长和体宽
                    calculate_body_size(all_coordinates_3m, all_coordinates_2m, all_coordinates_1m, save_subfolder, filename)

        print('完成')

    except FileNotFoundError:
        print("文件夹未找到，请检查路径。")
    except Exception as e:
        print(f"发生错误: {e}")

def calculate_body_size(all_coordinates_3m, all_coordinates_2m, all_coordinates_1m, save_subfolder, filename):
    # 选择具有最多帧数的集合
    max_frames = max(len(all_coordinates_3m) // 3, len(all_coordinates_2m) // 2, len(all_coordinates_1m))
    if max_frames == len(all_coordinates_3m) // 3:
        selected_coordinates = all_coordinates_3m
        num_mice = 3
    elif max_frames == len(all_coordinates_2m) // 2:
        selected_coordinates = all_coordinates_2m
        num_mice = 2
    else:
        selected_coordinates = all_coordinates_1m
        num_mice = 1

    # 计算体长和体宽
    body_sizes = []
    for i in range(0, len(selected_coordinates), num_mice):
        frame_data = selected_coordinates[i:i + num_mice]
        frame_number = frame_data[0][0]
        sizes = [frame_number]
        for data in frame_data:
            x1, y1, x2, y2 = data[2:6]
            length = abs(x2 - x1)
            width = abs(y2 - y1)
            sizes.append((length, width))
        body_sizes.append(sizes)

    # 输出到txt文件
    output_path = os.path.join(save_subfolder, f"{filename}_body_size.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        for sizes in body_sizes:
            line = ','.join(map(str, sizes))
            f.write(line + '\n')

if __name__ == '__main__':
    # 指定文件夹路径
    folder_path = r'/home/shanli/video_analysis/video_result_txt/ovary_456'  # 关键点文件夹
    save_folder = r'/home/shanli/video_analysis/changkuan/ovary_456'  # 输出文件夹

    txt(folder_path, save_folder)
    