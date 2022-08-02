import matplotlib
matplotlib.use('Agg')
import os, sys
os.environ['KMP_DUPLICATE_LIB_OK']='True'
import yaml
from argparse import ArgumentParser
from tqdm import tqdm

import imageio
import numpy as np
from skimage.transform import resize
from skimage import img_as_ubyte
import torch
from .sync_batchnorm import DataParallelWithCallback

from .modules.generator import OcclusionAwareGenerator
from .modules.keypoint_detector import KPDetector
from .animate import normalize_kp
from scipy.spatial import ConvexHull

import easydict

import random

def load_checkpoints(config_path, checkpoint_path, cpu=False):

    with open(config_path) as f:
        config = yaml.load(f)

    generator = OcclusionAwareGenerator(**config['model_params']['generator_params'],
                                        **config['model_params']['common_params'])
    if not cpu:
        generator.cuda()

    kp_detector = KPDetector(**config['model_params']['kp_detector_params'],
                             **config['model_params']['common_params'])
    if not cpu:
        kp_detector.cuda()
    
    if cpu:
        checkpoint = torch.load(checkpoint_path, map_location=torch.device('cpu'))
    else:
        checkpoint = torch.load(checkpoint_path)
 
    generator.load_state_dict(checkpoint['generator'])
    kp_detector.load_state_dict(checkpoint['kp_detector'])
    
    if not cpu:
        generator = DataParallelWithCallback(generator)
        kp_detector = DataParallelWithCallback(kp_detector)

    generator.eval()
    kp_detector.eval()
    
    return generator, kp_detector


def make_animation(source_image, driving_video, generator, kp_detector, relative=True, adapt_movement_scale=True, cpu=False):
    with torch.no_grad():
        predictions = []
        source = torch.tensor(source_image[np.newaxis].astype(np.float32)).permute(0, 3, 1, 2)
        if not cpu:
            source = source.cuda()
        driving = torch.tensor(np.array(driving_video)[np.newaxis].astype(np.float32)).permute(0, 4, 1, 2, 3)
        kp_source = kp_detector(source)
        kp_driving_initial = kp_detector(driving[:, :, 0])

        for frame_idx in tqdm(range(driving.shape[2])):
            driving_frame = driving[:, :, frame_idx]
            if not cpu:
                driving_frame = driving_frame.cuda()
            kp_driving = kp_detector(driving_frame)
            kp_norm = normalize_kp(kp_source=kp_source, kp_driving=kp_driving,
                                   kp_driving_initial=kp_driving_initial, use_relative_movement=relative,
                                   use_relative_jacobian=relative, adapt_movement_scale=adapt_movement_scale)
            out = generator(source, kp_source=kp_source, kp_driving=kp_norm)

            predictions.append(np.transpose(out['prediction'].data.cpu().numpy(), [0, 2, 3, 1])[0])
    return predictions


def make_portrait(q, img_path, user_id):
    opt = easydict.EasyDict({
        'config': 'deeplearning/config/vox-256.yaml',
        'checkpoint': 'vox-cpk.pth.tar',
        'result_video': 'result.mp4',
        'best_frame': None,
        'cpu': True,
        'relative': True,

        'adapt_scale': False,
        'find_best_frame': False
    })
    
    source_image = imageio.imread(img_path)

    rand = random.randrange(1, 5)
    video_path = f'deeplearning/original_video/{rand}.mp4'
    reader = imageio.get_reader(video_path)

    fps = reader.get_meta_data()['fps']
    driving_video = []
    try:
        for im in reader:
            driving_video.append(im)
    except RuntimeError:
        pass
    reader.close()

    source_image = resize(source_image, (256, 256))[..., :3]
    driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]
    generator, kp_detector = load_checkpoints(config_path=opt.config, checkpoint_path=opt.checkpoint, cpu=opt.cpu)

    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=opt.relative, adapt_movement_scale=opt.adapt_scale, cpu=opt.cpu)

    filename = f'{user_id}.gif'
    imageio.mimsave(filename, [img_as_ubyte(frame) for frame in predictions], fps=fps)

    os.system(f'aws s3 cp {filename} s3://wm-portrait --acl public-read')
    # os.system(f'rm {filename}')

    portrait_url = f'https://wm-portrait.s3.ap-northeast-2.amazonaws.com/{user_id}.gif'

    q.put(portrait_url)

