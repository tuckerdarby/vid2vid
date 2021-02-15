import sys
sys.path.append('/home/tuck/code/models/SPADE')
from models.pix2pix_model import Pix2PixModel
from options.test_options import TestOptions
import numpy as np
import torch
from util import util

opt = TestOptions().parse()
model = Pix2PixModel(opt)

print(opt)

def convert_image(image):
    image = np.array(image[:,:,0].reshape(1,1,256,256))
    image = torch.cuda.FloatTensor(image)
    data = {
        'label': image,
        'image': image,
        'instance': image
    }

    generated = model(data, mode='inference')
    generated = util.tensor2im(generated)
    return generated[0]
