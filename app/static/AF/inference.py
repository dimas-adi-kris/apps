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

from keras.backend import clear_session

import matplotlib.pyplot as plt
from datetime import datetime
timenow = datetime.now().strftime("%d%m%Y-%H%M%S")

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
    global timenow
    path_data = filename
    path_model = "Best Model 3 Classes.h5"
    ext = path_data.split(".")[-1]
    namefile = path_data.split('/')[4].split('.')[0]
    print(filename,ext,namefile)

    if ext == 'xml':
        with open(path_data) as fopen:
            file = fopen.read()    
        data = xmltodict.parse(file, encoding='latin-1')
        raw = data['CardioXP']['StudyInfo']['WaveData'][1]['Data']
        signal = raw.split(' ')
        signal = np.array(signal, dtype = int)
        
        plt.figure(figsize=(15,10))
        plt.plot(range(2700),signal[:2700])
        saving_file_bef = './app/static/AF/'+namefile+'-'+timenow+'-bef.png'
        plt.savefig(saving_file_bef)
        
        signal = normalize_bound(signal, lb=0, ub=1)
        signal = denoising(signal)
        signal = signal[0:2700]
        
        plt.figure(figsize=(15,10))
        plt.plot(range(2700),signal[:2700])
        saving_file_aft = './app/static/AF/'+namefile+'-'+timenow+'-aft.png'
        plt.savefig(saving_file_aft)
    elif ext == 'dat':
        record = wfdb.rdrecord(path_data)
        record_dict = record.__dict__    
        p_signal = record_dict['p_signal'][:,0]
        
        plt.figure(figsize=(15,10))
        plt.plot(range(2700),p_signal[:2700])
        saving_file_bef = './app/static/AF/'+namefile+'-'+timenow+'-bef.png'
        plt.savefig(saving_file_bef)
        
        p_signal = normalize_bound(p_signal, lb=0, ub=1)
        p_signal = denoising(p_signal)
        signal = p_signal[0:2700]
        
        plt.figure(figsize=(15,10))
        plt.plot(range(2700),signal[:2700])
        saving_file_aft = './app/static/AF/'+namefile+'-'+timenow+'-aft.png'
        plt.savefig(saving_file_aft)
    elif ext == 'mat':
        data = scipy.io.loadmat(path_data)
        sampels = data['val'][0]
        
        plt.figure(figsize=(15,10))
        plt.plot(range(2700),sampels[:2700])
        saving_file_bef = './app/static/AF/'+namefile+'-'+timenow+'-bef.png'
        plt.savefig(saving_file_bef)
        
        sampels = normalize_bound(sampels, lb = 0, ub = 1)
        sampels = denoising(sampels)
        signal = sampels[0:2700]
        
        plt.figure(figsize=(15,10))
        plt.plot(range(2700),signal[:2700])
        saving_file_aft = './app/static/AF/'+namefile+'-'+timenow+'-aft.png'
        plt.savefig(saving_file_aft)
    else:    
        sys.exit("Not A Valid Data")

    if len(signal) < 2700:
        sys.exit("Signal length is not sufficient")

    signal = np.reshape(signal, (1,2700,1))
    model = load_model(path_model)
    predicted_class = model.predict_classes(signal)[0]

    if predicted_class == 0:
        clear_session()
        print("Normal")
        return 'Normal',namefile+'-'+timenow
    elif predicted_class == 1:
        clear_session()
        print("Atrial Fibrilation")
        return 'Atrial Fibrilation',namefile+'-'+timenow
    else:
        clear_session()
        print("Non AF")
        return 'Non AF',namefile+'-'+timenow

