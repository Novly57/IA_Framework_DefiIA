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
for ligne in lignes[1:]:
    ligne = ligne.rstrip("\n").split(",")
    oldRequest.append(ligne[:])
oldRe.close()

domain = "51.91.251.0"
port = 3000
host = f"http://{domain}:{port}"
path = lambda x: urllib.parse.urljoin(host, x)
user_id = '5bafe3fc-6b26-46e0-af72-ee3709ed12d6'

f = open("data.csv","a")
oldRe = open("oldRequest.csv","a")
iteration = 0
    
    
def Re_Extract():
    while True:  
        avatar = rd.choice(oldRequest)
        if int(avatar[2]) > 0:
            sortie = True
            for av in oldRequest:
                if av[0] == avatar[0] and int(avatar[2])>int(av[2]):
                    sortie =False
                    break
            if sortie :
                break
    print(avatar)
    name,c,d,l,m,avatarId,RqNum = avatar#[:-1]
    while True:
    	newD = rd.randint(-44,-1)
    	if 0<=int(d)+newD<44:
    	    d = str(int(d)+newD)
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
    avatar = requ["city"]+','+str(requ["date"])+','+requ["language"]+','+str(requ["mobile"])+','+str(int(RqNum)+1)+','+str(requ["avatar_id"])+','
    data = ''
    for ligne in r1.json()["prices"]:
        data += avatar
        data += str(ligne["hotel_id"]) + ',' + str(ligne["price"]) + ','+ str(ligne["stock"]) + '\n'
    f.write(data)
    oldRe.write(name+','+c + ',' + str(d) + ',' + l + ',' + str(m) + ',' + str(requ["avatar_id"]) + ','+str(int(RqNum)+1) + '\n')
    oldRequest.append([name,c,str(d),l,str(m),avatarId,str(int(RqNum)+1)])
    print(avatar)

def NewEntry():
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


for i in range(400):
    Re_Extract()
    """
    if random.uniform(0,1)<0.5:
    	Re_Extract()
    else:
    	NewEntry()""" # attention OldRequest n'a pas le même format pour les deux méthodes

    
f.close()
oldRe.close()




"""
r = requests.get(path(f"avatars/{user_id}"))
for avatar in r.json():
    print(avatar['id'], avatar['name'])
"""





