from Model import *
from utils import *
import pickle
import torch
from torch import optim
import argparse
import datetime
import numpy as np
parser = argparse.ArgumentParser()

parser.add_argument('--task', type=int, default='1',
                    help='0 Regression. 1 Classification')
parser.add_argument('--grid-search', type=int, default='0',
                    help='0 False. 1 True')
parser.add_argument('--soft-training', type=int, default='0',
                    help='0 False. 1 True')
parser.add_argument('--sample-discrimination', type=int, default='0',
                    help='0 False. 1 True')
parser.add_argument('--optim', type=int, default='1',
                    help='0 SGD. 1 Adam')
parser.add_argument('--eval', type=int, default='1',
                    help='if set the last day as eval')
parser.add_argument('--max-epoch', type=int, default='300',
                    help='Training max epoch')
parser.add_argument('--wait-epoch', type=int, default='30',
                    help='Training min epoch')
parser.add_argument('--eta', type=float, default='1e-4',
                    help='Early stopping')
parser.add_argument('--lr', type=float, default='5e-4',
                    help='Learning rate ')
parser.add_argument('--device', type=str, default='2',
                    help='GPU to use')
parser.add_argument('--heads-att', type=int, default='6',
                    help='attention heads')
parser.add_argument('--hidn-att', type=int, default='60',
                    help='attention hidden nodes')
parser.add_argument('--hidn-rnn', type=int, default='360',
                    help='rnn hidden nodes')
parser.add_argument('--weight-constraint', type=float, default='0',
                    help='L2 weight constraint')
parser.add_argument('--rnn-length', type=int, default='2',
                    help='rnn length')
parser.add_argument('--dropout', type=float, default='0.2',
                    help='dropout rate')
parser.add_argument('--clip', type=float, default='0.25',
                    help='rnn clip')
parser.add_argument('--infer', type=float, default='1',
                    help='if infer relation')
parser.add_argument('--relation', type=str, default='None',
                    help='all, competitor, customer, industry, stratigic, supply')
parser.add_argument('--save', type=bool, default=True,
                    help='save model')
parser.add_argument('--dataset_name', type=str, default='KDD17',
                    help='dataset name ACL18 or KDD17')

def load_dataset(DEVICE):
    with open('./data/x_numerical.pkl', 'rb') as handle:
        markets = pickle.load(handle)
    with open('./data/y_.pkl', 'rb') as handle:
        y_load = pickle.load(handle)
    with open('./data/x_textual.pkl', 'rb') as handle:
        stock_sentiments = pickle.load(handle)

    markets = markets.astype(np.float64)
    x = torch.tensor(markets, device=DEVICE)
    x.to(torch.double)
    x_sentiment = torch.tensor(stock_sentiments, device=DEVICE)
    x_sentiment.to(torch.double)
    if args.relation != "None":
        with open('./relations/' + args.relation + '_relation.pkl', 'rb') as handle:
            relation_static = pickle.load(handle)
        relation_static = torch.tensor(relation_static, device=DEVICE)
        relation_static.to(torch.double)
    else:
        relation_static = None
    y = torch.tensor(y_load, device=DEVICE)
    y = (y>0).to(torch.long)

    return x, y, x_sentiment, relation_static

def train(model, x_train, x_sentiment_train, y_train, relation_static = None):
    model.train()
    seq_len = len(x_train)
    train_seq = list(range(seq_len))[rnn_length:]
    random.shuffle(train_seq)
    total_loss = 0
    total_loss_count = 0
    batch_train = 15
    for i in train_seq:
        output = model(x_train[i - rnn_length + 1: i + 1], x_sentiment_train[i - rnn_length + 1: i + 1],  relation_static = relation_static)
        loss = criterion(output, y_train[i])
        loss.backward()
        total_loss += loss.item()
        total_loss_count += 1
        if total_loss_count % batch_train == batch_train - 1:
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.clip)
            optimizer.step()
            optimizer.zero_grad()
    if total_loss_count % batch_train != batch_train - 1:
        torch.nn.utils.clip_grad_norm_(model.parameters(), args.clip)
        optimizer.step()
    return total_loss / total_loss_count

def evaluate(model, x_eval, x_sentiment_eval, y_eval, relation_static = None):
    model.eval()
    seq_len = len(x_eval)
    seq = list(range(seq_len))[rnn_length:]
    preds = []
    trues = []
    for i in seq:
        output = model(x_eval[i - rnn_length + 1: i + 1], x_sentiment_eval[i - rnn_length + 1: i + 1], relation_static = relation_static)
        output = output.detach().cpu()
        preds.append(np.exp(output.numpy()))
        trues.append(y_eval[i].cpu().numpy())
    # acc, auc = metrics(trues, preds)
    acc, f1, pre, rec, auc, mcc, trues_label, preds_label = metrics(trues, preds)
    # return acc,  auc
    return acc, f1, pre, rec, auc, mcc, trues_label, preds_label


if __name__=="__main__":
    args = parser.parse_args()
    DEVICE = "cuda:" + args.device
    criterion = torch.nn.NLLLoss()
    # do not set seed
    # set_seed(1017)
    if args.relation != "None":
        static = 1
        pass
    else:
        static = 0
        relation_static = None
    # load dataset
    print("loading dataset")
    # ADGAT 
    # x, y, x_sentiment, relation_static = load_dataset(DEVICE)
    # ACL18
    x, y, x_sentiment, relation_static = load_Dataset(args.dataset_name,DEVICE)
    
    print('x.shape:{}'.format(x.shape))
    print('y.shape:{}'.format(y.shape))
    print('x_sentiment.shape:{}'.format(x_sentiment.shape))
    # print('relation_static.shape:{}'.format(relation_static.shape))
    # hyper-parameters
    NUM_STOCK = x.size(1)
    D_MARKET = x.size(2)
    D_NEWS = x_sentiment.size(2)
    MAX_EPOCH =  args.max_epoch
    infer = args.infer
    hidn_rnn = args.hidn_rnn
    heads_att = args.heads_att
    hidn_att= args.hidn_att
    lr = args.lr
    rnn_length = args.rnn_length
    t_mix = 1
    # ADGAT train-test split
    if args.dataset_name == 'ACL18':
        sp1 = int(x.shape[0] * 0.6)
        sp2 = int(x.shape[0] * 0.8)
    elif args.dataset_name == 'KDD17':
        sp1 = 2014
        sp2 = 2266
    else:
        sp1 = 590
        sp2 = 660
    x_train = x[:sp1,:,:]
    x_eval = x[sp1:sp2,:,:]
    x_test = x[sp2:,:,:]
    
    y_train = y[:sp1,:]
    y_eval = y[sp1:sp2,:]
    y_test = y[sp2:,:]
    x_sentiment_train = x_sentiment[:sp1,:,:]
    x_sentiment_eval = x_sentiment[sp1:sp2,:]
    x_sentiment_test = x_sentiment[sp2:,:,:]
    '''
    x_train = x[: -140]
    x_eval = x[-140 - rnn_length : -70]
    x_test = x[-70 - rnn_length:]

    y_train = y[: -140]
    y_eval = y[-140 - rnn_length : -70]
    y_test = y[-70 - rnn_length:]
    x_sentiment_train = x_sentiment[: -140]
    x_sentiment_eval = x_sentiment[-140 - rnn_length : -70]
    x_sentiment_test = x_sentiment[-70 - rnn_length:]
    '''    
    # initialize
    best_model_file = 0
    epoch = 0
    wait_epoch = 0
    eval_epoch_best = 0
    best_predicted = []
    model = AD_GAT(num_stock=NUM_STOCK, d_market = D_MARKET,d_news= D_NEWS,
                      d_hidden = D_MARKET, hidn_rnn = hidn_rnn, heads_att = heads_att,
                      hidn_att= hidn_att, dropout = args.dropout,t_mix = t_mix,
                      infer = infer, relation_static = static)
    model.cuda(device=DEVICE)
    model.to(torch.double)
    optimizer = optim.Adam(model.parameters(), lr= args.lr, weight_decay=args.weight_constraint)
    #train
    while epoch < MAX_EPOCH:
        train_loss = train(model, x_train,x_sentiment_train, y_train, relation_static = relation_static)
        # eval_acc, eval_auc = evaluate(model, x_eval, x_sentiment_eval, y_eval, relation_static = relation_static)
        # test_acc, test_auc = evaluate(model, x_test, x_sentiment_test, y_test, relation_static = relation_static)
        
        eval_acc, eval_f1, eval_pre, eval_rec, eval_auc, eval_mcc, eval_true, eval_predicted = evaluate(model, x_eval, x_sentiment_eval, y_eval, relation_static = relation_static)
        print('*******************test****************')
        test_acc, test_f1, test_pre, test_rec, test_auc, test_mcc, test_true, test_predicted = evaluate(model, x_test, x_sentiment_test, y_test, relation_static = relation_static)
        
        # eval_str = "epoch{}, train_loss{:.4f}, eval_auc{:.4f}, eval_acc{:.4f}, test_auc{:.4f},test_acc{:.4f}".format(epoch, train_loss, eval_auc, eval_acc, test_auc, test_acc)
        eval_str = " {} epoch:{}, train_loss:{:.4f}, eval_auc:{:.4f}, eval_acc:{:.4f}, test_acc:{:.4f},test_f1:{:.4f},test_pre:{:.4f},test_rec:{:.4f},test_auc:{:.4f},test_mcc:{:.4f}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),epoch, train_loss, eval_auc, eval_acc, test_acc, test_f1, test_pre, test_rec, test_auc, test_mcc)
        print(eval_str)

        # if eval_auc > eval_epoch_best:
        if eval_auc > eval_epoch_best:
            # save best predicted results
            best_predicted = test_predicted
            np_best_predicted = np.array(best_predicted)
            # ACL18
            # save_best_predicted = np.reshape(np_best_predicted,(92,85))
            # KDD17
            save_best_predicted = np.reshape(np_best_predicted,(219,50))
            print('save_best_predited:')
            print(save_best_predicted)
            np_true_label = np.array(test_true)
            # ACL18
            # save_true_label = np.reshape(np_true_label,(92,85))
            # KDD17
            save_true_label = np.reshape(np_true_label,(219,50))
            np.savetxt('grounf_truth.csv',save_true_label,delimiter=',')
            print('ground_truth save success')
            np.savetxt('predicted.csv',save_best_predicted,delimiter=',')
            print('predicted results save success')
            # eval_epoch_best = eval_auc
            eval_epoch_best = eval_auc
            # eval_best_str = "epoch{}, train_loss{:.4f}, eval_auc{:.4f}, eval_acc{:.4f}, test_auc{:.4f},test_acc{:.4f}".format(epoch, train_loss, eval_auc,eval_acc, test_auc, test_acc)
            eval_best_str = " {} epoch:{}, train_loss:{:.4f}, eval_auc:{:.4f}, eval_acc:{:.4f}, test_acc:{:.4f},test_f1:{:.4f},test_pre:{:.4f},test_rec:{:.4f},test_auc:{:.4f},test_mcc:{:.4f}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),epoch, train_loss, eval_auc, eval_acc, test_acc, test_f1, test_pre, test_rec, test_auc, test_mcc)
            wait_epoch = 0
            if args.save:
                if best_model_file:
                    os.remove(best_model_file)
                best_model_file = "./SaveModels/eval:auc{}_acc{}_test:auc{}_acc{}".format(eval_auc, eval_acc, test_auc, test_acc)
                # best_model_file = "./SaveModels/eval_epoch{}.pth".format(epoch)
                torch.save(model.state_dict(), best_model_file)
        else:
            wait_epoch += 1

        if wait_epoch > 10:
            print("saved_model_result:",eval_best_str)
            '''
            np_best_predicted = np.array(best_predicted)
            save_best_predicted = np.reshape(np_best_predicted,(71,85))
            np.savetxt('predicted.csv',save_best_predicted,delimiter=',')
            print('save success')
            '''
            break
        epoch += 1
