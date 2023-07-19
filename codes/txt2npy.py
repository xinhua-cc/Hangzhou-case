import os
import numpy as np
import re
import tensorflow as tf
from sklearn.model_selection import train_test_split

def get_filenames(data_path):
    data_list = os.listdir(data_path) # 获取一个包含文件名的列表
    data_list.sort(key=lambda x: int(re.split('[._]', x)[-2])) # 对列表进行分割，按照序号进行升序排序
    name_list = []
    for m_name in data_list:
        name_list.append(os.path.join(data_path, m_name))
    return name_list


def read_files(input_list, label_list, sensi_path, para_name):
    inputs, labels = [], []
    x_train, x_test, y_train, y_test = [], [], [], []
    assert len(input_list) == len(label_list)
    data_len = len(label_list)
    print(data_len)
    # shuffle the orfer of input
    m_index = [i for i in range(data_len)]
    np.random.shuffle(m_index)
    input_list = np.array(input_list)
    label_list = np.array(label_list)
    input_list_1 = input_list[m_index]
    label_list_1 = label_list[m_index]
    
    m_input_sum1 = 0
    m_input_sum2 = 0
    m_input_max1 = 0
    m_input_max2 = 0
    m_input_min1 = 9999999999999
    m_input_min2 = 9999999999999
    
    sensis = np.loadtxt(sensi_path)

    for i in range(data_len):
        input_ = np.loadtxt(input_list_1[i])
        input_[:, 1] = input_[:, 1] * sensis
        m_input = input_.copy()
        m_input_sum1 = m_input_sum1 + sum(input_[:, 0])
        m_input_sum2 = m_input_sum2 + sum(input_[:, 1])
        
        t_max = max(input_[:, 0])
        if m_input_max1 < t_max:
            m_input_max1 = t_max.copy()        
        t_min = min(input_[:, 0])
        if m_input_min1 > t_min:
            m_input_min1 = t_min.copy() 
            
        t_max = max(input_[:, 1])
        if m_input_max2 < t_max:
            m_input_max2 = t_max.copy()         
        t_min = min(input_[:, 1])
        if m_input_min2 > t_min:
            m_input_min2 = t_min.copy() 
        
        label_ = np.loadtxt(label_list_1[i])

        inputs.append(m_input)
        labels.append(label_)
    m_input_mean1 = m_input_sum1 / (data_len * inputs[0].shape[0])
    m_input_mean2 = m_input_sum2 / (data_len * inputs[0].shape[0])
    m_input_diff1 = m_input_max1 - m_input_min1
    m_input_diff2 = m_input_max2 - m_input_min2
    data=open(para_name,'w+')
    print("this is mean1:", m_input_mean1, file = data)
    print("this is mean2:", m_input_mean2, file = data)
    print("this is max1:", m_input_max1, file = data)
    print("this is min1:", m_input_min1, file = data)
    print("this is max1-min1:", m_input_diff1, file = data)
    print("this is max2:", m_input_max2, file = data)
    print("this is min2:", m_input_min2, file = data)
    print("this is max2-min2:", m_input_diff2, file = data)
    data.close()

    for i in range(data_len):
        inputs[i][:, 0] = (inputs[i][:, 0] - m_input_min1) / (m_input_max1 - m_input_min1)
        inputs[i][:, 1] = (inputs[i][:, 1] - m_input_min2) / (m_input_max2 - m_input_min2)
        rem = i % 10
        if(rem == 1 or rem == 2):
            x_test.append(inputs[i])
            y_test.append(labels[i])
        else:
            x_train.append(inputs[i])
            y_train.append(labels[i])

    m_train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))  
    m_val_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)) 

    return m_train_dataset, m_val_dataset


def read_files_3(input_list, label_list, sensi_path, para_name):
    inputs, labels = [], []
    x_train, x_test, y_train, y_test = [], [], [], []
    assert len(input_list) == len(label_list)
    data_len = len(label_list)
    print(data_len)
    # shuffle the orfer of input
    m_index = [i for i in range(data_len)]
    np.random.shuffle(m_index)
    input_list = np.array(input_list)
    label_list = np.array(label_list)
    input_list_1 = input_list[m_index]
    label_list_1 = label_list[m_index]
    
    m_input_sum1 = 0
    m_input_sum2 = 0
    m_input_sum3 = 0
    m_input_max1 = 0
    m_input_max2 = 0
    m_input_max3 = 0
    m_input_min1 = 9999999999999
    m_input_min2 = 9999999999999
    m_input_min3 = 9999999999999
    
    sensis = np.loadtxt(sensi_path)

    for i in range(data_len):
        input_ = np.zeros((178, 3))
        re_fv = np.loadtxt(input_list_1[i])
        input_[:, 0:2] = re_fv.copy()
        input_[:, 2] = sensis.copy()
        m_input = input_.copy()
        m_input_sum1 = m_input_sum1 + sum(input_[:, 0])
        m_input_sum2 = m_input_sum2 + sum(input_[:, 1])
        m_input_sum3 = m_input_sum3 + sum(input_[:, 2])
        
        t_max = max(input_[:, 0])
        if m_input_max1 < t_max:
            m_input_max1 = t_max.copy()        
        t_min = min(input_[:, 0])
        if m_input_min1 > t_min:
            m_input_min1 = t_min.copy() 
            
        t_max = max(input_[:, 1])
        if m_input_max2 < t_max:
            m_input_max2 = t_max.copy()         
        t_min = min(input_[:, 1])
        if m_input_min2 > t_min:
            m_input_min2 = t_min.copy() 
            
        t_max = max(input_[:, 2])
        if m_input_max3 < t_max:
            m_input_max3 = t_max.copy()         
        t_min = min(input_[:, 2])
        if m_input_min3 > t_min:
            m_input_min3 = t_min.copy() 
        
        label_ = np.loadtxt(label_list_1[i])

        inputs.append(m_input)
        labels.append(label_)
    m_input_mean1 = m_input_sum1 / (data_len * inputs[0].shape[0])
    m_input_mean2 = m_input_sum2 / (data_len * inputs[0].shape[0])
    m_input_mean3 = m_input_sum3 / (data_len * inputs[0].shape[0])
    m_input_diff1 = m_input_max1 - m_input_min1
    m_input_diff2 = m_input_max2 - m_input_min2
    m_input_diff3 = m_input_max3 - m_input_min3
    data=open(para_name,'w+')
    print("this is mean1:", m_input_mean1, file = data)
    print("this is mean2:", m_input_mean2, file = data)
    print("this is mean3:", m_input_mean3, file = data)
    print("this is max1:", m_input_max1, file = data)
    print("this is min1:", m_input_min1, file = data)
    print("this is max1-min1:", m_input_diff1, file = data)
    print("this is max2:", m_input_max2, file = data)
    print("this is min2:", m_input_min2, file = data)
    print("this is max2-min2:", m_input_diff2, file = data)
    print("this is max3:", m_input_max3, file = data)
    print("this is min3:", m_input_min3, file = data)
    print("this is max3-min3:", m_input_diff3, file = data)
    data.close()

    for i in range(data_len):
        inputs[i][:, 0] = (inputs[i][:, 0] - m_input_min1) / m_input_diff1
        inputs[i][:, 1] = (inputs[i][:, 1] - m_input_min2) / m_input_diff2
        inputs[i][:, 2] = (inputs[i][:, 2] - m_input_min3) / m_input_diff3
        rem = i % 10
        if(rem == 1 or rem == 2):
            x_test.append(inputs[i])
            y_test.append(labels[i])
        else:
            x_train.append(inputs[i])
            y_train.append(labels[i])

    m_train_dataset = tf.data.Dataset.from_tensor_slices((x_train, y_train))  
    m_val_dataset = tf.data.Dataset.from_tensor_slices((x_test, y_test)) 

    return m_train_dataset, m_val_dataset