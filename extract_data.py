import pandas as pd
import random as rd
import urllib.parse
import requests

# possible features
city = ['amsterdam', 'copenhagen', 'madrid', 'paris', 'rome', 'sofia', 'valletta', 'vienna' ,'vilnius']
date = [i for i in range(0,45)]  # entier entre 0 et 44
language = ['austrian', 'bulgarian', 'chypriot', 'croatian', 'czech', 'danish', 'dutch', 'estonian', 'finnish', 'french', 'german', 'greek', 'hungarian', 'irish', 'italian', 'latvian', 'lithuanian', 'luxembourgish', 'maltese', 'polish', 'portuguese', 'romanian', 'slovakian', 'slovene', 'spanish','swedish']
mobile = [0,1]


domain = "51.91.251.0"
port = 3000
host = f"http://{domain}:{port}"
path = lambda x: urllib.parse.urljoin(host, x)
user_id = '5bafe3fc-6b26-46e0-af72-ee3709ed12d6'
#name = 'first-avatar'
#r = requests.post(path(f'avatars/{user_id}/{name}'))

print("Creation of the avatars")
f = open("Data_DefiIA2.txt","w")
f.write("City\tDate\tLanguage\tMobile\tAvatar_id\tHotel_id\tPrice\tStock\n") # Only the first time

for i in range(6,20):
    name = str(i)+'_avatar'
    r = requests.post(path(f'avatars/{user_id}/{name}'))
    l, c, d, m = rd.choice(language),rd.choice(city),str(rd.choice(date)),str(rd.choice(mobile))
    params = {
    "avatar_name": name,
    "language": l,
    "city": c,
    "date": d,
    "mobile": m}
    r1 = requests.get(path(f"pricing/{user_id}"), params=params)
    #r1.json()
    requ = r1.json()["request"]
    avatar = requ["city"]+'\t'+str(requ["date"])+'\t'+requ["language"]+'\t'+str(requ["mobile"])+'\t'+str(requ["avatar_id"])+'\t'
    data = ''
    for ligne in r1.json()["prices"]:
        data += avatar
        data += str(ligne["hotel_id"]) + '\t' + str(ligne["price"]) + '\t'+ str(ligne["stock"]) + '\n'
        f.write(data)
    
f.close()
print("Avatars created")


"""
r = requests.get(path(f"avatars/{user_id}"))
for avatar in r.json():
    print(avatar['id'], avatar['name'])
"""





