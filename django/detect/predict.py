from mmaction.apis import inference_recognizer, init_recognizer

import sys
import os

root_path = "/var/www/app/"

if __name__ == "__main__":
    # default
    if len(sys.argv) >= 2:
        video_path = sys.argv[1]  # 指定视频路径，需要根据command传入的参数修改

    config_path = root_path + "utils/swin_tiny_patch244_window877_nystagmusdata_1k.py"

    checkpoint_path = root_path + "utils/best_top1_acc_epoch_142.pth"

    video_path = (
        root_path + "data/0000000000_005_0000000009_0000000001_01_02_R.avi"
    )  # 默认视频路径

    label_path = root_path + "tools/labels.txt"

    # 从配置文件和权重文件中构建模型
    model = init_recognizer(
        config_path, checkpoint_path, device="cuda:3"
    )  # device 可以是 'cuda:0'
    # 对单个视频进行测试
    result = inference_recognizer(model, video_path, label_path)
    print(result)

    max_result = max(result, key=lambda x: x[1])
    max_label = max_result[0]
    print("predict:", max_label)
