from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import learning_curve, validation_curve

base_est = DecisionTreeClassifier(criterion='gini',
                                 splitter='best',
                                 max_depth=1,
                                 min_samples_split=100,
                                 min_samples_leaf=100,
                                 min_weight_fraction_leaf=0.0,
                                 max_features= 10,
                                 random_state=123,
                                 max_leaf_nodes=None,
                                 class_weight='balanced',
                                 presort=False)

estimator = AdaBoostClassifier(base_estimator=base_est,
                         n_estimators=100,
                         learning_rate= 1,
                         algorithm='SAMME.R',
                         random_state=123)


train_sizes, train_scores, test_scores = learning_curve(estimator,
                                                        X_k.loc[X_train.index, :],
                                                        y_train,
                                                        train_sizes = [0.333, 0.666, 1],
                                                        cv = 4,
                                                        scoring=fbeta_scorer,
                                                        exploit_incremental_learning= False)
param_range = [5, 10, 25, 100, 200]
train_scores_val, val_scores_val = validation_curve(estimator,
                                                    X_k.loc[X_train.index, :],
                                                    y_train,
                                                    param_name = "n_estimators",
                                                    param_range= param_range,
                                                    cv=4,
                                                    scoring = fbeta_scorer,
                                                    n_jobs=1)


LC_fig = plt.figure(figsize=(15,5))
A = LC_fig.add_subplot(1,2,1)
A.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', color = 'blue')
A.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', color = 'green')
A.fill_between(train_sizes,
               np.mean(train_scores, axis=1) - np.std(train_scores, axis=1),
               np.mean(train_scores, axis=1) + np.std(train_scores, axis=1),
               color ='blue',
               alpha = 0.25)
A.fill_between(train_sizes,
               np.mean(test_scores, axis=1) - np.std(test_scores, axis=1),
               np.mean(test_scores, axis=1) + np.std(test_scores, axis=1),
               color ='green',
               alpha = 0.25)
A.set_ylim(0,1.1)
B = LC_fig.add_subplot(1,2,2)
B.plot(param_range, np.mean(train_scores_val, axis=1), 'o-', color = 'blue')
B.plot(param_range, np.mean(val_scores_val, axis=1), 'o-', color = 'green')
B.fill_between(param_range,
               np.mean(train_scores_val, axis=1) - np.std(train_scores_val, axis=1),
               np.mean(train_scores_val, axis=1) + np.std(train_scores_val, axis=1),
               color ='blue',
               alpha = 0.25)
B.fill_between(param_range,
               np.mean(val_scores_val, axis=1) - np.std(val_scores_val, axis=1),
               np.mean(val_scores_val, axis=1) + np.std(val_scores_val, axis=1),
               color ='green',
               alpha = 0.25)
B.set_ylim(0,1.1)
plt.show()
