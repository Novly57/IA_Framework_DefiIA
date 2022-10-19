import pandas as pd
import random as rd
import urllib.parse
import requests
import sys

# import functions from generateRequest.py
sys.path.insert(1, '../test_set')
import generateRequest as gen

# save the old requests
oldRe = open("oldRequest.csv","r")
lignes = oldRe.readlines()
oldRequest = []
for ligne in lignes:
    ligne = ligne.rstrip("\n").split(",")
    oldRequest.append(ligne[:])
oldRe.close()

domain = "51.91.251.0"
port = 3000
host = f"http://{domain}:{port}"
path = lambda x: urllib.parse.urljoin(host, x)
user_id = '5bafe3fc-6b26-46e0-af72-ee3709ed12d6'

#f = open("data.csv","a")
#oldRe = open("oldRequest.csv","a")

for i in range(1):
    while True:  
        avatar = rd.choice(oldRequest[1:])
        if avatar[1] > 0:
            break
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
    oldRe.write(c + ',' + str(d) + ',' + l + ',' + str(m) + ',' + str(requ["avatar_id"]) + ',1' + '\n')
    oldRequest.append([c,str(d),l,str(m)])
    print(avatar)

"""
iteration = 0
for i in range(600,1000):
    name = str(i)+'_avatar'
    r = requests.post(path(f'avatars/{user_id}/{name}'))
    while True:
    	l, c, m, d = gen.generate() #rd.choice(language),rd.choice(city),str(rd.choice(date)),str(rd.choice(mobile))
    	#print([l,c,m,d])
    	if [l,c,m,d] not in oldRequest: break
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
    oldRe.write(c + ',' + str(d) + ',' + l + ',' + str(m) + ',' + str(requ["avatar_id"]) + ',1' + '\n')
    oldRequest.append([c,str(d),l,str(m)])
    
f.close()
oldRe.close()

"""
"""
r = requests.get(path(f"avatars/{user_id}"))
for avatar in r.json():
    print(avatar['id'], avatar['name'])
"""





