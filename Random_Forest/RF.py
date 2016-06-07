from sklearn.ensemble import RandomForestClassifier

estimator = RandomForestClassifier(n_estimators=50,
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
                   scoring=f1_scorer,
                   fit_params=None,
                   n_jobs=1,
                   iid=True,
                   refit=True,
                   cv= 5,
                   verbose=0,
                   pre_dispatch='2*n_jobs',
                   error_score='raise')

clf.fit(X_train, y_train)

print(classification_report(y_train,
                            clf.predict(X_train),
                            target_names = ['n0', 'n1']))

print(clf.best_estimator_)
RF_clf = clf.best_estimator_
