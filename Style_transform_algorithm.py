# for DL modeling

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as T
import time
from imageio.v2 import imread

# for number-crunching
import numpy as np

# for data visualization
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('svg')


class Style_transfer():
    def __init__(self,content_image,style_image):
        self.content_image = content_image
        self.style_image = style_image
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')


    def load_vgg19_model_and_freez_weights(self):
        # import the mVgg19 odel
        self.vggnet = torchvision.models.vgg19(pretrained=True)
        # freeze all layers
        for parameters in self.vggnet.parameters():
            parameters.requires_grad = False
        # set to evaluation mode
        self.vggnet.eval()
        # send the network to the GPU if available
        self.vggnet.to(self.device)
        self.vggnet
    def prepare_images(self):
        # initialize the target image and random numbers
        self.target_image = np.random.randint(low=0,high=255,size=self.content_image.shape,dtype=np.uint8)
    def image_transformations(self):
        # create the transforms
        Ts = T.Compose([ T.ToTensor(),
                 T.Resize(256),
                 T.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
               ])
        self.content_image = Ts( self.content_image ).unsqueeze(0).to(self.device)
        self.style_image   = Ts( self.style_image   ).unsqueeze(0).to(self.device)
        self.target_image  = Ts( self.target_image  ).unsqueeze(0).to(self.device)
    # A function that returns feature maps
    def getFeatureMapActs(self,img, net):
        # initialize feature maps as a list
        featuremaps = []
        featurenames = []

        convLayerIdx = 0

        # loop through all layers in the "features" block
        for layernum in range(len(net.features)):

            # print out info from this layer
            # print(layernum,net.features[layernum])

            # process the image through this layer
            img = net.features[layernum](img)

            # store the image if it's a conv2d layer
            if 'Conv2d' in str(net.features[layernum]):
                # print('getFeatureMapActs : ConvLayer_' , str(convLayerIdx) , " image shape:" ,img.size)
                featuremaps.append(img)
                featurenames.append('ConvLayer_' + str(convLayerIdx))
                convLayerIdx += 1

        return featuremaps, featurenames
    # A function that returns the Gram matrix of the feature activation map
    def gram_matrix(self,M):
        # reshape to 2D
        _, chans, height, width = M.shape
        M = M.reshape(chans, height * width)

        # compute and return covariance matrix
        gram = torch.mm(M, M.t()) / (chans * height * width)
        return gram
    def select_layers(self,layers4content,layers4style,weights4style):
        #Now for the transfer
        #which layers to use
        self.layers4content = layers4content
        self.layers4style   = layers4style
        self.weights4style  = weights4style
    def train_the_image(self,numepochs,styleScaling,learning_rate):
        # make a copy of the target image and push to GPU

        self.target_image.requires_grad = True
        self.target_image = self.target_image.to(self.device)
        self.styleScaling = styleScaling

        # number of epochs to train
        numepochs = numepochs

        # optimizer for backprop
        optimizer = torch.optim.RMSprop([self.target_image], lr=learning_rate)

        for epochi in range(numepochs):
            print(epochi)
            # extract the target feature maps
            targetFeatureMaps, targetFeatureNames = self.getFeatureMapActs(self.target_image, self.vggnet)
            styleFeatureMaps,styleFeatureNames = self.getFeatureMapActs(self.style_image,self.vggnet)
            contentFeatureMaps, contentFeatureNames = self.getFeatureMapActs(self.content_image, self.vggnet)

            # initialize the individual loss components
            styleLoss = 0
            contentLoss = 0

            # loop over layers
            for layeri in range(len(targetFeatureNames)):

                # compute the content loss
                if targetFeatureNames[layeri] in self.layers4content:
                    contentLoss += torch.mean((targetFeatureMaps[layeri] - contentFeatureMaps[layeri]) ** 2)

                # compute the style loss
                if targetFeatureNames[layeri] in self.layers4style:
                    # Gram matrices
                    # print(targetFeatureMaps[layeri].shape,styleFeatureMaps[layeri].shape)
                    Gtarget = self.gram_matrix(targetFeatureMaps[layeri])
                    Gstyle = self.gram_matrix(styleFeatureMaps[layeri])
                    # print(Gtarget.shape,Gstyle.shape)

                    # compute their loss (de-weighted with increasing depth)
                    styleLoss += torch.mean((Gtarget - Gstyle) ** 2) * self.weights4style[self.layers4style.index(targetFeatureNames[layeri])]
            # combined loss
            combiloss = styleScaling * styleLoss + contentLoss
            # print(styleScaling*styleLoss,styleScaling,styleLoss,contentLoss)
            # print(combiloss)
            # finally ready for backprop!
            optimizer.zero_grad()
            combiloss.backward()
            optimizer.step()
    def get_trained_image(self):
        return torch.sigmoid(self.target_image).cpu().detach().squeeze().numpy().transpose((1,2,0))
if __name__ == "__main__":
    numepochs = 1500
    styleScaling = 1e6
    learning_rate = 0.005
    layers4content = ['ConvLayer_1', 'ConvLayer_4']
    layers4style = ['ConvLayer_1', 'ConvLayer_2', 'ConvLayer_3', 'ConvLayer_4', 'ConvLayer_5']
    weights4style = [1, .5, .5, .2, .1]

    img4content = imread('https://upload.wikimedia.org/wikipedia/commons/6/61/De_nieuwe_vleugel_van_het_Stedelijk_Museum_Amsterdam.jpg')
    img4style = imread('https://upload.wikimedia.org/wikipedia/commons/c/c5/Edvard_Munch%2C_1893%2C_The_Scream%2C_oil%2C_tempera_and_pastel_on_cardboard%2C_91_x_73_cm%2C_National_Gallery_of_Norway.jpg')
    start_time = time.time()
    styleobject = Style_transfer(content_image=img4content,style_image=img4style)
    styleobject.load_vgg19_model_and_freez_weights()
    styleobject.prepare_images()
    styleobject.image_transformations()

    styleobject.select_layers(layers4content=layers4content,
                              layers4style=layers4style,
                              weights4style=weights4style)

    styleobject.train_the_image(numepochs = numepochs,
                                styleScaling = styleScaling,
                                learning_rate = learning_rate)
    target_image = styleobject.get_trained_image()
    end_time = time.time()
    print(f"Execution time for {numepochs} is {end_time - start_time} seconds")
    #print(target_image)
    plt.imshow(target_image)
    #print(target_image)
    plt.title('Target picture', fontweight='bold')
    plt.show()






