from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

estimator = SVC(C=1,
          kernel='linear',
          probability=True,
          tol=0.001,
          cache_size=200,
          gamma = 'auto',
          class_weight='balanced',
          verbose=False,
          max_iter=-1,
          random_state= 123)

clf_search = GridSearchCV(estimator,
                   param_grid = {'C': [1,0.5, 0.1]},
                   scoring=fbeta_scorer,
                   fit_params=None,
                   n_jobs=1,
                   iid=True,
                   refit=True,
                   cv= 5,
                   verbose=0,
                   pre_dispatch='2*n_jobs',
                   error_score='raise')
clf_search.fit(Xpca_train, ypca_train)
clf_svm = clf_search.best_estimator_
print(classification_report(ypca_train,
                            clf_svm.predict(Xpca_train),
                            target_names = ['n0', 'n1']))
print('\nF beta: ', fbeta_score(ypca_train, clf_svm.predict(Xpca_train), pos_label='n1',beta=2))
print('\nMCC: ',matthews_corrcoef(ypca_train, clf_svm.predict(Xpca_train)))
