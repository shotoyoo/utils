# python3: encoding utf-8
import itertools
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor, export_graphviz
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
import graphviz
from collections import OrderedDict
import pdb
def get_scores(model, args, X, y, testX, testy):
    # args : {name: [val1, val2,...],...}
    out = []
    models = []
    for param in itertools.product(*args.values()):
        a = OrderedDict({k:v for k,v in zip(args.keys(), param)})
        reg = model(**a)
        reg.fit(X, y)
        a["train"] = reg.score(X, y)
        a["test"] = reg.score(testX, testy)
        out.append(a)
        models.append(reg)
    df = pd.DataFrame(out)
    return df, models

if __name__=="__main__":
    df = pd.read_csv("test3.csv", encoding="cp932", header=0)
    X = pd.get_dummies(df.loc[:,"middle_area":"midnight"])
    y = df["score"]
    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=42)
    model = MLPRegressor
    params = OrderedDict({"hidden_layer_sizes": [(100,100)], "alpha":[1e-3, 1e-4, 1e-5], "learning_rate_init":[3e-2, 4e-2, 5e-2, 6e-2, 7e-2], "random_state":[0], "max_iter":[10000]})
    # params = OrderedDict({"n_estimators":[10, 100], "min_samples_split":[10,50,200], "max_features":["auto", 1, 5, 10], "random_state":[0]})
    df,models = get_scores(model, params, X_train, y_train, X_test, y_test)
    pdb.set_trace()
