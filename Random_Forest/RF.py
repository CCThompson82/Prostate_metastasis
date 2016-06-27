from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import learning_curve, validation_curve
estimator = RandomForestClassifier(n_estimators=250,
                                   criterion='gini',
                                   max_depth=1,
                                   min_samples_split=100,
                                   min_samples_leaf=50,
                                   min_weight_fraction_leaf=0.0,
                                   max_features= 5,
                                   max_leaf_nodes=None,
                                   bootstrap=True,
                                   oob_score=False,
                                   n_jobs=1,
                                   random_state=123,
                                   verbose=0,
                                   warm_start=False,
                                   class_weight='balanced')


train_sizes, train_scores, test_scores = learning_curve(estimator,
                                                        X_k.loc[X_train.index, :],
                                                        y_train,
                                                        train_sizes = [0.33, 0.66, 1],
                                                        cv = 4,
                                                        scoring=fbeta_scorer,
                                                        exploit_incremental_learning= False)
param_range = [10, 50, 100, 250, 500, 1000]
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
plt.show()
