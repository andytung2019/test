import pickle as p
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as plimg
from PIL import Image
def load_CIFAR_batch(filename):
    """ load single batch of cifar """
    with open(filename, 'rb')as f:
#        datadict = p.load(f)
        datadict = p.load(f,encoding='latin1')
        X = datadict['data']
        Y = datadict['labels']
        X = X.reshape(10000, 3, 32, 32)
        Y = np.array(Y)
        return X, Y
 
def load_CIFAR_Labels(filename):
    with open(filename, 'rb') as f:
        lines = [x for x in f.readlines()]
        print(lines)
 
 
if __name__ == "__main__":
    load_CIFAR_Labels("./cifar-10-batches-py/batches.meta")
    imgX, imgY = load_CIFAR_batch("./cifar-10-batches-py/data_batch_1")
    print(imgX.shape)
    print("saving ......")
#    for i in range(imgX.shape[0]):
    for i in range(300):#
#        imgs = imgX[i - 1]
        imgs = imgX[i]
        img0 = imgs[0]
        img1 = imgs[1]
        img2 = imgs[2]
        i0 = Image.fromarray(img0)#
        i1 = Image.fromarray(img1)
        i2 = Image.fromarray(img2)
        img = Image.merge("RGB",(i0,i1,i2))
        name = "img" + str(i)+'.png'
        img.save("./cifar10_images/"+name,"png")#
        for j in range(imgs.shape[0]):
#                img = imgs[j - 1]
                img = imgs[j]
                name = "img" + str(i) + str(j) + ".png"
                print("save ..." + name)
                plimg.imsave("./cifar10_images/" + name, img)#

