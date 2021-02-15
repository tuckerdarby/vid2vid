import sys
# sys.path.append('/home/tuck/code/vid2vid')
from models.models import create_model
from options.test_options import TestOptions
import numpy as np
import torch
from torch.autograd import Variable
import util.util as util
import cv2

# Setup options
opt = TestOptions().parse(save=False)
opt.nThreads = 1   # test code only supports nThreads = 1
opt.batchSize = 1  # test code only supports batchSize = 1
opt.serial_batches = True  # no shuffle
opt.no_flip = True  # no flip
opt.use_instance = True
opt.use_single_G = True
opt.fg = True
opt.name = 'label2city_1024_g1'
opt.checkpoints_dir = '/home/tuck/code/models/vid2vid/checkpoints/'
opt.dataroot = 'City'
opt.label_nc = 35
opt.loadSize = 1024
opt.n_scales_spatial = 3
opt.n_downsample_G = 2
# opt.no_dist_map = True
input_nc = 1 if opt.label_nc != 0 else opt.input_nc
opt.n_frames_G = 3

# python test.py --name label2city_1024_g1 --label_nc 35 --loadSize 1024 --n_scales_spatial 3 --use_instance --fg --n_downsample_G 2 --use_single_G

# Create model
model = create_model(opt)

def _get_image_tensor(m):
    ks = []
    for k in m:
        k = k.transpose(2,0,1)
        ks.append(k)
    ks = np.vstack(ks)
    ks = ks.reshape((1, 9, 512, 1024))
    image = np.array(ks, dtype=np.uint8)
    image = np.array(image, dtype=np.float32)
    image = torch.Tensor(image)
    return image

def convert_image(segment_map, instance_map):
    # segment_map = np.full((512, 1024, 3), 27)
    # instance_map = np.full((512, 1024, 3), 0)
    data = {
        'A': _get_image_tensor(segment_map),
        'B': torch.Tensor([0]),
        'inst': _get_image_tensor(instance_map),
        'change_seq': torch.Tensor([False])
    }

    _, _, height, width = data['A'].size()
    A = Variable(data['A']).view(1, -1, input_nc, height, width)
    B = Variable(data['B']).view(1, -1, opt.output_nc, height, width) if len(data['B'].size()) > 2 else None
    inst = Variable(data['inst']).view(1, -1, 1, height, width) if len(data['inst'].size()) > 2 else None
    generated = model.inference(A, B, inst)[0]
    generated = util.tensor2im(generated)
    return generated

# import cv2
# for i in range(15):
#     A = np.full((512, 1024, 3), 0)
#     # A[:,:] = (128, 64, 128)
#     inst = np.full((512, 1024, 3), 0)
#     im = convert_image(A, inst)
#     cv2.imshow('name', im)
#     cv2.waitKey(1)

# cv2.waitKey(1)
