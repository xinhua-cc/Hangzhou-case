import tensorflow as tf
import numpy as np
import os
import argparse
from network import model_178
import datasetloader as dl
from txt2npy import read_files


parser = argparse.ArgumentParser()
parser.add_argument("--epoch", default=10000000)
parser.add_argument("--batch_size", default=128)
parser.add_argument("--ratio", default=0.2)
parser.add_argument("--traininput_dir", default="/data/Hangzhou/data/train_input_4/")
parser.add_argument("--trainlabel_dir", default="/data/Hangzhou/data/train_label_4/")
parser.add_argument("--sensi_input_dir", default="/data/Hangzhou/data/sensi/sensi_fre_inv.txt")
parser.add_argument("--sensi_loss_dir", default="/data/Hangzhou/data/sensi/sensi_layer.txt")
parser.add_argument("--cpt_dir", default="./checkpoint_freinv_layer")
parser.add_argument("--callbacks_dir", default="./callbacks_freinv_layer")
parser.add_argument("--parameter_name", default="parameters_freinv_layer.txt")
opt = parser.parse_args()

# 1. single
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
print(gpus)
tf.config.experimental.set_visible_devices(devices=gpus[0], device_type='GPU')
strategy = tf.distribute.MirroredStrategy()
# 2. multiple
# gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
# print(gpus)
# strategy = tf.distribute.MirroredStrategy(["GPU:0", "GPU:1", "GPU:2"])
#******************************************************************************
# read sensi
m_sensi = np.loadtxt(opt.sensi_loss_dir)


m_batch_size = opt.batch_size * strategy.num_replicas_in_sync
# m_batch_size = opt.batch_size
# def scheduler(epoch):
#     return 0.0001
    # elif 3000 < epoch <= 10000:
    #  	return 0.001

def scheduler(epoch):
    if epoch <= 100000:
        return 0.001

def cc_loss_1(y_true, y_cal): # default label in front
    CCCC = np.arange(12)
    cc_loss = 100000 * 0.5 * tf.reduce_mean(tf.square((y_true - y_cal) / y_true) * (1 + CCCC))
    return cc_loss
def cc_loss_2(y_true, y_cal): # default label in front
    ccc = m_sensi
    cc_loss = 0.5 * tf.reduce_mean(ccc * tf.square(y_true - y_cal))
    return cc_loss

Exists1 = os.path.exists(opt.cpt_dir)
if not Exists1:
    os.makedirs(opt.cpt_dir)

Exists2 = os.path.exists(opt.callbacks_dir)
if not Exists2:
    os.makedirs(opt.callbacks_dir)


traininput_filenames = dl.get_filenames(opt.traininput_dir)
trainlabel_filenames = dl.get_filenames(opt.trainlabel_dir)


dl.cc_train_dataset, dl.cc_val_dataset = read_files(traininput_filenames, trainlabel_filenames, opt.sensi_input_dir, opt.parameter_name)
print("load all_data success !!!!!!!!!")

m_shuffer_2 = int(len(traininput_filenames) * opt.ratio)
m_shuffer_1 = int(len(traininput_filenames) * (1 - opt.ratio))
train_dataset, val_dataset = dl.datasetflow_reader(batch_size=m_batch_size, shuffer_1=m_shuffer_1, shuffer_2=m_shuffer_2)

checkpoint_prefix = os.path.join(opt.cpt_dir, "weights.{epoch:02d}-{loss:.5f}.h5")

'''
if os.path.exists(opt.opt_dir + 'variables' + 'variables.index'):
    print('------------------load weights-------------------')
    model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))
'''

callbacks = [
    tf.keras.callbacks.LearningRateScheduler(scheduler),
    tf.keras.callbacks.TensorBoard(opt.callbacks_dir),
    tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix,
                                       monitor='loss', # applied for quit the training process
                                       save_wights_only=True, save_best_only=False, save_freq = 10 * m_batch_size,
                                       verbose=1)
    ]

# 1. single
m_model = model_178()
# m_model.load_weights("weights.27000.h5")
m_model.compile(optimizer=tf.keras.optimizers.Adam(),
                loss=cc_loss_2)
# loss=tf.keras.losses.mean_squared_error
# loss=cc_loss_2
m_model.fit(train_dataset, validation_data=val_dataset, epochs=opt.epoch, callbacks=callbacks,
                validation_freq=10)

#2. multiple
# with strategy.scope():
#     m_model = model_178()
    
#     # m_model.load_weights("/home/xhc/hefei_network/checkpoint_1/weights.9040-1.21131.h5")
    
    
#     m_model.compile(optimizer=tf.keras.optimizers.Adam(),
#               loss=cc_loss_3)
    
#     m_model.fit(train_dataset, validation_data=val_dataset, epochs=opt.epoch, callbacks=callbacks,
#                 validation_freq=10)
