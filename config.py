class Config(object):
    data_path = 'data/'  # 数据集存放路径
    num_workers = 4  # 多进程加载数据所用的进程数
    image_size = 96  # 图片尺寸
    batch_size = 256
    max_epoch = 200
    lr1 = 2e-3  # 生成器的学习率
    lr2 = 2e-4  # 判别器的学习率
    beta1 = 0.5  # Adam优化器的beta1参数
    gpu = False  # 是否使用GPU
    nz = 100  # 噪声维度
    ngf = 64  # 生成器feature map数
    ndf = 64  # 判别器feature map数

    save_path = 'imgs/'  # 生成图片保存路径

    vis = False  # 是否使用visdom可视化
    env = 'GAN'  # visdom的env
    plot_every = 20  # 每间隔20 batch，visdom画图一次

    debug_file = '/tmp/debuggan'  # 存在该文件则进入debug模式
    d_every = 1  # 每1个batch训练一次判别器
    g_every = 2  # 每2个batch训练一次生成器
    save_every = 10  # 每10个epoch保存一次模型
    netd_path = 'checkpoints/netd_199.pth'  # 'checkpoints/netd_.pth' #预训练模型
    netg_path = 'checkpoints/netg_199.pth'  # 'checkpoints/netg_211.pth'

    # 测试时所用参数
    gen_img = 'result/result.png'
    # 从5000张生成的图片中保存最好的64张
    gen_num = 1
    gen_search_num = 100
    gen_mean = 0  # 噪声的均值
    gen_std = 1  # 噪声的方差

opt = Config()

