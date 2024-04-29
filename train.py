import torch as t
import torchvision as tv
import tqdm
from config import opt
from model import NetG, NetD
from torchnet.meter import AverageValueMeter

def train(**kwargs):
    for k_, v_ in kwargs.items():
        setattr(opt, k_, v_)

    device=t.device('cuda') if opt.gpu else t.device('cpu')

    # 数据
    transforms = tv.transforms.Compose([
        tv.transforms.Resize(opt.image_size),
        tv.transforms.CenterCrop(opt.image_size),
        tv.transforms.ToTensor(),
        tv.transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    dataset = tv.datasets.ImageFolder(opt.data_path, transform=transforms)
    dataloader = t.utils.data.DataLoader(dataset,
                                         batch_size=opt.batch_size,
                                         shuffle=True,
                                         num_workers=opt.num_workers,
                                         drop_last=True
                                         )

    # 网络
    netg, netd = NetG(opt), NetD(opt)
    map_location = lambda storage, loc: storage
    if opt.netd_path:
        netd.load_state_dict(t.load(opt.netd_path, map_location=map_location))
    if opt.netg_path:
        netg.load_state_dict(t.load(opt.netg_path, map_location=map_location))
    netd.to(device)
    netg.to(device)


    # 定义优化器
    optimizer_g = t.optim.Adam(netg.parameters(), opt.lr1, betas=(opt.beta1, 0.999))
    optimizer_d = t.optim.Adam(netd.parameters(), opt.lr2, betas=(opt.beta1, 0.999))

    # 真图片label为1，假图片label为0
    # noises为生成网络的输入
   # true_labels = t.ones(opt.batch_size).to(device)
   # fake_labels = t.zeros(opt.batch_size).to(device)
    fix_noises = t.randn(opt.batch_size, opt.nz, 1, 1).to(device)
    noises = t.randn(opt.batch_size, opt.nz, 1, 1).to(device)

    # 实例化用于计算平均值的工具类，用于在训练过程中跟踪损失函数的平均值。
    errord_meter = AverageValueMeter()
    errorg_meter = AverageValueMeter()

    epochs = range(opt.max_epoch)  # 创建迭代器对象epochs
    for epoch in epochs:
        for ii, (img, _) in tqdm.tqdm(enumerate(dataloader)):
            real_img = img.to(device)

            if ii % opt.d_every == 0:
                # 训练判别器

                optimizer_d.zero_grad()  # 训练开始前首先将优化器梯度清零
                # 尽可能的把真图片判别为正确,尽可能把假图片判别为错误

                r_preds = netd(real_img)  # 针对真实图片的预测分数

                noises.data.copy_(t.randn(opt.batch_size, opt.nz, 1, 1))  # 将随机生成的噪声数据复制到预先定义好的 noises 张量
                fake_img = netg(noises).detach()  # 根据噪声生成假图
                f_preds = netd(fake_img)
                # 参考Relativistic average HingeGAN
                r_f_diff = (r_preds - f_preds.mean()).clamp(max=1)
                f_r_diff = (f_preds - r_preds.mean()).clamp(min=-1)
                loss_d_real = (1 - r_f_diff).mean()
                loss_d_fake = (1 + f_r_diff).mean()
                loss_d = loss_d_real + loss_d_fake

                loss_d.backward()
                optimizer_d.step()
                errord_meter.add(loss_d.item())

            if ii % opt.g_every == 0:
                # 训练生成器
                optimizer_g.zero_grad()
                noises.data.copy_(t.randn(opt.batch_size, opt.nz, 1, 1))
                fake_img = netg(noises)
                f_preds = netd(fake_img)
                r_preds = netd(real_img)

                r_f_diff = r_preds - t.mean(f_preds)
                f_r_diff = f_preds - t.mean(r_preds)

                error_g = t.mean(t.nn.ReLU()(1+r_f_diff))+t.mean(t.nn.ReLU()(1-f_r_diff))
                error_g.backward()
                optimizer_g.step()
                errorg_meter.add(error_g.item())


        if (epoch+1) % opt.save_every == 0:
            # 保存模型、图片
            fix_fake_imgs = netg(fix_noises)
            tv.utils.save_image(fix_fake_imgs.data[:64], '%s/%s.png' % (opt.save_path, epoch+1), normalize=True,
                                value_range=(-1, 1))
            t.save(netd.state_dict(), 'checkpoints/netd_%s.pth' % epoch)
            t.save(netg.state_dict(), 'checkpoints/netg_%s.pth' % epoch)
            errord_meter.reset()
            errorg_meter.reset()
         