# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import tensorflow as tf
import numpy as np
import glob
import sys
from models import *
import yaml
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import utils

####### Reading Hyperparameters #####
with open("config.yaml") as file:
	data = yaml.load(file)
	training_params = data['training_params']
	learning_rate = float(training_params['learning_rate'])
	batch_size = int(training_params['batch_size'])
	epoch_size = int(training_params['epochs'])
	data_path = training_params['data_path']
	model_params= data['model_params']
	descrip = model_params['descrip']
	log_dir = model_params['log_dir']
	mode = model_params['mode']
	if len(descrip)==0:
		raise ValueError, "Please give a proper description of the model you are training."
	print "Model description:", descrip

######## Making Directory #########
model_path = log_dir+sys.argv[1]
print "Model Path: ", model_path
if not os.path.exists(model_path):
	os.makedirs(model_path)
	os.makedirs(model_path+"/results")
	os.makedirs(model_path+"/tf_graph")
	os.makedirs(model_path+"/saved_model")


######### Loading Data ###########
train_img1 = np.load(data_path+"train_haze_clear.npy") # First image of each pair is hazy image and second image is clear images
# train_img2 = 1/255.0*np.load(data_path+"train_trans.npy") 
val_img1 = np.load(data_path+"val_haze_clear.npy")
# val_img2 = 1/255.0*np.load(data_path+"val_trans.npy")	   

print train_img1.min(), train_img1.max()

train_img1 = train_img1.astype(float)/127.5 - 1.0
val_img1 = val_img1.astype(float)/127.5 - 1.0
print train_img1.min(), train_img1.max()

print "Data Loaded"

nnet = pix2pix(model_path)
if mode=='train':
	os.system('cp config.yaml '+model_path+'/config.yaml')
	os.system('cp models.py '+model_path+'/model.py')
	nnet.build_model()
	print "Model Build......"
	# nnet.train_model([train_img1, train_img2],[val_img1,val_img2] , learning_rate, batch_size, epoch_size)
	nnet.train_model(train_img1[:4000] , val_img1[:500], learning_rate, batch_size, epoch_size)
else:
	print model_path
	predict_clear= nnet.test(val_img1[:,0,:,:,:], batch_size)
	# predict_clear= nnet.test(batch_size)
	for i in range(val_img1.shape[0]):
		pair2 = np.hstack((val_img1[i,0,:,:,:],val_img1[i,1,:,:,:], predict_clear[i]))
		cv2.imwrite(model_path+"/results/val/"+str(i)+"_clear.jpg", 255.0*pair2)
