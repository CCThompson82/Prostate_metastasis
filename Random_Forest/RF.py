from sklearn.ensemble import RandomForestClassifier

estimator = RandomForestClassifier(n_estimators=50,
                                   criterion='gini',
                                   max_depth=3,
                                   min_samples_split=75,
                                   min_samples_leaf=20,
                                   min_weight_fraction_leaf=0.0,
                                   max_features='auto',
                                   max_leaf_nodes=None,
                                   bootstrap=True,
                                   oob_score=True,
                                   n_jobs=1,
                                   random_state=123,
                                   verbose=0,
                                   warm_start=False,
                                   class_weight='balanced')
clf = GridSearchCV(estimator,
                   param_grid = {},
                   scoring=fbeta_scorer,
                   fit_params=None,
                   n_jobs=1,
                   iid=True,
                   refit=True,
                   cv= 5,
                   verbose=0,
                   pre_dispatch='2*n_jobs',
                   error_score='raise')

clf.fit(X_k.loc[X_train.index], y_train)
print(clf.best_estimator_)
print('\n',classification_report(y_train,
                            clf.predict(X_k.loc[X_train.index]),
                            target_names = ['n0', 'n1']))
RF_clf = clf.best_estimator_
print('\nF beta: ', fbeta_score(y_train, RF_clf.predict(X_k.loc[X_train.index]), beta = 2, pos_label='n1'))
print('\nMCC: ',matthews_corrcoef(y_train, RF_clf.predict(X_k.loc[X_train.index])))
