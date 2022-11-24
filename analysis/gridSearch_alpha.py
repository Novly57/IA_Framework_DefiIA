import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split  
from sklearn.preprocessing import StandardScaler  

listAlpha = np.linspace(0,10,4)
for alph in listAlpha:
    colQT = ['request_number', 'stock', 'date']
    colBool = ['mobile', 'pool', 'parking', 'is_same_cl']
    colQL = ['city', 'language', 'group', 'brand', 'children_policy']
    def additive_smoothing(x, alpha = alph):
        """ alpha = 1.96 borne à 95% pour la loi normale  """
        moy = (x+alpha).mean()
        d = x.max()-x.min()
        N = x.count()
        return N*moy/(N+alpha*d)

    additive_smoothing.__name__ = 'additive_smoothing'
    
    path = '../data/' 
    hotels = pd.read_csv(path + '/features_hotels.csv')
    data = pd.read_csv(path + 'data.csv')
    # création de la colonne request_number dans le test set

    data = data.drop(index = data.loc[data.avatar_id == 134].index)
    # ajout des caractéristiques des hotels
    data = data.merge(hotels, on=['hotel_id','city'])
    
    dic_lang = {'amsterdam':'dutch', 'copenhagen':'danish', 'madrid':'spanish', 'paris':'french', 'rome':'italian', 'sofia':'bulgarian', 'valletta':'maltese', 'vienna':'austrian' ,'vilnius':'lithuanian'}
    data['city_language'] = data['city'].map(dic_lang)
    data['is_same_cl'] = data['city_language']==data['language']
    data_test['city_language'] = data_test['city'].map(dic_lang)
    data_test['is_same_cl'] = data_test['city_language']==data_test['language']
    
    for i in colQL :
        df_tmp = data[[i,'price']].groupby(i).agg({'price':['mean','var',additive_smoothing]}).price
        df_tmp = df_tmp.add_suffix('_'+i)
        colQT+= list(df_tmp.columns.unique())
        data = data.join(df_tmp, on = i)

    colQL+= ['price']
    
    y = data[colQT[-1]]
    
    dataQT = data[colQT[:-1]]
    dataBool = data[colBool]
    
    df = pd.concat([dataQT, dataBool],axis=1)
    X_train, X_test, Y_train, Y_test = train_test_split(df,y,test_size=.1,random_state=11)
    
    GBR = GradientBoostingRegressor()
    parameters = {'learning_rate': [0.01,0.03,0.05],
                      'subsample'    : [0.9, 0.5, 0.2],
                      'n_estimators' : [100,750, 1500],
                      'max_depth'    : [4,7,10]}

    grid_GBR = GridSearchCV(estimator=GBR, param_grid = parameters, cv = 2, n_jobs=-1)

    grid_GBR.fit(X_train, Y_train)
    
    print(" Results from Grid Search " )
    print(f"alpha = {alph}")
    print("\n The best estimator across ALL searched params:\n",grid_GBR.best_estimator_)
    print("\n The best score across ALL searched params:\n",grid_GBR.best_score_)
    print("\n The best parameters across ALL searched params:\n",grid_GBR.best_params_)
    all_info = f"alpha = {alph} The best estimator across ALL searched params:\n{grid_GBR.best_estimator_}\n The best score across ALL searched params:\n {grid_GBR.best_score_} \n The best parameters across ALL searched params:\n {grid_GBR.best_params_}\n"
    
    feature_importances = zip(X_train.columns,GBR.feature_importances_)
    x = dict(feature_importances)
    print({k: v for k, v in sorted(x.items(), key=lambda item: -item[1])})
    
    f= open('Save.txt','a')
    f.write(all_info)
    f.close()
