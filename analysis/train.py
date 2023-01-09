import pandas as pd
import numpy as np 
from sklearn.ensemble import GradientBoostingRegressor
import pickle

############################## PARAMETERS TO FILL ##############################
path = '../data/'                   # chemin vers le dossier contenant les données
lang_cit = True                     # pour utiliser la variablle ville == langue
_round = False                      # pour arrondir les prédictions
name = 'submit_from_train'          # name (csv file)
file_name = 'model_from_train'      # name (model file)



# boosting parameters
learning_rate = .01             # best = .01                         
max_depth = 4                   # best = 4 
n_estimators = 10               # best = 1500
validation_fraction = .1        # best = .1 
criterion = 'friedman_mse'      # best = 'friedman_mse'
subsample = .2                  # best = .2
max_leaf_nodes = 50             # best = 50
max_features = 1.0              # best = 1.0
verbose = 1                     # best = 1

################################################################################

### LOADING DATA
hotels = pd.read_csv(path + '/features_hotels.csv')
data = pd.read_csv(path + 'data.csv')
data_test = pd.read_csv(path + 'test_set.csv')

### DROP DUPLICATES & DATA WITH PROBLEMS
to_exclude = data[['city', 'language','mobile','request_number','date']].drop_duplicates()
# to_exclude.to_csv('to_exclude.csv', index = False)
print('---------\nNombre de requêtes uniques :', to_exclude.shape[0])

tot = 0 
for i in range(7):
    tot += np.unique(data.loc[data.request_number == i].avatar_id.values).shape[0]
print('---------\nEstimation du nombre total de requêtes :', tot)
print('---------')

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

### boosting
GBR = GradientBoostingRegressor()
GBR.set_params(learning_rate = learning_rate, 
                max_depth = max_depth,
                n_estimators = n_estimators,
                validation_fraction = validation_fraction,
                criterion = criterion,
                subsample = subsample,
                max_leaf_nodes = max_leaf_nodes,
                max_features = max_features,
                verbose = verbose)

fit = GBR.fit(X_train,Y_train)
y_pred = fit.predict(X_test)

### save

if _round : y_pred = np.round(y_pred)

sub = pd.DataFrame(y_pred)
sub.to_csv(path + 'submit/' + name + '.csv',index=True, header=['price'], index_label = 'index')

pickle.dump(fit, open(file_name,'wb'))
model_loaded = pickle.load(open(file_name,'rb'))



