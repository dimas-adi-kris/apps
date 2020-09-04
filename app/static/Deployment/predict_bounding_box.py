# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 17:17:47 2020

@author: ISYSRG.COM
"""

from __future__ import division
import cv2
import numpy as np
import sys
import pickle
from optparse import OptionParser
import time
from keras_frcnn import config
from keras import backend as K
from keras.layers import Input
from keras.models import Model
from keras_frcnn import roi_helpers
from keras.applications.mobilenet import preprocess_input
from keras_frcnn import vgg as nn
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


def format_img_size(img, C):
    """ formats the image size based on config """
    img_min_side = float(C.im_size)
    (height,width,_) = img.shape
        
    if width <= height:
        ratio = img_min_side/width
        new_height = int(ratio * height)
        new_width = int(img_min_side)
    else:
        ratio = img_min_side/height
        new_width = int(ratio * width)
        new_height = int(img_min_side)
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    return img, ratio    

def format_img_channels(img, C):
    """ formats the image channels based on config """
    img = img[:, :, (2, 1, 0)]
    img = img.astype(np.float32)
    img[:, :, 0] -= C.img_channel_mean[0]
    img[:, :, 1] -= C.img_channel_mean[1]
    img[:, :, 2] -= C.img_channel_mean[2]
    img /= C.img_scaling_factor
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0)
    return img

def format_img(img, C):
    """ formats an image for model prediction based on config """
    img, ratio = format_img_size(img, C)
    img = format_img_channels(img, C)
    return img, ratio


# Method to transform the coordinates of the bounding box to its original size
def get_real_coordinates(ratio, x1, y1, x2, y2):

    real_x1 = int(round(x1 // ratio))
    real_y1 = int(round(y1 // ratio))
    real_x2 = int(round(x2 // ratio))
    real_y2 = int(round(y2 // ratio))

    return (real_x1, real_y1, real_x2 ,real_y2)


def predict(filepath):
    import os
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    
    sys.setrecursionlimit(40000)
    
    parser = OptionParser()
    
    num_rois = 10
    config_filename = "config_combine_200.pickle"
    network = "vgg"
    write = True
    load = "models/vgg/combine_200.hdf5"
    
    
    config_output_filename = config_filename
    
    with open(config_output_filename, 'rb') as f_in:
        C = pickle.load(f_in)
    
    # turn off any data augmentation at test time
    C.network = "vgg16"
    C.use_horizontal_flips = False
    C.use_vertical_flips = False
    C.rot_90 = False

    
    class_mapping = C.class_mapping
    
    if 'bg' not in class_mapping:
        class_mapping['bg'] = len(class_mapping)
    
    class_mapping = {v: k for k, v in class_mapping.items()}
    print(class_mapping)
    class_to_color = {class_mapping[v]: np.random.randint(0, 255, 3) for v in class_mapping}
    C.num_rois = int(num_rois)
    
    if C.network == 'resnet50':
        num_features = 1024
    elif C.network =="mobilenetv2":
        num_features = 320
    else:
        # may need to fix this up with your backbone..!
        print("backbone is not resnet50. number of features chosen is 512")
        num_features = 512
    
    if K.image_dim_ordering() == 'th':
        input_shape_img = (3, None, None)
        input_shape_features = (num_features, None, None)
    else:
        input_shape_img = (None, None, 3)
        input_shape_features = (None, None, num_features)
    
    
    img_input = Input(shape=input_shape_img)
    roi_input = Input(shape=(C.num_rois, 4))
    feature_map_input = Input(shape=input_shape_features)
    
    # define the base network (resnet here, can be VGG, Inception, etc)
    shared_layers = nn.nn_base(img_input)
    
    # define the RPN, built on the base layers
    num_anchors = len(C.anchor_box_scales) * len(C.anchor_box_ratios)
    rpn_layers = nn.rpn(shared_layers, num_anchors)
    
    classifier = nn.classifier(feature_map_input, roi_input, C.num_rois, nb_classes=len(class_mapping))
    
    model_rpn = Model(img_input, rpn_layers)
    model_classifier = Model([feature_map_input, roi_input], classifier)
    
    # model loading
    if load == None:
      print('Loading weights from {}'.format(C.model_path))
      model_rpn.load_weights(C.model_path, by_name=True)
      model_classifier.load_weights(C.model_path, by_name=True)
    else:
      print('Loading weights from {}'.format(load))
      model_rpn.load_weights(load, by_name=True)
      model_classifier.load_weights(load, by_name=True)
    
    #model_rpn.compile(optimizer='adam', loss='mse')
    #model_classifier.compile(optimizer='adam', loss='mse')
    
    all_imgs = []
    classes = {}
    bbox_threshold = 0.5
    
    visualise = True
    num_rois = C.num_rois
    
    st = time.time()
    if "/" in filepath:
        img_name = filepath.split("/")[-1]
    else:
        img_name = filepath.split("\\")[-1]
    
    img = cv2.imread(filepath)

    # preprocess image
    X, ratio = format_img(img, C)
    img_scaled = (np.transpose(X[0,:,:,:],(1,2,0)) + 127.5).astype('uint8')
    if K.image_dim_ordering() == 'tf':
        X = np.transpose(X, (0, 2, 3, 1))
    # get the feature maps and output from the RPN
    [Y1, Y2, F] = model_rpn.predict(X)
    

    R = roi_helpers.rpn_to_roi(Y1, Y2, C, K.image_dim_ordering(), overlap_thresh=0.7)
    # print(R.shape)
    
    # convert from (x1,y1,x2,y2) to (x,y,w,h)
    R[:, 2] -= R[:, 0]
    R[:, 3] -= R[:, 1]

    # apply the spatial pyramid pooling to the proposed regions
    bboxes = {}
    probs = {}
    for jk in range(R.shape[0]//num_rois + 1):
        ROIs = np.expand_dims(R[num_rois*jk:num_rois*(jk+1),:],axis=0)
        if ROIs.shape[1] == 0:
            break

        if jk == R.shape[0]//num_rois:
            #pad R
            curr_shape = ROIs.shape
            target_shape = (curr_shape[0],num_rois,curr_shape[2])
            ROIs_padded = np.zeros(target_shape).astype(ROIs.dtype)
            ROIs_padded[:,:curr_shape[1],:] = ROIs
            ROIs_padded[0,curr_shape[1]:,:] = ROIs[0,0,:]
            ROIs = ROIs_padded

        [P_cls,P_regr] = model_classifier.predict([F, ROIs])
        print(P_cls)

        for ii in range(P_cls.shape[1]):

            if np.max(P_cls[0,ii,:]) < 0.6 or np.argmax(P_cls[0,ii,:]) == (P_cls.shape[2] - 1):
                continue

            cls_name = class_mapping[np.argmax(P_cls[0,ii,:])]

            if cls_name not in bboxes:
                bboxes[cls_name] = []
                probs[cls_name] = []
            (x,y,w,h) = ROIs[0,ii,:]

            bboxes[cls_name].append([16*x,16*y,16*(x+w),16*(y+h)])
            probs[cls_name].append(np.max(P_cls[0,ii,:]))

    
    all_dets = []

    for key in bboxes:
        # print(key)
        # print(len(bboxes[key]))
        bbox = np.array(bboxes[key])

        new_boxes, new_probs = roi_helpers.non_max_suppression_fast(bbox, np.array(probs[key]), overlap_thresh = 0.1)
        for jk in range(new_boxes.shape[0]):
            (x1, y1, x2, y2) = new_boxes[jk,:]
            (real_x1, real_y1, real_x2, real_y2) = get_real_coordinates(ratio, x1, y1, x2, y2)

            cv2.rectangle(img,(real_x1, real_y1), (real_x2, real_y2), (int(class_to_color[key][0]), int(class_to_color[key][1]), int(class_to_color[key][2])),2)

            textLabel = '{}: {}'.format(key,int(100*new_probs[jk]))
            all_dets.append((key,100*new_probs[jk]))

            (retval,baseLine) = cv2.getTextSize(textLabel,cv2.FONT_HERSHEY_COMPLEX,1,1)
            textOrg = (real_x1, real_y1-0)

            # cv2.rectangle(img, (textOrg[0] - 5, textOrg[1]+baseLine - 5), (textOrg[0]+retval[0] + 5, textOrg[1]-retval[1] - 5), (0, 0, 0), 2)
            # cv2.rectangle(img, (textOrg[0] - 5,textOrg[1]+baseLine - 5), (textOrg[0]+retval[0] + 5, textOrg[1]-retval[1] - 5), (255, 255, 255), -1)
            cv2.putText(img, textLabel, textOrg, cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 1)
    
    print('Elapsed time = {}'.format(time.time() - st))
    print(all_dets)
    print(bboxes)
    # enable if you want to show pics
    if write:
        if not os.path.isdir("app/static/Deployment/results"):
           os.mkdir("app/static/Deployment/results")
        cv2.imwrite(os.path.join('app/static/Deployment/results','{}'.format(img_name)),img)

# if __name__ == "__main__":
#     filepath = "111.jpg"
#     predict(filepath)