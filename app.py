import pandas as pd
import gradio as gr
import numpy as np
import pickle
import warnings
import os
warnings.filterwarnings("ignore")

path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data/')
file_name = 'gradio_model'
# pickle.dump(gbmOpt, open(file_name,'wb')) avec gbmOpt = gbm.fit(...)
model_loaded = pickle.load(open(path+file_name,'rb'))

target_enco = pd.read_csv(path+'target_encoding.csv')
hotels = pd.read_csv(path + '/features_hotels.csv')
data_test = pd.read_csv(path + '/data.csv')
data_test_stock = data_test.drop(['mobile','avatar_id','price','language','city','request_number'],axis=1).drop_duplicates()
data_test_city = hotels.drop(['group','brand','parking','children_policy','pool'],axis=1).drop_duplicates()

def predict_price(order_requests, city, date, language, mobile, hotel_id):
    stock_info = data_test_stock.loc[data_test_stock['hotel_id']==hotel_id]
    city_info = data_test_city
    if hotel_id not in np.unique(city_info.loc[city_info['city'] == city]['hotel_id']):
        return 'Please select a correct hotel_id in the list below', list(np.unique(city_info.loc[city_info['city'] == city]['hotel_id'])),''
    else :
        stock_info.set_index('date', inplace=True)
        stock_info['stock'] = stock_info['stock'].interpolate()
        stock_info = stock_info.reset_index()
        stock = int(stock_info.loc[stock_info['date']==date]['stock'])

        hotels['hotel_id'].loc[hotels['city']==city]
        city_encoding = list(target_enco.loc[target_enco['name'] == 'city_'+city].iloc[0])[:-1]
        language_encoding = list(target_enco.loc[target_enco['name'] == 'language_'+language].iloc[0])[:-1]
        mobile_encoding = list(target_enco.loc[target_enco['name'] == 'mobile_'+str(int(mobile))].iloc[0])[:-1]
        hotel_encoding = list(target_enco.loc[target_enco['name'] == 'hotel_id_'+str(hotel_id)].iloc[0])[:-1]


        X_test = pd.DataFrame([[order_requests,stock,date]+city_encoding+language_encoding+mobile_encoding+hotel_encoding])
        y_pred = model_loaded.predict(X_test)
        hoteldic = hotels.iloc[hotel_id].to_dict()
#         sentence = f'Hotel from group : {hoteldic['group']} and brand :{hoteldic['brand']}. '
        sentence = 'Hotel from group : '+hoteldic['group']+' and brand :'+hoteldic['brand']+'. '
        if hoteldic['pool'] and hoteldic['parking']:
            sentence+= 'Pool and Parking available'
        elif hoteldic['pool']:
            sentence+= 'Pool available'
        elif hoteldic['parking']:
            sentence+= 'Parking available'
        sentence += '. Children policy of type ' + str(hoteldic['children_policy'])
        return stock,np.round(y_pred[0],2),sentence


cities = ['amsterdam', 'copenhagen', 'madrid', 'paris', 'rome', 'sofia', 'valletta', 'vienna' ,'vilnius']


ord_requ = gr.inputs.Slider(minimum=1, maximum = 6,default=1,step=1)
lang = gr.inputs.Dropdown(choices = ['austrian', 'bulgarian', 'cypriot', 'croatian', 'czech', 'danish', 'dutch', 'estonian', 'finnish', 'french', 'german', 'greek', 'hungarian', 'irish', 'italian', 'latvian', 'lithuanian', 'luxembourgish', 'maltese', 'polish', 'portuguese', 'romanian', 'slovakian', 'slovene', 'spanish','swedish'])
cit = gr.inputs.Dropdown(choices = ['amsterdam', 'copenhagen', 'madrid', 'paris', 'rome', 'sofia', 'valletta', 'vienna' ,'vilnius'])
input_hotel_id = gr.inputs.Slider(0, 999,default=1,step=1)
dat = gr.inputs.Slider(0, 44,default=1,step=1)

app = gr.Interface(
    fn=predict_price,
    inputs=[ord_requ,cit,dat,lang, "checkbox",input_hotel_id],
    outputs=[gr.outputs.Textbox(label="Stocks Available"),gr.outputs.Textbox(label="Price"),gr.outputs.Textbox(label="Hotel Features")],
    examples = [[1,'rome',31,'french',True,38],
               [2,'valletta',10,'bulgarian',False,55],
               [3,'madrid',26,'danish',True,860]],
    live = True)
app.launch(share=True)
