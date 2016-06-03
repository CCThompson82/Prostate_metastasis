from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.metrics import f1_score, make_scorer
import feather

#X_train = feather.read_dataframe("X_train.feather") #make files accessible to individual py programs
#y_train = feather.read_dataframe("y_train.feather") #make files accessible to individual py programs

f1_scorer = make_scorer(f1_score,
                        greater_is_better = True,
                        needs_proba= False,
                        needs_threshold=False,
                        pos_label='n1',
                        average = 'binary')
estimator = SVC(C=.5,
                kernel='linear',
                probability=False,
                tol=0.001,
                cache_size=200,
                class_weight={'n0':0.05, 'n1':0.95},
                verbose=False,
                max_iter=-1,
                random_state= 123)
selector = RFECV(estimator,
                 step = 2,
                 cv = 5,
                scoring = f1_scorer)
selector.fit(X_train, y_train)

from sklearn.metrics import classification_report
print(classification_report(y_train,
                            selector.predict(X_train),
                            target_names = ['n0', 'n1']))
print(X_train.columns[selector.support_])
SVM_clf = selector.estimator_
print(SVM_clf)