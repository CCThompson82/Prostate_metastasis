from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.feature_selection import RFECV

estimator = SVC(C=.05,
          kernel='linear',
          probability=True,
          tol=0.001,
          cache_size=200,
          gamma = 'auto',
          class_weight='balanced',
          verbose=False,
          max_iter=-1,
          random_state= 123)

clf_svm_rf = RFECV(estimator,
                   step=1,
                   cv=4,
                   scoring=fbeta_scorer)

clf_svm_rf.fit(X_kk.loc[X_train.index,:], y_train)

X_svm = pd.DataFrame(clf_svm_rf.transform(X_kk), index= X_kk.index, columns = X_kk.columns[clf_svm_rf.support_])

train_sizes, train_scores, test_scores = learning_curve(estimator,
                                                        X_svm.loc[X_train.index, :],
                                                        y_train,
                                                        train_sizes = [0.33, 0.66, 1],
                                                        cv = 4,
                                                        scoring=fbeta_scorer,
                                                        exploit_incremental_learning= False)
param_range = [0.5, .2,.15,.1,.05, 0.01, 1e-3]
train_scores_val, val_scores_val = validation_curve(estimator,
                                                    X_svm.loc[X_train.index, :],
                                                    y_train,
                                                    param_name = "C",
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
