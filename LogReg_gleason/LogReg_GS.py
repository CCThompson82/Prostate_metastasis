from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(solver='svd',
                                 shrinkage=None,
                                 priors=None,
                                 n_components=1,
                                 store_covariance=False,
                                 tol=0.0001)
lda.fit(Xpca_train,ypca_train)
Xlda_train = lda.transform(Xpca_train)
Xlda_test = lda.transform(Xpca_test)

#gleason = clinical['gleasonscore']
#gleason = gleason.loc[y.index]
gleason_train = gleason.loc[y_train.index]
gleason_test = gleason.loc[y_test.index]
gleason_train = gleason_train.reshape(-1,1)
gleason_test = gleason_test.reshape(-1,1)

logisticDF = pd.DataFrame({'lda_transform' : Xlda_train[:,0],
                           'gleason_scores' : gleason_train[:,0]}, index = y_train.index)
logisticDF_test = pd.DataFrame({'lda_transform' : Xlda_test[:,0],
                                'gleason_scores' : gleason_test[:,0]}, index = y_test.index)

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
                   scoring=fbeta_scorer,
                   fit_params=None,
                   n_jobs=1,
                   iid=True,
                   refit=True,
                   cv= 5,
                   verbose=0,
                   pre_dispatch='2*n_jobs',
                   error_score='raise')
clf.fit(logisticDF, y_train)
LR_clf = clf.best_estimator_
print(LR_clf)
print(classification_report(y_train,
                            LR_clf.predict(logisticDF),
                            target_names = ['n0', 'n1']))
print('\nF beta: ', fbeta_score(y_train, LR_clf.predict(logisticDF), beta = 2, pos_label='n1'))
print('\nMCC: ',matthews_corrcoef(y_train, LR_clf.predict(logisticDF)))
