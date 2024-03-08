Ⅰ main.py
flask入口函数，定义了POST/GET方法（主要是看这个）

Ⅱ nystagmus.py
生成眼震视图

Ⅲ predict.py
调用分类模型




PS1:这个文件夹在原服务器上的位置是/var/www/app/，在代码中使用了绝对位置root_path = "/var/www/app/"，这个得改

PS2:main中小程序视频下载链接，这个得改

PS3:调用predict.py分类没写，需要参考main.py中在合适的时候调用

PS4:配置环境比较重要,以下为原环境部分包版本(视具体情况定d=====(￣▽￣*)b，不一定要按这个来，能运行就行)
python==3.6.9//
dlib==19.24.99//
Flask==2.0.3//
matplotlib==3.3.4//
numpy==1.19.5//
opencv-contrib-python==3.4.10.35//
Pillow==8.3.1//
PyYAML==5.4.1//
requests==2.25.1//
scipy==1.5.2//
tensorboard==2.9.1//
tensorflow==2.5.2

tensorflow-hub==0.8.0//
...