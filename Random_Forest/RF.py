from sklearn.ensemble import RandomForestClassifier

estimator = RandomForestClassifier(n_estimators=200,
                                   criterion='gini',
                                   max_depth=2,
                                   min_samples_split=50,
                                   min_samples_leaf=10,
                                   min_weight_fraction_leaf=0.0,
                                   max_features='auto',
                                   max_leaf_nodes=None,
                                   bootstrap=True,
                                   oob_score=False,
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

clf.fit(X_train, y_train)
print(clf.best_estimator_)
print('\n',classification_report(y_train,
                            clf.predict(X_train),
                            target_names = ['n0', 'n1']))
RF_clf = clf.best_estimator_
print('\nF beta: ', fbeta_score(y_train, RF_clf.predict(X_train), beta = 2, pos_label='n1'))
print('\nMCC: ',matthews_corrcoef(y_train, RF_clf.predict(X_train)))
