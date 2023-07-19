import numpy as np
import tensorflow as tf
# import matplotlib.pyplot as plt
# import scipy.io as sio
import os
from network import model_178
# import re
# from sklearn.model_selection import train_test_split



input_dir = "H:\\Hangzhou_Fengqi_case\\figures\\fig7\\fvinterp\\"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_fre/weights.311-4400.59180.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_fre_layer/weights.153-586.01434.h5"
weights_dir = "H:\\Hangzhou_Fengqi_case\\experiment\\case\\weights.149-566.96667.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_layerinv/weights.202-12998.42676.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_raw/weights.90-4427.67432.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_freinv/weights.99-4355.18945.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_freinv_layer/weights.131-577.89191.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_freinv_layer_3/weights.119-578.39325.h5"
# weights_dir = "/data/Hangzhou/network_compare_sensiway/checkpoint_freinv_3/weights.109-4355.25244.h5"
test_dir = "H:\\Hangzhou_Fengqi_case\\figures\\fig7\\CNNresult\\"
sensi_dir = "H:\\Hangzhou_Fengqi_case\\experiment\\case\\sensi_all_1.txt"
m_num = 3

m_sensi = np.loadtxt(sensi_dir)
def get_filenames(data_path):
    data_list = os.listdir(data_path) # 获取一个包含文件名的列表
    name_list = []
    for m_name in data_list:
        name_list.append(os.path.join(data_path, m_name))
    return name_list

model = model_178()
model.load_weights(weights_dir)
Exists = os.path.exists(test_dir)
if not Exists:
    os.makedirs(test_dir)


for i in range(m_num):
    fv = []
    name = str(i + 1)
    input_ = np.loadtxt(input_dir + name+ '.txt')
    input_[:, 1] = input_[:, 1] * m_sensi
    input_18 = input_.copy()
    input_18[:, 0] = (input_[:, 0] - 1.8) / 17.7
    input_18[:, 1] = (input_[:, 1] - 150.010299) / 485.1424569999999
    fv.append(input_18)
    fv = np.expand_dims(fv, -1)
    pre_18 = model.predict(fv)
    pre_18 = tf.squeeze(pre_18)
    np.savetxt(test_dir + "pre_" + name + ".txt", pre_18, fmt = '%s')

# for 3 channels
# sensis = np.loadtxt(sensi_dir)
# for i in range(m_num):
#     fv = []
#     name = str(i + 1)
#     input_ = np.zeros((178, 3))
#     re_fv = np.loadtxt(input_dir + name+ '.txt')
#     input_[:, 0:2] = re_fv.copy()
#     input_[:, 2] = sensis.copy()

#     input_18 = input_.copy()
#     input_18[:, 0] = (input_[:, 0] - 1.8) / 17.7
#     input_18[:, 1] = (input_[:, 1] - 150.010299) / 485.1424569999999
#     input_18[:, 2] = (input_[:, 2] - 8.465227) / 13.314807
#     fv.append(input_18)
#     fv = np.expand_dims(fv, -1)
#     pre_18 = model.predict(fv)
#     pre_18 = tf.squeeze(pre_18)
#     np.savetxt(test_dir + "pre_" + name + ".txt", pre_18, fmt = '%s')
        

print("-------predict success-----")

# predict 1.txt
# fv = []
# # input_ = np.loadtxt('/home/xhc/data/test_data/result/1_fv.txt')
# input_ = np.loadtxt(input_dir+'1.txt')
# input_18 = input_
# input_18[:, 0] = (input_[:, 0] - 1.6) / 5.4
# input_18[:, 1] = (input_[:, 1] - 104.896813) / 2302.487563
# fv.append(input_18)
# fv = np.expand_dims(fv, -1)
# pre_18 = model.predict(fv)
# pre_18 = tf.squeeze(pre_18)

# # predict 2.txt
# fv = []
# input_ = np.loadtxt(input_dir+'2.txt')
# input_69 = input_
# input_69[:, 0] = (input_[:, 0] - 1.6) / 5.4
# input_69[:, 1] = (input_[:, 1] - 104.896813) / 2302.487563
# fv.append(input_69)
# fv = np.expand_dims(fv, -1)
# pre_69 = model.predict(fv)
# pre_69 = tf.squeeze(pre_69)

# print("-------predict success-----")

# # save predictions
# np.savetxt(test_dir + "pre_1.txt", pre_18, fmt = '%s')
# np.savetxt(test_dir + "pre_2.txt", pre_69, fmt = '%s')
