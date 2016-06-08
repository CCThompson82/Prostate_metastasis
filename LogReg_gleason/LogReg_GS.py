from sklearn.linear_model import LogisticRegression
gleason_train = gleason.loc[y_train.index]
gleason_test = gleason.loc[y_test.index]
gleason_train = gleason_train.reshape(-1,1)
gleason_test = gleason_test.reshape(-1,1)

estimator = LogisticRegression(penalty='l2',
                              dual=False,
                              tol=0.0001,
                              C=.1,
                              fit_intercept=True,
                              intercept_scaling=1,
                              class_weight='balanced',
                              random_state=123,
                              solver='liblinear',
                              max_iter=100,
                              multi_class='ovr',
                              verbose=0,
                              warm_start=False,
                              n_jobs=1)
clf = GridSearchCV(estimator,
                   param_grid = {'C': [1,0.5,0.1,0.01]},
                   scoring=matthews_cor_scorer,
                   fit_params=None,
                   n_jobs=1,
                   iid=True,
                   refit=True,
                   cv= 5,
                   verbose=0,
                   pre_dispatch='2*n_jobs',
                   error_score='raise')
clf.fit(gleason_train, y_train)

print(classification_report(y_train,
                            clf.predict(gleason_train),
                            target_names = ['n0', 'n1']))
Gleason_LR_clf = clf.best_estimator_
print(Gleason_LR_clf)

print('MCC: ',matthews_corrcoef(y_train, Gleason_LR_clf.predict(gleason_train)))
