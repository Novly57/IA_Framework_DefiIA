import numpy as np
import pandas as pd

def prop(data, colname, length):
    return data[colname].value_counts()/length

def get_prop():
    hotels = pd.read_csv('../data/features_hotels.csv')
    test_set = pd.read_csv('../data/test_set.csv')
    test_set = test_set.merge(hotels, on=['hotel_id','city'])
    N = len(test_set)

    proportions = {}
    for i in test_set.columns:
        proportions[i] = prop(test_set, i, N)
    return proportions


def generate(proportions = get_prop(), eps = .9):
    list_city = ['amsterdam', 'copenhagen', 'madrid', 'paris', 'rome', 'sofia', 'valletta', 'vienna' ,'vilnius']
    list_lang = ['austrian', 'bulgarian', 'chypriot', 'croatian', 'czech', 'danish', 'dutch', 'estonian', 'finnish', 'french', 'german', 'greek', 'hungarian', 'irish', 'italian', 'latvian', 'lithuanian', 'luxembourgish', 'maltese', 'polish', 'portuguese', 'romanian', 'slovakian', 'slovene', 'spanish','swedish']
    if np.random.uniform() <= eps :
        date = np.random.choice(proportions['date'].index.to_numpy(), 1, p = proportions['date'].to_numpy())[0]
        city = np.random.choice(proportions['city'].index.to_numpy(), 1, p = proportions['city'].to_numpy())[0]
        lang = np.random.choice(proportions['language'].index.to_numpy(), 1, p = proportions['language'].to_numpy())[0]
        mobile = np.random.choice(proportions['mobile'].index.to_numpy(), 1, p = proportions['mobile'].to_numpy())[0]
    else :
        date = np.random.choice(range(45))
        city = np.random.choice(list_city)
        lang = np.random.choice(list_lang)
        mobile = np.random.choice([0,1])
    return lang, city, str(mobile), str(date)