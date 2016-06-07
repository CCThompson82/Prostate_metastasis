from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
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
                         learning_rate=.001,
                         algorithm='SAMME',
                         random_state=123)

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

ada_clf = clf.best_estimator_
print(classification_report(y_train,
                            clf.predict(X_train),
                            target_names = ['n0', 'n1']))
