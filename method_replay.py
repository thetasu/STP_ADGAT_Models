import pickle
import numpy as np
import pandas as pd
import torch
from sklearn import metrics

with open('./data/x_numerical.pkl', 'rb') as handle:
    markets = pickle.load(handle)
    markets = np.reshape(markets,[markets.shape[1],markets.shape[0],markets.shape[-1]])
with open('./data/y_.pkl', 'rb') as handle:
    y_load = pickle.load(handle)

with open('./data/latest_x_numerical.pkl', 'rb') as handle:
    latest_markets = pickle.load(handle)
    latest_markets = np.reshape(latest_markets,[latest_markets.shape[1],latest_markets.shape[0],latest_markets.shape[-1]])
with open('./data/latest_y_numerical.pkl', 'rb') as handle:
    latest_y_load = pickle.load(handle)

# with open('./data/x_textual.pkl', 'rb') as handle:
#     stock_sentiments = pickle.load(handle)
y = torch.tensor(y_load)
y = (y > 0).to(torch.long)

y_new = torch.tensor(latest_y_load)
y_new = (y_new > 0).to(torch.long)
print(y==y_new)

print(markets.shape)
print(y_load.shape)
print(latest_markets.shape)
print(latest_y_load.shape)
print(y_load[-1,0:10])
print(latest_y_load[-1,0:10])

print(y_load==latest_y_load)
print((y_load[-1,0:10]==latest_y_load[-1,0:10]).all())
print(y[-1,0:10])
# print(y_load[0])
# print(y.shape)
# print(y[0])


# ground_truth = pd.read_csv('ground_truth_aastgcn_1day.csv')
# print(ground_truth.shape)
# print(ground_truth.values)
# prediction = pd.read_csv('prediction_aastgcn_1day.csv')
# print(prediction.shape)
# print(prediction.values)
# diff = prediction.values - ground_truth.values
# print(diff.shape)
# print(diff)
# y = torch.tensor(diff)
# y = (y > 0).to(torch.long).numpy()
# print(y.shape)
# print(y)
# np.savetxt('prediction_label.csv',y,delimiter=',')
# print('save success')

# ground_truth_label = pd.read_csv('ground_truth_label.csv').values.flatten()
# prediction_label = pd.read_csv('prediction_label.csv').values.flatten()
# print(ground_truth_label)
# print(prediction_label)
#
# acc = metrics.accuracy_score(ground_truth_label,prediction_label)
# print(acc)