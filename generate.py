import torch as t
import torchvision as tv
import shutil
import os
from config import opt
from model import NetG, NetD
#print(opt.netd_path)
def generate(**kwargs):
    """
    随机生成动漫头像，并根据netd的分数选择较好的
    """
    for k_, v_ in kwargs.items():
        setattr(opt, k_, v_)

    device = t.device('cuda') if opt.gpu else t.device('cpu')

    netg, netd = NetG(opt).eval(), NetD(opt).eval()
    noises = t.randn(opt.gen_search_num, opt.nz, 1, 1).normal_(opt.gen_mean, opt.gen_std)
    noises = noises.to(device)

    map_location = lambda storage, loc: storage
    netd.load_state_dict(t.load(opt.netd_path, map_location=map_location))
    netg.load_state_dict(t.load(opt.netg_path, map_location=map_location))
    netd.to(device)
    netg.to(device)

    # 生成图片，并计算图片在判别器的分数
    fake_img = netg(noises)
    scores = netd(fake_img).detach()

    # 挑选最好的某几张
    
    indexs = scores.topk(int(opt.gen_num))[1]
    result = []
    for ii in indexs:
        result.append(fake_img.data[ii])
    # 保存图片
    tv.utils.save_image(t.stack(result), opt.gen_img, normalize=True, value_range=(-1, 1))
  # 复制图片到 imgs 文件夹并按顺序命名
    imgs_folder = 'imgs'
    if not os.path.exists(imgs_folder):
        os.makedirs(imgs_folder)
    
    # 获取已存在的图片序号
    existing_files = os.listdir(imgs_folder)
    num_existing_files = len(existing_files)
    
    # 生成新文件名
    new_file_name = os.path.join(imgs_folder, f'result_{num_existing_files + 1}.png')
    
    # 复制图像文件
    shutil.copy(opt.gen_img, new_file_name)

