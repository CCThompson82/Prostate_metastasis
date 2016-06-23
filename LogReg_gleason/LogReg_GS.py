from sklearn.linear_model import LogisticRegression


logisticDF = pd.DataFrame({'lda_decision': lda.decision_function(X_k),
                           'gleason': gleason,
                           #'age': age ,
                           #'psa' : psa,
                           }, index=X_k.index)

logisticDF_train = logisticDF.loc[X_train.index, :]
logisticDF_test = logisticDF.loc[X_test.index, :]


estimator = LogisticRegression(penalty='l2',
                              dual=False,
                              tol=0.0001,
                              C=1,
                              fit_intercept=True,
                              intercept_scaling=1,
                              class_weight={'n0':1, 'n1': 8},
                              random_state=123,
                              solver='liblinear',
                              max_iter=100,
                              multi_class='ovr',
                              verbose=0,
                              warm_start=False,
                              n_jobs=1)

clf = GridSearchCV(estimator,
                   param_grid = {'C': [1,0.1, 0.01, 0.001, 0.0001]},
                   scoring=fbeta_scorer,
                   fit_params=None,
                   n_jobs=1,
                   iid=True,
                   refit=True,
                   cv= 5,
                   verbose=0,
                   pre_dispatch='2*n_jobs',
                   error_score='raise')
clf.fit(logisticDF_train, y_train)
LR_clf = clf.best_estimator_
print(LR_clf)
print(classification_report(y_train,
                            LR_clf.predict(logisticDF_train),
                            target_names = ['n0', 'n1']))
print('\nF beta: ', fbeta_score(y_train, LR_clf.predict(logisticDF_train), beta = 2, pos_label='n1'))
print('\nMCC: ',matthews_corrcoef(y_train, LR_clf.predict(logisticDF_train)))
