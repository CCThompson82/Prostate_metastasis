from sklearn.feature_selection import RFECV
from sklearn.svm import SVC

estimator = SVC(C= .5,
                kernel='linear',
                probability=False,
                tol=0.001,
                gamma = 'auto',
                cache_size=200,
                class_weight='balanced',
                verbose=False,
                max_iter=-1,
                random_state= 123)
selector = RFECV(estimator,
                 step = 2,
                 cv = 5,
                scoring = matthews_cor_scorer)
selector.fit(Xpca_train, ypca_train)

print(classification_report(ypca_train,
                            selector.predict(Xpca_train),
                            target_names = ['n0', 'n1']))
print(Xpca_train.columns[selector.support_])

SVM_clf = selector.estimator_

print(SVM_clf)
