import pandas as pd
import numpy as np

def train_test_dataset(hotels, data, data_test, lang_cit):
    ### DROP DUPLICATES & DATA WITH PROBLEMS
    to_exclude = data[['city', 'language','mobile','request_number','date']].drop_duplicates()
    # to_exclude.to_csv('to_exclude.csv', index = False)

    tot = 0 
    for i in range(7):
        tot += np.unique(data.loc[data.request_number == i].avatar_id.values).shape[0]

    to_drop = [134]
    data = data.loc[~data.avatar_id.isin(to_drop)]

    data = data.drop(['avatar_id'], axis = 1).drop_duplicates()

    ### ajout des caractéristiques des hotels
    data = data.merge(hotels, on=['hotel_id','city'])
    data_test = data_test.merge(hotels, on=['hotel_id','city'])
    data_test = data_test.sort_values('index').reset_index(drop=True).drop(['index'], axis = 1)

    ### création de la colonne request_number dans le test set
    data_test['request_number'] = 1
    for avatar in np.unique(data_test['avatar_id']):
        data_test.loc[data_test['avatar_id'] == avatar, 'request_number'] = data_test['order_requests'].loc[data_test['avatar_id']== avatar] - min(data_test['order_requests'].loc[data_test['avatar_id']== avatar])+1
        
    ### ajout de la variable ville == langue
    if lang_cit == True: 
        dic_lang = {'amsterdam':'dutch', 'copenhagen':'danish', 'madrid':'spanish', 'paris':'french', 'rome':'italian', 'sofia':'bulgarian', 'valletta':'maltese', 'vienna':'austrian' ,'vilnius':'lithuanian'}
        data['city_language'] = data['city'].map(dic_lang)
        data['is_same_cl'] = data['city_language']==data['language']
        data_test['city_language'] = data_test['city'].map(dic_lang)
        data_test['is_same_cl'] = data_test['city_language']==data_test['language']
    #     colBool += ['is_same_cl']

    ### colonnes pour l'analyse
    col = ['city', 'date', 'language', 'mobile', 'request_number', 'stock', 'group', 'brand', 'parking', 'pool','children_policy', 'is_same_cl', 'price']
    data = data[col]
    data_test = data_test[col[:-1]]

    ### additive smoothing
    def additive_smoothing(x,alpha= 1.96):
        """ alpha = 1.96 borne à 95% pour la loi normale  """
        moy = (x+alpha).mean()
        d = x.max()-x.min()
        N = x.count()
        return N*moy/(N+alpha*d)

    additive_smoothing.__name__ = 'additive_smoothing'

    colQT = ['request_number', 'stock', 'date']
    notQT = ['city', 'language', 'mobile', 'group', 'brand', 'parking', 'pool','children_policy', 'is_same_cl'] 

    for i in notQT:
        df_tmp = data[[i, 'price']].groupby(i).agg({'price': ['mean', 'var', additive_smoothing]}).price
        df_tmp = df_tmp.add_suffix('_' + i)
        colQT += list(df_tmp.columns.unique())
        data = data.join(df_tmp, on=i)
        data_test = data_test.join(df_tmp, on=i)

    colQT += ['price']

    ### dataframes / X_train / X_test
    df = data[colQT[:-1]]
    df_test = data_test[colQT[:-1]]
    y = data[colQT[-1]]

    X_train = df
    X_test = df_test
    Y_train = y
    Y_test = None

    return X_train, X_test, Y_train, Y_test