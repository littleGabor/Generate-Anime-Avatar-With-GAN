from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
from config import opt
from generate import generate
import subprocess
import base64
import shutil
import os
import json

app = Flask(__name__)
CORS(app)
imgs_folder = 'imgs'  # 历史图片保存的文件夹路径
imgs_like_folder = 'like' # 喜欢的图片保存的文件夹路径

@app.route('/history')
def get_history_images():
    images = []
    
    # 遍历imgs文件夹下的所有图片文件
    for filename in os.listdir(imgs_folder):
        if filename.endswith('.png'):  # 假设图片格式为png，根据实际情况修改
            with open(os.path.join(imgs_folder, filename), 'rb') as f:
                img_data = f.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            images.append({'filename': filename, 'base64': img_base64})

    return jsonify(images)


@app.route('/like')
def get_like_images():
    images = []
    
    # 遍历imgs文件夹下的所有图片文件
    for filename in os.listdir(imgs_like_folder):
        if filename.endswith('.png'):  # 假设图片格式为png，根据实际情况修改
            with open(os.path.join(imgs_like_folder, filename), 'rb') as f:
                img_data = f.read()
            img_base64 = base64.b64encode(img_data).decode('utf-8')
            images.append({'filename': filename, 'base64': img_base64})

    return jsonify(images)


@app.route('/switch-model', methods=['POST'])
def switch_model():
    data = request.get_json()
    model_name = data.get('model_name')

    # 根据选择的模型名称更新 netd_path 和 netg_path
    if model_name == '1':
        opt.netd_path = 'path_to_model_1'
        opt.netg_path = 'path_to_model_1'
    elif model_name == '2':
        opt.netd_path = 'path_to_model_2'
        opt.netg_path = 'path_to_model_2'
    # 添加更多的模型选择

    # 返回成功消息
    return jsonify({'message': 'Model switched successfully'}), 200




@app.route('/update-config', methods=['POST'])
def update_config():
    try:
        # 检查请求数据是否包含'new_config'
        if 'new_config' not in request.json:
            return jsonify({'error': 'Invalid request: no new_config provided'}), 422

        # 更新配置
        new_config = request.json['new_config']
        for key, value in new_config.items():
            setattr(opt, key, value)
    #    print('后端', opt.gen_num)
   #     print(opt.netd_path)
        # 调用 generate 函数生成图片
        generate()

        result_path = opt.gen_img  # 生成的图片路径
        if not os.path.isfile(result_path):
            return jsonify({'error': 'Generated image not found'}), 404

        # 读取生成的图片并转换为 Base64 编码
        with open(result_path, 'rb') as f:
            img_data = f.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')

        # 返回生成的图片的 Base64 编码给前端
        return jsonify({'message': 'Image generated successfully', 'image_base64': img_base64}), 200

    except Exception as e:
        # 记录错误日志
        app.logger.error(f'Error generating image: {str(e)}')
        return jsonify({'error': f'Error generating image: {str(e)}'}), 500




@app.route('/clear-history', methods=['DELETE'])
def clear_history():
    def clear_imgs_folder():
        # 删除imgs文件夹中的所有文件
        for filename in os.listdir(imgs_folder):
            file_path = os.path.join(imgs_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    clear_imgs_folder()  # 调用清空imgs文件夹的函数
    return 'History images cleared successfully'

@app.route('/clear-like', methods=['DELETE'])
def clear_like():
    def clear_imgs_like_folder():
        # 删除imgs文件夹中的所有文件
        for filename in os.listdir(imgs_like_folder):
            file_path = os.path.join(imgs_like_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

    clear_imgs_like_folder()  # 调用清空imgs文件夹的函数
    return 'History images cleared successfully'

@app.route('/copy-file', methods=['POST'])
def copy_file():
    try:
        # 执行文件复制操作
         # 获取已存在的图片序号
        existing_files = os.listdir(imgs_like_folder)
        num_existing_files = len(existing_files)
        
        # 生成新文件名
        new_file_name = os.path.join(imgs_like_folder, f'result_{num_existing_files + 1}.png')
        
        # 复制图像文件
        shutil.copy('result/result.png', new_file_name)
        return 'File copied successfully', 200
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)


