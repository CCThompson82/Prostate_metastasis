from sklearn.feature_selection import RFECV
from sklearn.svm import SVC
from sklearn.feature_selection import RFECV

svm_clf = SVC(C= 0.05,  #data is noisy and will not be linear separable.
          kernel='linear',
          probability=True,
          tol=0.001,
          cache_size=200,
          gamma = 'auto',
          class_weight='balanced',
          verbose=False,
          max_iter=-1,
          random_state= 123)

from itertools import permutations

def wrapper(clf, X, y, max_features, show_max, steps_down, gain_tolerance) :
    feature_remaining = list(X.columns.values)
    row_list = []
    k_features = []
    test_features = []
    for it in range(0,max_features,1) :
        if steps_down == 0 :
            break
        else :
            feature_scores_dict = {}
            feature_sd_dict = {}
            for feature in feature_remaining :
                test_features.append(feature)
                clf.fit(X.loc[:,test_features], y)
                cv_scores = cross_val_score(clf, X.loc[:,test_features], y, scoring = fbeta_scorer, cv = 4)
                feature_scores_dict.update({tuple(test_features) : np.mean(cv_scores)})
                feature_sd_dict.update({tuple(test_features) : np.std(cv_scores)})
                test_features.remove(test_features[-1])
            k_features.append(max(feature_scores_dict.keys(), key=(lambda k: feature_scores_dict[k]))[-1])
            test_features.append(max(feature_scores_dict.keys(), key=(lambda k: feature_scores_dict[k]))[-1])
            feature_remaining.remove(max(feature_scores_dict.keys(), key=(lambda k: feature_scores_dict[k]))[-1])
            dict1 = {'n_features': len(k_features),
                     'F2_score': feature_scores_dict.get(tuple(k_features)),
                     'F2_SD' : feature_sd_dict.get(tuple(k_features)),
                     'Features': list(k_features)}
            row_list.append(dict1)
            print('Iteration: ',it+1,' complete!')

            """Does F2 increase?"""
            #print(row_list[-1])
            if it > 0 :
                gain = row_list[-1].get('F2_score') - row_list[-2].get('F2_score')
                print("F2 Score Gain:",gain)
                if gain < gain_tolerance :
                    steps_down -= 1

    """Benchmark for all features used"""
    if show_max == True :
        clf.fit(X,y)
        cv_scores = cross_val_score(clf, X, y, scoring = fbeta_scorer, cv = 5)
        dict1 = {'n_features': X.shape[1],
                 'F2_score': np.mean(cv_scores),
                 'F2_SD' : np.std(cv_scores),
                 'Features': ["ALL"]}
        row_list.append(dict1)
    DF = pd.DataFrame(row_list, columns=['n_features','F2_score','F2_SD','Features'])
    #print(DF.iloc[:,0:3])

    """Make Complexity Plot"""
    plt.figure(figsize=(10,10))
    plt.scatter(DF['n_features'], DF['F2_score'], color='black')
    plt.errorbar(DF['n_features'], DF['F2_score'], yerr=DF['F2_SD'])
    plt.xlabel('Number of features')
    plt.xlim(0, np.max(DF['n_features'])+1)
    plt.ylabel('Mean F2 Score (CV=5)')
    plt.title('Complexity Plot')
    plt.show()
    return(k_features, DF)


k_features, DF = wrapper(svm_clf,
                         X_k.loc[X_train.index],
                         y_train,
                         max_features= 5,
                         show_max= False,
                         steps_down=3,
                         gain_tolerance = 0.0)

print(DF.head())
