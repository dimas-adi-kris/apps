# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:18:45 2020

@author: naufa
"""

import numpy as np
import scipy.io
from wfdb.processing import normalize_bound
import wfdb
import xmltodict
from keras.models import load_model
from statsmodels.robust import mad
import sys
import pywt

def denoising(feature):
    levels = 8            
    a = feature
    w = pywt.Wavelet('sym5')
    ca = []
    cd = []
    
    for level in range(levels):
        (a, d) = pywt.dwt(a, w)
        ca.append(a)
        cd.append(d)
    a = [0] * len(a)
    a = np.array(a)
    cd.append(a)
        
    sigma = mad( cd[0] )
    uthresh = sigma * np.sqrt( 2*np.log( len(feature)))
        
    new_cd = []
    for d in cd:
        new_cd.append(pywt.threshold(d, value=uthresh, mode="soft"))
    new_cd.reverse()
    new_signal = pywt.waverec(new_cd, w)
    return new_signal

def utama(filename):
    path_data = filename
    path_model = "models/AF/Best Model 3 Classes.h5"
    ext = path_data.split(".")[-1]

    if ext == 'xml':
        with open(path_data) as fopen:
            file = fopen.read()    
        data = xmltodict.parse(file, encoding='latin-1')
        raw = data['CardioXP']['StudyInfo']['WaveData'][1]['Data']
        signal = raw.split(' ')
        signal = np.array(signal, dtype = int)
        signal = normalize_bound(signal, lb=0, ub=1)
        signal = denoising(signal)
        signal = signal[0:2700]
    elif ext == 'dat':
        record = wfdb.rdrecord(path_data)
        record_dict = record.__dict__    
        p_signal = record_dict['p_signal'][:,0]
        p_signal = normalize_bound(p_signal, lb=0, ub=1)
        p_signal = denoising(p_signal)
        signal = p_signal[0:2700]
    elif ext == 'mat':
        data = scipy.io.loadmat(path_data)
        sampels = data['val'][0]
        sampels = normalize_bound(sampels, lb = 0, ub = 1)
        sampels = denoising(sampels)
        signal = sampels[0:2700]
    else:    
        sys.exit("Not A Valid Data")

    if len(signal) < 2700:
        sys.exit("Signal length is not sufficient")

    signal = np.reshape(signal, (1,2700,1))
    model = load_model(path_model)
    predicted_class = model.predict_classes(signal)[0]

    if predicted_class == 0:
        print("Normal")
        return 'Normal'
    elif predicted_class == 1:
        print("Atrial Fibrilation")
        return 'Atrial Fibrilation'
    else:
        print("Non AF")
        return 'Non AF'
