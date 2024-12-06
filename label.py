# -*- coding: utf-8 -*-
# 引入依赖包
# pip install alibabacloud_imagerecog20190930

import os#处理环境变量
import io#处理字节流数据
from urllib.request import urlopen#用于从URL获取图像数据
from alibabacloud_imagerecog20190930.client import Client#用于初始化API客户端
from alibabacloud_imagerecog20190930.models import GenerateCaptionRequest#用于构造API请求
from alibabacloud_tea_openapi.models import Config
from alibabacloud_tea_util.models import RuntimeOptions
import matplotlib.pyplot as plt#显示图像
from PIL import Image#处理图像数据
## 配置API客户端
config = Config(
  # 创建AccessKey ID和AccessKey Secret，请参考https://help.aliyun.com/document_detail/175144.html
  # 如果您用的是RAM用户的AccessKey，还需要为RAM用户授予权限AliyunVIAPIFullAccess，请参考https://help.aliyun.com/document_detail/145025.html
  # 从环境变量读取配置的AccessKey ID和AccessKey Secret。运行代码示例前必须先配置环境变量。
  access_key_id=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID'),
  access_key_secret=os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET'),
  # 访问的域名
  endpoint='imagerecog.cn-shanghai.aliyuncs.com',#阿里云图像识别服务在上海区域的API入口即端点。
  # 访问的域名对应的region
  region_id='cn-shanghai'
)

## 加载图像
#场景一：文件在本地
#img = open(r'C:\Users\Administrator.DESKTOP-DJPMUJC\Desktop\HOMEWORK\机器学习\T_project\NSD_dataset_image\subj01\train\train-0120_nsd-01013.png', 'rb')
#场景二：使用任意可访问的url 从URL获取图像的二进制数据
url = 'https://viapi-test-bj.oss-cn-beijing.aliyuncs.com/viapi-3.0domepic/imagerecog/TaggingImage/TaggingImage1.jpg'
img = io.BytesIO(urlopen(url).read())#将二进制数据转换为字节流对象

##构造API请求
request = GenerateCaptionRequest()#创建一个 TaggingImageAdvanceRequest 对象，用于构造API请求
request.image_urlobject = img#将图像数据赋值给 image_urlobject 字段
runtime = RuntimeOptions()#用于设置API调用的运行时选项
request.max_length = 100  # 设置生成描述的最大长度
request.language = 'zh'   # 设置生成描述的语言为中文
## 调用API并获取结果
try:
  # 初始化Client客户端
  client = Client(config)#用config初始化API客户端
  #物体识别
  response = client.tgenerate_caption(request, runtime)
  caption = response.body.caption
  # 获取整体结果
  print(f"生成的描述: {caption}")#打印API返回的完整响应体
except Exception as error:
  # 获取整体报错信息
  print(error)
  # 获取单个字段
  print(error.code)

#plt.show()