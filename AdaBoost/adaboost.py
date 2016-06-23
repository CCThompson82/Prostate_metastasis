from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import NuSVC
from sklearn.learning_curve import learning_curve

base_est = DecisionTreeClassifier(criterion='gini',
                                  splitter='best',
                                  max_depth=1,
                                  min_samples_split=50,
                                  min_samples_leaf=10,
                                  min_weight_fraction_leaf=0.0,
                                  max_features=None,
                                  random_state=123,
                                  max_leaf_nodes=None,
                                  class_weight='balanced',
                                  presort=False)


estimator = AdaBoostClassifier(base_estimator=base_est,
                         n_estimators=100,
                         learning_rate= 1,
                         algorithm='SAMME',
                         random_state=123)

l_curve = learning_curve(estimator,
                         X_train,
                         y_train,
                         train_sizes = [0.12, 0.25, 0.5, 0.75,0.88, 1],
                         cv = 3,
                         scoring=fbeta_scorer,
                         exploit_incremental_learning= False)

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

ada_clf = clf.best_estimator_
print(classification_report(y_train,
                            clf.predict(X_train),
                            target_names = ['n0', 'n1']))
print('F beta: ', fbeta_score(y_train, ada_clf.predict(X_train), beta = 2, pos_label='n1'))
print('\nMCC: ',matthews_corrcoef(y_train, ada_clf.predict(X_train)))
