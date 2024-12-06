#from openai import OpenAI
import openai
import os#处理环境变量
import io#处理字节流数据
import base64
from PIL import Image
import json


def encode_image(image):
    image = image.resize((256, 256))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

client =openai.OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY2"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
# 指定包含图片的文件夹路径
image_folder_path = r'C:\Users\Administrator.DESKTOP-DJPMUJC\Desktop\HOMEWORK\机器学习\T_project\NSD_dataset_image\subj08\train'
# 构建要保存到JSON文件中的数据结构(字典)图片名和描述一一对应
new_images_dict = {}
#单一文件处理
#image_path=r"C:\Users\Administrator.DESKTOP-DJPMUJC\Desktop\image.png"
#file_name = os.path.basename(image_path)
#image = Image.open(image_path)
#base64_image = encode_image(image)
#批量处理
for filename in os.listdir(image_folder_path):#遍历文件夹
    if filename.endswith('.jpg') or filename.endswith('.png'):#筛选图片文件
        image_path = os.path.join(image_folder_path, filename)#拼接图片路径
        try:#遇到异常继续执行
            image = Image.open(image_path)
            base64_image = encode_image(image)
            #调用 chat.completions.create 方法，向 qwen-vl-max-latest 模型发送一个聊天完成请求。
            response = client.chat.completions.create(
                model="qwen-vl-max-latest", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                messages=[
                            {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Please output a brief caption of the image. For example, 'This is a black dog chewing an orange frisbee on the green grass.'"
                                },
                                {
                                    "type": "image_url", 
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                                    ]
                                }   
                    ]
                )
            caption=response.choices[0].message.content#打印图片描述
            new_images_dict[filename] = caption
            #print(caption)#打印图片描述
        except openai.BadRequestError as e:
            # 如果API请求失败（例如因为内容审核未通过），将描述设置为空字符串
            new_images_dict[filename] = "This picture makes it illegal"
            continue  # 继续处理下一个图片
        except Exception as e:
            # 捕获其他可能的异常，并将描述设置为空字符串
            new_images_dict[filename] = "Some other request errors"
            continue  # 继续处理下一个图片
# 解析API响应中的usage信息
#res_json = response.to_dict()  # 将API响应转换为字典
#usage = res_json.get("usage", {})
#total_tokens = usage.get("total_tokens", 0)
#print(f"Total Tokens Used: {total_tokens}")

# 指定JSON文件的路径
json_file_path = 'captionofsub8.json'
# 将数据写入JSON文件（追加）
# 读取已有的JSON文件内容
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        try:
            # 尝试加载现有数据
            images_dict = json.load(json_file)
        except json.JSONDecodeError:
            # 如果文件存在但不是有效的JSON，则初始化为空字典
            images_dict = {}
else:
    # 如果文件不存在，则初始化为空字典
    images_dict = {}

# 将新数据合并到现有数据中
images_dict.update(new_images_dict)

# 将合并后的数据写回到JSON文件
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(images_dict, json_file, ensure_ascii=False, indent=4)
# 将数据写入JSON文件（覆盖重新）
#with open(json_file_path, 'w', encoding='utf-8') as json_file:
#   json.dump(images_dict, json_file, ensure_ascii=False, indent=4)
print("Done!")