import argparse
import os
import time

import cv2
import tensorflow.compat.v1 as tf
from numpy import *
import numpy as np
import dlib
import os
import re
from PIL import Image
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import shutil

from utils.config import config
from utils.logger import Logger
from models.models import Simple, NASNET, Inception, GAP, YOLO
from utils.utils import annotator, change_channel, gray_normalizer

import importlib, sys

importlib.reload(sys)

np.set_printoptions(suppress=True)  # 设置numpy数据不以科学计数法输出
tf.disable_v2_behavior()
tf.reset_default_graph()
# 根目录
root_path = "/var/www/app/"


# 1.视频逐帧裁剪，得到眼部区域存为图片
def eye_segmentation(Nystagmus_file):
    file_name = os.path.splitext(Nystagmus_file)[0]
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(
        root_path + "utils/shape_predictor_68_face_landmarks.dat"
    )

    cap = cv2.VideoCapture(root_path + "data/" + Nystagmus_file)
    if cap.isOpened() == False:
        print("Error opening video stream or file")

    os.makedirs(root_path + "frame_roi_left/" + file_name)
    os.makedirs(root_path + "frame_roi_right/" + file_name)
    i, n, flag = 0, 1, 1
    # cv2读取视频
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break

        # img = cv2.imread(img)
        if frame is None:
            print("frame is NULL!")
        else:
            img_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            # 人脸数rects
            rects = detector(img_gray, 0)
            # print(len(rects))
            for j in range(len(rects)):
                # 68点的集合
                landmarks = np.matrix(
                    [[p.x, p.y] for p in predictor(frame, rects[j]).parts()]
                )
                point = np.array(landmarks)

            if n % flag == 0:
                i = i + 1
                # print(i)
                print("frame" + str(i))
            # 右眼ROI区域
            left1_x = point[17][0]
            left1_y = point[17][1]
            right1_x = point[21][0]
            right1_y = point[28][1]

            # 把眼睛区域裁剪出来
            right_eye_cut = frame[left1_y:right1_y, left1_x:right1_x]
            right_roi = cv2.resize(
                right_eye_cut, (200, 108), interpolation=cv2.INTER_CUBIC
            )
            cv2.imwrite(
                root_path + "frame_roi_right/" + file_name + "/frame{}.jpg".format(i),
                right_roi,
            )

            # 左眼ROI区域
            left2_x = point[22][0]
            left2_y = point[22][1]
            right2_x = point[26][0]
            right2_y = point[28][1]

            # # 把眼睛区域裁剪出来
            left_eye_cut = frame[left2_y:right2_y, left2_x:right2_x]
            left_roi = cv2.resize(
                left_eye_cut, (200, 108), interpolation=cv2.INTER_CUBIC
            )
            cv2.imwrite(
                root_path + "frame_roi_left/" + file_name + "/frame{}.jpg".format(i),
                left_roi,
            )

            n = n + 1
            cv2.waitKey(1)

    cap.release()


# 2.帧合成视频
def frame2video(im_dir, video_dir, fps):
    im_list = os.listdir(im_dir)
    im_list.sort(key=lambda x: int(x.replace("frame", "").split(".")[0]))  # 最好再看看图片顺序对不
    img = Image.open(os.path.join(im_dir, im_list[0]))
    img_size = img.size  # 获得图片分辨率，im_dir文件夹下的图片分辨率需要一致
    # fourcc = cv2.cv.CV_FOURCC('M','J','P','G') #opencv版本是2
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # opencv版本是3
    videoWriter = cv2.VideoWriter(video_dir, fourcc, fps, img_size)
    # count = 1
    for i in im_list:
        im_name = os.path.join(im_dir + i)
        frame = cv2.imdecode(np.fromfile(im_name, dtype=np.uint8), -1)
        videoWriter.write(frame)
        # count+=1
        # if (count == 200):
        #     print(im_name)
        #     break
    videoWriter.release()
    print("finish")


def frametovideo(Nystagmus_file):
    file_name = os.path.splitext(Nystagmus_file)[0]
    im_dir1 = root_path + "frame_roi_left/" + file_name + "/"  # 帧存放路径
    video_dir1 = root_path + "data/" + file_name + "_left.mp4"  # 合成视频存放的路径
    im_dir2 = root_path + "frame_roi_right/" + file_name + "/"  # 帧存放路径
    video_dir2 = root_path + "data/" + file_name + "_right.mp4"  # 合成视频存放的路径
    fps = 30  # 帧率，每秒钟帧数越多，所显示的动作就会越流畅
    frame2video(im_dir1, video_dir1, fps)
    frame2video(im_dir2, video_dir2, fps)

    # 删除文件夹
    try:
        shutil.rmtree(im_dir1)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    try:
        shutil.rmtree(im_dir2)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


# 3.瞳孔追踪
def fit_rotated_ellipse_ransac(data, iter=50, sample_num=10, offset=80.0):
    # 拟合旋转椭圆中的随机抽样算法
    count_max = 0
    effective_sample = None

    for i in range(iter):
        sample = np.random.choice(len(data), sample_num, replace=False)

        xs = data[sample][:, 0].reshape(-1, 1)
        ys = data[sample][:, 1].reshape(-1, 1)

        J = np.mat(
            np.hstack((xs * ys, ys**2, xs, ys, np.ones_like(xs, dtype=np.float)))
        )
        Y = np.mat(-1 * xs**2)
        P = (J.T * J).I * J.T * Y

        # fitter a*x**2 + b*x*y + c*y**2 + d*x + e*y + f = 0
        a = 1.0
        b = P[0, 0]
        c = P[1, 0]
        d = P[2, 0]
        e = P[3, 0]
        f = P[4, 0]
        ellipse_model = (
            lambda x, y: a * x**2 + b * x * y + c * y**2 + d * x + e * y + f
        )

        # threshold
        ran_sample = np.array(
            [[x, y] for (x, y) in data if np.abs(ellipse_model(x, y)) < offset]
        )

        if len(ran_sample) > count_max:
            count_max = len(ran_sample)
            effective_sample = ran_sample

    return fit_rotated_ellipse(effective_sample)


def fit_rotated_ellipse(data):
    # 拟合旋转椭圆
    xs = data[:, 0].reshape(-1, 1)
    ys = data[:, 1].reshape(-1, 1)

    J = np.mat(np.hstack((xs * ys, ys**2, xs, ys, np.ones_like(xs, dtype=np.float))))
    Y = np.mat(-1 * xs**2)
    P = (J.T * J).I * J.T * Y

    a = 1.0
    b = P[0, 0]
    c = P[1, 0]
    d = P[2, 0]
    e = P[3, 0]
    f = P[4, 0]
    theta = 0.5 * np.arctan(b / (a - c))

    cx = (2 * c * d - b * e) / (b**2 - 4 * a * c)
    cy = (2 * a * e - b * d) / (b**2 - 4 * a * c)

    cu = a * cx**2 + b * cx * cy + c * cy**2 - f
    w = np.sqrt(
        cu
        / (
            a * np.cos(theta) ** 2
            + b * np.cos(theta) * np.sin(theta)
            + c * np.sin(theta) ** 2
        )
    )
    h = np.sqrt(
        cu
        / (
            a * np.sin(theta) ** 2
            - b * np.cos(theta) * np.sin(theta)
            + c * np.cos(theta) ** 2
        )
    )

    ellipse_model = lambda x, y: a * x**2 + b * x * y + c * y**2 + d * x + e * y + f

    error_sum = np.sum([ellipse_model(x, y) for x, y in data])
    print("fitting error = %.3f" % (error_sum))

    return (cx, cy, w, h, theta)


def pupil_track(file_name):
    # 创建一个VideoCapture对象并从输入文件中读取
    # 如果输入是摄像头，则输入0而不是文件名
    cap = cv2.VideoCapture(root_path + "data/" + file_name + ".mp4")
    # 检查视频是否读取成功
    if cap.isOpened() == False:
        print("Error opening video stream or file")
    total = 0
    j = 0
    # 一直读视频直到读完
    xcoordinates = []
    ycoordinates = []
    while cap.isOpened():
        # 逐帧捕捉
        # ret的值为True或False，代表有没有读到图片。frame是当前截取一帧的图片
        ret, frame = cap.read()

        if ret == False:
            j = j + 1
            print(str(j) + ":frame could be NULL")
            break
        j = j + 1
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  # 构造3*3卷积核
        # frame=frame.astype(np.float32)
        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将BGR格式转换成灰度图片
        # image_gray = frame #如果本来就是灰度图片
        blur = cv2.GaussianBlur(
            image_gray, (3, 3), 0
        )  # 高斯滤波。（3,3）是高斯内核大小（width和height）
        ret, thresh1 = cv2.threshold(
            blur, 50, 255, cv2.THRESH_BINARY
        )  # 二值化处理。cv2.threshold (源图片, 阈值, 填充色, 阈值类型)
        opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)  # 开运算：先进行腐蚀，再进行膨胀操作
        closing = cv2.morphologyEx(
            opening, cv2.MORPH_CLOSE, kernel
        )  # 闭运算：先进行膨胀操作，再进行腐蚀操作

        image = 255 - closing  # 灰度值逆转

        # 轮廓检测。contours:一个列表，每一项都是一个轮廓。
        # 每个轮廓contours[i]对应4个元素:hierarchy[i][0] ~hierarchy[i][3]，分别表示后一个轮廓、前一个轮廓、父轮廓、内嵌轮廓的索引编号
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        hull = []
        # print(str(j)+':contours为'+str(len(contours)))
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))  # 计算contours[i]的凸包

        #   cnt = sorted(hull, key=cv2.contourArea)
        #   maxcnt = cnt[-1]
        for con in hull:
            approx = cv2.approxPolyDP(
                con, 0.01 * cv2.arcLength(con, True), True
            )  # 轮廓近似
            area = cv2.contourArea(con)  # 计算轮廓面积
            if len(approx) > 10 and area > 1000:
                cx, cy, w, h, theta = fit_rotated_ellipse_ransac(
                    con.reshape(-1, 2)
                )  # 拟合旋转椭圆
                xcoordinates.append(cx)
                ycoordinates.append(cy)
                # cv2.ellipse(frame,(int(cx),int(cy)),(int(w),int(h)),theta*180.0/np.pi,0.0,360.0,(0,0,255),1) #绘制椭圆（瞳孔位置）
                # cv2.drawMarker(frame, (int(cx),int(cy)),(0, 0, 255),cv2.MARKER_CROSS,2,1) #画点（标记像素点）
                # cv2.imshow('Output',frame) #显示图像
                total = total + 1
                print(total)

                #   result.write(frame)
            # 按Q退出

            if cv2.waitKey(25) & 0xFF == ord("q"):
                break

    plt.figure(figsize=(19.2, 10.8))
    # 创建小图1
    ##将小图分成2行1列,第三个参数表示第n个图
    plt.subplot(2, 1, 1)
    plt.xlabel("Samples")
    plt.ylabel("Pupil Position(Pixels)")
    plt.title("X")
    plt.plot(xcoordinates[:])
    print("xcoordinates:", xcoordinates)
    # np.savetxt('result/data/'+file_name+'_x.txt', xcoordinates)

    # 创建小图2
    # 第三个参数表示是第2个图
    plt.subplot(2, 1, 2)
    plt.xlabel("Samples")
    plt.ylabel("Pupil Position(Pixels)")
    plt.title("Y")
    plt.plot(ycoordinates[:])
    print("ycoordinates:", ycoordinates)
    # np.savetxt('result/data/'+file_name+'_y.txt', ycoordinates)

    # 通过subplots_adjust()设置间距配置
    plt.subplots_adjust(
        left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.3
    )
    plt.savefig(root_path + "result/plot" + file_name + ".png")
    print("save:plot" + file_name + ".png")
    # plt.show()

    # 完成所有操作后，释放视频播放对象
    cap.release()
    # result.release()
    # 关闭所有窗口
    cv2.destroyAllWindows()


# 3-new.瞳孔追踪
def load_model(session, m_type, m_name, logger):
    best_dir = "best_loss"

    model_path = root_path + "models/" + m_name
    path = os.path.join(model_path, best_dir)
    if not os.path.exists(path):
        raise FileNotFoundError

    if m_type == "simple":
        model = Simple(m_name, config, logger)
    elif m_type == "YOLO":
        model = YOLO(m_name, config, logger)
    elif m_type == "GAP":
        model = GAP(m_name, config, logger)
    elif m_type == "NAS":
        model = NASNET(m_name, config, logger)
    elif m_type == "INC":
        model = Inception(m_name, config, logger)
    else:
        raise ValueError

    # 加载最佳模型
    ckpt = tf.train.get_checkpoint_state(path)
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        logger.log("Reloading model parameters..")
        model.restore(session, ckpt.model_checkpoint_path)

    else:
        raise ValueError("There is no best model with given model")

    return model


def rescale(image):
    """
    如果输入视频不是网络大小，则会调整输入视频的大小

    :param image:一个帧形式的输入视频

    :return:按比例缩小的帧
    """
    scale_side = max(image.shape)

    scale_value = config["input_width"] / scale_side

    scaled_image = cv2.resize(image, dsize=None, fx=scale_value, fy=scale_value)

    scaled_image = np.asarray(scaled_image, dtype=np.uint8)

    w_pad = int((config["input_width"] - scaled_image.shape[1]) / 2)
    h_pad = int((config["input_width"] - scaled_image.shape[0]) / 2)

    #  (config["image_width"], config["image_height"])
    new_image = (
        np.ones((config["input_width"], config["input_height"]), dtype=np.uint8) * 250
    )

    new_image[
        h_pad : h_pad + scaled_image.shape[0], w_pad : w_pad + scaled_image.shape[1]
    ] = scaled_image

    return new_image


def upscale_preds(_preds, _shapes):
    """

    在预测的瞳孔周围画一个圆圈获取预测并将其放大到视频的原始大小
    :param preds:
    :param shapes:
    :return: upscales x and y
    """

    pad_side = np.max(_shapes)

    downscale_value = config["input_width"] / pad_side

    scaled_height = _shapes[0] * downscale_value
    scaled_width = _shapes[1] * downscale_value

    w_pad = (config["input_width"] - scaled_width) / 2
    h_pad = (config["input_width"] - scaled_height) / 2

    x = _preds[0] - w_pad
    y = _preds[1] - h_pad
    w = _preds[2]

    upscale_value = pad_side / config["input_height"]

    x = x * upscale_value
    y = y * upscale_value
    w = w * upscale_value

    return x, y, w


# 从文件中加载具有最佳保存状态的模型，并预测输入视频的瞳孔位置。最终将视频与预测的瞳孔一起保存在磁盘上
def main(m_type, m_name, logger, Nystagmus_file, write_output=True):
    file_name = os.path.splitext(Nystagmus_file)[0]
    with tf.Session() as sess1:
        # 第一次
        model1 = load_model(sess1, m_type, m_name, logger)

        # 检查输入源是否为文件或相机
        if file_name == None:
            print("error")

        # 加载视频
        cap1 = cv2.VideoCapture(root_path + "data/" + file_name + "_left.mp4")
        ret1 = True
        counter1 = 0
        tic1 = time.time()
        frames1 = []
        preds1 = []
        result1 = []
        xcoordinates1 = []
        ycoordinates1 = []

        while ret1:
            ret1, frame1 = cap1.read()

            if ret1:
                frames1.append(frame1)
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
                f_shape1 = frame1.shape
                if frame1.shape[0] != 192:
                    frame1 = rescale(frame1)

                image1 = gray_normalizer(frame1)
                image1 = change_channel(image1, config["input_channel"])
                [p1] = model1.predict(sess1, [image1])
                x1, y1, w1 = upscale_preds(p1, f_shape1)

                preds1.append([x1, y1, w1])
                xcoordinates1.append(x1)
                ycoordinates1.append(y1)
                result1.append([x1, y1])

                # frames.append(gray)
                counter1 += 1

        toc1 = time.time()
        print("{0:0.2f} FPS".format(counter1 / (toc1 - tic1)))
    tf.reset_default_graph()

    # 视频大小
    video_size = frames1[0].shape[0:2]
    if write_output:
        # 准备视频写入以显示结果

        video1 = cv2.VideoWriter(
            root_path + "data/" + file_name + "_left.avi",
            cv2.VideoWriter_fourcc(*"XVID"),
            30,
            (video_size[1], video_size[0]),
        )

        for i, img in enumerate(frames1):
            # RGB(0,250,0)预测圈颜色
            labeled_img1 = annotator((0, 250, 0), img, *preds1[i])
            print("(" + str(xcoordinates1[i]) + "," + str(ycoordinates1[i]) + ")")

            video1.write(labeled_img1)

        plt.figure(figsize=(25.6, 14.4))
        # 创建小图1
        ##将小图分成2行1列,第三个参数表示第n个图
        plt.subplot(2, 1, 1)
        plt.xlabel("Samples")
        plt.ylabel("Pupil Position(Pixels)")
        plt.title("X")
        plt.plot(xcoordinates1[:])
        print("xcoordinates:", xcoordinates1)
        # np.savetxt('result/data/'+file_name+'_x.txt', xcoordinates1)

        # 创建小图2
        # 第三个参数表示是第2个图
        plt.subplot(2, 1, 2)
        plt.xlabel("Samples")
        plt.ylabel("Pupil Position(Pixels)")
        plt.title("Y")
        plt.plot(ycoordinates1[:])
        print("ycoordinates:", ycoordinates1)

        # 通过subplots_adjust()设置间距配置
        plt.subplots_adjust(
            left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.3
        )
        plt.savefig(root_path + "result/plot" + file_name + "_left.png")
        print("save:plot" + file_name + "_left.png")
        # plt.show()
        np.savetxt(root_path + "result/data/" + file_name + "_left.txt", result1)

        cv2.destroyAllWindows()
        video1.release()

    with tf.Session() as sess2:
        # 第二次
        model2 = load_model(sess2, m_type, m_name, logger)
        cap2 = cv2.VideoCapture(root_path + "data/" + file_name + "_right.mp4")
        ret2 = True
        counter2 = 0
        tic2 = time.time()
        frames2 = []
        preds2 = []
        xcoordinates2 = []
        ycoordinates2 = []
        result2 = []

        while ret2:
            ret2, frame2 = cap2.read()

            if ret2:
                # Our operations on the frame come here
                frames2.append(frame2)
                frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
                f_shape2 = frame2.shape
                if frame2.shape[0] != 192:
                    frame2 = rescale(frame2)

                image2 = gray_normalizer(frame2)
                image2 = change_channel(image2, config["input_channel"])
                [p2] = model2.predict(sess2, [image2])
                x2, y2, w2 = upscale_preds(p2, f_shape2)

                preds2.append([x2, y2, w2])
                xcoordinates2.append(x2)
                ycoordinates2.append(y2)
                result2.append([x2, y2])

                # frames.append(gray)
                counter2 += 1

        toc2 = time.time()
        print("{0:0.2f} FPS".format(counter2 / (toc2 - tic2)))

    # 视频大小
    video_size = frames2[0].shape[0:2]
    if write_output:
        # 准备视频写入以显示结果

        video2 = cv2.VideoWriter(
            root_path + "data/" + file_name + "_right.avi",
            cv2.VideoWriter_fourcc(*"XVID"),
            30,
            (video_size[1], video_size[0]),
        )

        for i, img in enumerate(frames2):
            # RGB(0,250,0)预测圈颜色
            labeled_img2 = annotator((0, 250, 0), img, *preds2[i])
            print("(" + str(xcoordinates2[i]) + "," + str(ycoordinates2[i]) + ")")

            video2.write(labeled_img2)

        plt.figure(figsize=(25.6, 14.4))
        # 创建小图1
        ##将小图分成2行1列,第三个参数表示第n个图
        plt.subplot(2, 1, 1)
        plt.xlabel("Samples")
        plt.ylabel("Pupil Position(Pixels)")
        plt.title("X")
        plt.plot(xcoordinates2[:])
        print("xcoordinates:", xcoordinates2)
        # np.savetxt('result/data/'+file_name+'_right_x.txt', xcoordinates2)

        # 创建小图2
        # 第三个参数表示是第2个图
        plt.subplot(2, 1, 2)
        plt.xlabel("Samples")
        plt.ylabel("Pupil Position(Pixels)")
        plt.title("Y")
        plt.plot(ycoordinates2[:])
        print("ycoordinates:", ycoordinates2)

        # 通过subplots_adjust()设置间距配置
        plt.subplots_adjust(
            left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.3
        )
        plt.savefig(root_path + "result/plot" + file_name + "_right.png")
        print("save:plot" + file_name + "_right.png")
        # plt.show()
        np.savetxt(root_path + "result/data/" + file_name + "_right.txt", result2)

        cv2.destroyAllWindows()
        video2.release()

    print("Done...")
    return "success!"


if __name__ == "__main__":
    # default
    Nystagmus_file = "2259.mp4"
    if len(sys.argv) >= 2:
        Nystagmus_file = sys.argv[1]
    file_name = os.path.splitext(Nystagmus_file)[0]
    eye_segmentation(Nystagmus_file)
    frametovideo(Nystagmus_file)

    # pupil_track(file_name+'_left')
    # pupil_track(file_name+'_right')

    # class_ = argparse.ArgumentDefaultsHelpFormatter
    # parser = argparse.ArgumentParser(description=__doc__,
    #                                 formatter_class=class_)

    # parser.add_argument('--model_type',
    #                    help="INC, YOLO, simple",
    #                    default="INC")

    # parser.add_argument('--model_name',
    #                    help="name of saved model (3A4Bh-Ref25)",
    #                    default="3A4Bh-Ref25")

    # parser.add_argument('video_path',help="path to video file, empty for camera")

    # args = parser.parse_args()

    # model_name = args.model_name
    model_name = "3A4Bh-Ref25"
    model_type = "INC"
    # video_path = 'data/'+Nystagmus_file

    # 初始化logger
    logger = Logger(model_type, model_name, "", config, dir="models/")
    logger.log("Start inferring model...")

    main(model_type, model_name, logger, Nystagmus_file)

    # main(model_type, model_name, logger, file_name+'_right')
