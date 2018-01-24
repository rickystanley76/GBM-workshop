

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import metrics
import xgboost as xgb
import multiprocessing


d = pd.read_csv("../data/airline100K.csv")

vars_cat = ["Month","DayofMonth","DayOfWeek","UniqueCarrier", "Origin", "Dest"]
vars_num = ["DepTime","Distance"]
def my_get_dummies(d, col):
    dd = pd.get_dummies(d.ix[:, col])
    dd.columns = [col + "_%s" % c for c in dd.columns]
    return(dd)
    
X_cat = pd.concat([my_get_dummies(d, col) for col in vars_cat], axis = 1)
X = pd.concat([X_cat, d.ix[:,vars_num]], axis = 1)    
## TODO: training very slow, needs sparse representation!
      
y = np.where(d[["dep_delayed_15min"]]=="Y",1,0)[:,0]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=123)


n_c = multiprocessing.cpu_count()
n_c

## TRAIN
%time md = xgb.XGBClassifier(max_depth=10, n_estimators=100, learning_rate=0.1, n_jobs=n_c).fit(X_train, y_train)


## SCORE
y_pred = md.predict_proba(X_test)[:,1]

metrics.confusion_matrix(y_test, y_pred>0.5)

metrics.roc_auc_score(y_test, y_pred)

metrics.confusion_matrix(y_test, y_pred>0.7)
metrics.confusion_matrix(y_test, y_pred>0.6)
metrics.confusion_matrix(y_test, y_pred>0.5)


## try playing with the hyperparams e.g. max_depth = 2,5,10,15; learning_rate=0.01,0.03,0.1;
## n_estimators = 100,300,1000; check out further params in the docs
## (re-run from "TRAIN" part above)


