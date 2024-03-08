from flask import Flask, render_template, request, jsonify, send_file
import sys
import os
import requests
import json
import io
from base64 import encodebytes
from PIL import Image


app = Flask(__name__)
root_path = "/var/www/app/"


def get_response_image(image_path):
    pil_img = Image.open(image_path, mode="r")  # 读 PIL 图像
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format="PNG")  # PIl图像 -> 二进制
    encoded_img = encodebytes(byte_arr.getvalue()).decode("ascii")  #   base64
    return encoded_img


@app.route("/")
def index():
    return "erro123r", 404


@app.route("/test/<string:videoname>", methods=["POST", "GET"])
def upload(videoname):
    if request.method == "POST":
        file_name = request.form.get("first")
        # 这个是根据小程序demo中视频的存储方式，设置的下载链接（小程序前端通过POST将视频名称传给后端）
        download_url = (
            "https://636c-cloud1-6gxw9l7437b94ed0-1312301817.tcb.qcloud.la/video/"
            + file_name
            + ".mp4"
        )

        file = root_path + "/data/" + file_name + ".mp4"
        r = requests.get(download_url, stream=True)
        with open(file, "wb") as f:
            f.write(r.content)

        # 调用nystagmus.py，注意传参
        com = (
            "sudo  nohup python -u "+ root_path+"nystagmus.py "+ file_name+ ".mp4 > "+ root_path+"test.log 2>&1 &"
        )

        if os.system(com) == 0:
            result = "success"
        else:
            result = "failed"
        return jsonify({"code": 200, "success": 0, "msg": "download over:" + result})

    elif request.method == "GET":
        if videoname == "":
            return jsonify({"code": 404})
        elif len(videoname) == 32:
            if os.path.exists(root_path + "/result/plot" + videoname + "_left.png") and os.path.exists(root_path + "/result/plot" + videoname + "_right.png"):
                result = [
                    root_path + "/result/plot" + videoname + "_left.png",
                    root_path + "/result/plot" + videoname + "_right.png",
                ]
                encoded_imges = []
                for image_path in result:
                    encoded_imges.append(get_response_image(image_path))

                # return send_file(filename, mimetype='image/png')
            else:
                encoded_imges = "not exit"
            # m='success:'+videoname

            return jsonify(
                {
                    "code": 200,
                    "success": 0,
                    "msg": "success:" + videoname,
                    "img": encoded_imges,
                }
            )


if __name__ == "__main__":
    app.run()
