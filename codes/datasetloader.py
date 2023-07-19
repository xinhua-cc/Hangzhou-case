import numpy as np
import os
import tensorflow as tf
import re

cc_train_dataset = 1
cc_val_dataset = 1

def get_filenames(data_dir):
    data_list = os.listdir(data_dir)                            # 获取一个包含文件名的列表
    data_list.sort(key=lambda x: int(re.split('[._]', x)[-2]))  # 对列表进行分割，按照序号进行升序排序
    name_list = []
    for example in data_list:
        name_list.append(os.path.join(data_dir, example))

    return name_list


def datasetflow_reader(batch_size=128, shuffer_1=10000, shuffer_2=3000):
    # n_readers:并行程度；n_parse_threads: 解析时候的并行程度；shuffer_buffer_size：shuFFer时buffer的大小
    # print(dataset)      
    cc_1 = cc_train_dataset.shuffle(shuffer_1).batch(batch_size)
    cc_2 = cc_val_dataset.shuffle(shuffer_2).batch(batch_size)
    # dataset = dataset.batch(batch_size)
    return cc_1, cc_2

# if __name__ == '__main__':
#     input_dir = "/home/xinhua/data/v12_samef_source/train_input_1/"
#     label_dir =  "G:\\inversion based on machine learning\\data\\2-2\\train_label\\6924.txt"
#     x, y = single_reader(input_dir, label_dir)
