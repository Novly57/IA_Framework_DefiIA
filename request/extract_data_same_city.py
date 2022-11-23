import pandas as pd
import random as rd
import urllib.parse
import requests
import sys

# import functions from generateRequest.py
sys.path.insert(1, '../test_set')
import generateRequest as gen


# possible features
city = ['amsterdam', 'copenhagen', 'madrid', 'paris', 'rome', 'sofia', 'valletta', 'vienna' ,'vilnius']
date = [i for i in range(0,45)]  # entier entre 0 et 44
language = ['austrian', 'bulgarian', 'cypriot', 'croatian', 'czech', 'danish', 'dutch', 'estonian', 'finnish', 'french', 'german', 'greek', 'hungarian', 'irish', 'italian', 'latvian', 'lithuanian', 'luxembourgish', 'maltese', 'polish', 'portuguese', 'romanian', 'slovakian', 'slovene', 'spanish','swedish']
mobile = [0,1]

dic_lang = {'amsterdam':'dutch', 'copenhagen':'danish', 'madrid':'spanish', 'paris':'french', 'rome':'italian', 'sofia':'bulgarian', 'valletta':'maltese', 'vienna':'austrian' ,'vilnius':'lithuanian'}

# save the old requests
oldRe = open("oldRequest.csv","r")
lignes = oldRe.readlines()
oldRequest = []
for ligne in lignes:
    ligne = ligne.rstrip("\n").split(",")
    oldRequest.append(ligne[:-2])
oldRe.close()

domain = "51.91.251.0"
port = 3000
host = f"http://{domain}:{port}"
path = lambda x: urllib.parse.urljoin(host, x)
user_id = '5bafe3fc-6b26-46e0-af72-ee3709ed12d6'
#name = 'first-avatar'
#r = requests.post(path(f'avatars/{user_id}/{name}'))

print("Creation of the avatars")
f = open("data.csv","a")
f2 = open('data_language_utility.csv','a')
oldRe = open("oldRequest.csv","a")
#f.write("City\tDate\tLanguage\tMobile\tAvatar_id\tHotel_id\tPrice\tStock\n") # Only the first time


def do_request(name,l,c,d,m):
    params = {
    "avatar_name": name,
    "language": l,
    "city": c,
    "date": d,
    "mobile": m}
    r1 = requests.get(path(f"pricing/{user_id}"), params=params)
    #r1.json()
    print(r1.json())
    requ = r1.json()["request"]
    avatar = requ["city"]+','+str(requ["date"])+','+requ["language"]+','+str(requ["mobile"])+','+'1,'+str(requ["avatar_id"])+','
    data = ''
    for ligne in r1.json()["prices"]:
        data += avatar
        data += str(ligne["hotel_id"]) + ',' + str(ligne["price"]) + ','+ str(ligne["stock"]) + '\n'
    f.write(data)
    f2.write(data)
    oldRe.write(name+','+c + ',' + str(d) + ',' + l + ',' + str(m) + ',' + str(requ["avatar_id"]) + ',1' + '\n')
    oldRequest.append([c,str(d),l,str(m)])
    return 1


for i in range(100,200):
    name = str(i)+'_avatar_sameLang_and_City'
    r = requests.post(path(f'avatars/{user_id}/{name}'))
    c = rd.choice(city)
    l = dic_lang[c]
    m, d = str(rd.choice(mobile)),str(rd.choice(date))
    do_request(name,l,c,d,m)
    for j in range(3):
    	name = str(j)+'_avatar_compare_'+str(i)
    	r = requests.post(path(f'avatars/{user_id}/{name}'))
    	while True:
    	    l2 = rd.choice(language)
    	    if l2 != l: break
    	do_request(name,l2,c,d,m)
    
f.close()
f2.close()
oldRe.close()


"""
r = requests.get(path(f"avatars/{user_id}"))
for avatar in r.json():
    print(avatar['id'], avatar['name'])
"""





