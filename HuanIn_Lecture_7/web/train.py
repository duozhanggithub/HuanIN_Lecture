import numpy as np
from sklearn import linear_model
from sklearn.svm import SVR
import pickle

with open('./RSSI.csv', 'rb') as csvfile:
    data = np.loadtxt(csvfile, delimiter=',')

x = data[:, 0].reshape(-1,1)
y = data[:, 1]

our_model = SVR()
our_model.fit(x,y)

# use pickle to dumo the trained model as a pickle file
pickle.dump(our_model, open('model.pkl', 'wb'))
