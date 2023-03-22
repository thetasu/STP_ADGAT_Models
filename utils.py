from torch import nn
import math
import random
import torch
import numpy as np
from sklearn.metrics import roc_auc_score
import os
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, matthews_corrcoef

def reset_parameters(named_parameters):
    for i in named_parameters():
        if len(i[1].size()) == 1:
            std = 1.0 / math.sqrt(i[1].size(0))
            nn.init.uniform_(i[1], -std, std)
        else:
            nn.init.xavier_normal_(i[1])

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def metrics(trues, preds):
    trues = np.concatenate(trues,-1)
    preds = np.concatenate(preds,0)
    # print('original preds:')
    # print(preds[0:20,:])
    # print('original preds:')
    # print(preds.argmax(-1)[0:20])
    pre_label = []
    for i in preds[:,1].tolist():
        if i>=0.5:
            pre_label.append(1)
        else:
            pre_label.append(0)
    '''
    pre_label = np.array(pre_label)
    tures_test = np.reshape(trues,(71,85))
    print('tures_test.shape:{}'.format(tures_test.shape))
    print(tures_test[-10:,0])
    print('pre_label.shape:{}'.format(pre_label.shape))
    print(pre_label[0:10])
    print('trues.shape:{}'.format(trues.shape))
    print(trues[0:10])
    print('preds.shape:{}'.format(preds.shape))
    print(preds[0:10,:])
    '''
    acc = sum(preds.argmax(-1) == trues) / len(trues)
    auc = roc_auc_score(trues,preds[:,1])
    # add f1, pre, rec, mcc evaluation metrics
    acc = accuracy_score(trues,pre_label)
    f1 = f1_score(trues,pre_label)
    pre = precision_score(trues,pre_label)
    rec = recall_score(trues,pre_label)
    mcc = matthews_corrcoef(trues,pre_label)
    # return acc, auc
    
    return acc, f1, pre, rec, auc, mcc,trues,pre_label

def createPath(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)


def files_name(path):
    filesname_list = []
    for i in range(len(path)):
        (filepath, tempfilename) = os.path.split(path[i])
        (filesname, extension) = os.path.splitext(tempfilename)
        filesname_list.append(filesname)
    # print("stock_id list:",filesname_list)
    return filesname_list

def dir_name(path):
    file_list = os.listdir(path)
    file_name_list = []
    for i in range(len(file_list)):
        file_name = path + '/' + file_list[i]
        # print(file_name)
        file_name_list.append(file_name)
    return file_name_list

def load_Dataset(dataset_name,DEVICE):
    if dataset_name == 'KDD17':
        data_path = './data/KDD17/preprocessed/'
    elif dataset_name == 'ACL18':
        data_path = './data/ACL18/preprocessed/'
    else:
        print('data path err')
    file_path = dir_name(data_path)
    stock_id_list = files_name(file_path)
    clear_stock_id_list = []
    for s in stock_id_list:
        if s not in ['AGFS', 'BABA', 'GMRE']:
            clear_stock_id_list.append(s)
    clear_stock_id_list.sort()
    print(clear_stock_id_list)
    for index, ticker in enumerate(clear_stock_id_list):
        if ticker not in ['AGFS', 'BABA', 'GMRE']:
            # print('index:{} ticker:{}'.format(index, ticker))
            single_eod_data = pd.read_csv(data_path + ticker + '.csv', header=None, delimiter=',').values
            if dataset_name == 'KDD17':
                label_data = single_eod_data[29:-1,-2]
                single_eod_data = single_eod_data[29:-1,:-2]
            elif dataset_name == 'ACL18':
                label_data = single_eod_data[148:,-2]
                single_eod_data = single_eod_data[148:,:-2]
            if ticker == clear_stock_id_list[0]:
                print('single EOD data shape:',single_eod_data.shape) # 2488,11
                print(single_eod_data)
                eod_data = np.zeros([len(clear_stock_id_list), single_eod_data.shape[0],
                                     single_eod_data.shape[1]], dtype=np.double)
                label_matrix = np.zeros([len(clear_stock_id_list),single_eod_data.shape[0]],dtype=np.long)
            eod_data[index,:,:] = single_eod_data[:,:]
            label_matrix[index,:] = label_data
    # err method, distory the data distribution
    # eod_data = eod_data.reshape([eod_data.shape[1], eod_data.shape[0], eod_data.shape[-1]])
    eod_data = eod_data.transpose((1,0,2))
    label_matrix = label_matrix.T

    x_sentiment = np.zeros([eod_data.shape[0],eod_data.shape[1],8])
    relation_message = None
    print('eod_data.shape:{}'.format(eod_data.shape))
    print('label_matrix.shape:{}'.format(label_matrix.shape))
    
    x = torch.tensor(eod_data, device=DEVICE)
    x.to(torch.double)
    x_s = torch.tensor(x_sentiment, device=DEVICE)
    x_s.to(torch.double)
    y = torch.tensor(label_matrix, device=DEVICE)
    y = (y>0).to(torch.long)
    return x,y,x_s,relation_message
'''
X,Labels,x_sentiment = load_Dataset('KDD17')
print(X[0:10,0,:])
print(Labels[0:10,0])
print('**************************************************************')
X,Labels,x_sentiment = load_Dataset('ACL18')
print(X[0:10,0,:])
print(Labels[0:10,0])'''
