import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torchvision.transforms.functional import InterpolationMode


class TensorScale_255to1:
    def __call__(self, img):
        return img.float() / 255

class TensorLabeltoLong:
    def __call__(self, label):
        label = label.reshape(label.shape[1], label.shape[2])
        label = label.long()
        return label


def label_remap(img, old_values, new_values):
    # Replace old values by the new ones
    tmp = torch.zeros_like(img)
    for old, new in zip(old_values, new_values):
        tmp[img == old] = new

    return tmp


def RandomScaleCrop(image, label):
    """
    scale the images in the range (0.5,1.5) for Cityscapes
    then extract a crop with size 512×1024 for Cityscapes
    """
    scale = np.random.uniform(0.5, 1.5) 
    #print('scale:', scale)
    new_h, new_w = int(scale * image.shape[-2]), int(scale * image.shape[-1])
    #print(new_h, new_w)
    image = transforms.functional.resize(image, (new_h, new_w), InterpolationMode.BILINEAR)
    label = transforms.functional.resize(label, (new_h, new_w), InterpolationMode.NEAREST)
    #print(image.shape, label.shape)
    rect = transforms.RandomCrop.get_params(image, (512, 1024))
    #print(rect)
    image = transforms.functional.crop(image, *rect)
    label = transforms.functional.crop(label, *rect)
    #print(image.shape, label.shape)

    return image, label

def get_transform():
    image_transform = transforms.Compose([
        transforms.Resize((512, 1024)),
        TensorScale_255to1()
    ])

    label_transform = transforms.Compose([
        transforms.Resize((512, 1024), InterpolationMode.NEAREST),  
        TensorLabeltoLong()
    ])
    return image_transform, label_transform