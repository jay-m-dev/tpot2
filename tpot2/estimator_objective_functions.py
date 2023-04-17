from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
import numpy as np
import time
import sklearn.metrics
import networkx as nx
from collections.abc import Iterable
import pandas as pd



def cross_val_score_objective(pipeline, X, y, scorers, cv, fold=None):
    #check if scores is not iterable
    if not isinstance(scorers, Iterable): 
        scorers = [scorers]
    scores = []
    if fold is None:
        for train_index, test_index in cv.split(X, y):
            this_fold_pipeline = sklearn.base.clone(pipeline)
            if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            else:
                X_train, X_test = X[train_index], X[test_index]

            if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            else:
                y_train, y_test = y[train_index], y[test_index]


            start = time.time()
            this_fold_pipeline.fit(X_train,y_train)
            duration = time.time() - start

            this_fold_scores = [sklearn.metrics.get_scorer(scorer)(this_fold_pipeline, X_test, y_test) for scorer in scorers] 
            scores.append(this_fold_scores)
            del this_fold_pipeline
            del X_train
            del X_test
            del y_train
            del y_test
            

        return np.mean(scores,0)
    else:
        this_fold_pipeline = sklearn.base.clone(pipeline)
        train_index, test_index = list(cv.split(X, y))[fold]
        if isinstance(X, pd.DataFrame) or isinstance(X, pd.Series):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        else:
            X_train, X_test = X[train_index], X[test_index]

        if isinstance(y, pd.DataFrame) or isinstance(y, pd.Series):
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        else:
            y_train, y_test = y[train_index], y[test_index]

        start = time.time()
        this_fold_pipeline.fit(X_train,y_train)
        duration = time.time() - start
        this_fold_scores = [sklearn.metrics.get_scorer(scorer)(this_fold_pipeline, X_test, y_test) for scorer in scorers] 
        return this_fold_scores




def number_of_nodes_objective(graph_pipeline):
    return graph_pipeline.graph.number_of_nodes()


def average_path_length_objective(graph_pipeline):

    path_lengths =  nx.shortest_path_length(graph_pipeline.graph, source=graph_pipeline.root)
    return np.mean(np.array(list(path_lengths.values())))+1

