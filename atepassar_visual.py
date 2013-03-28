#-*- coding:utf-8 -*-
from unicodedata import normalize
from pygeocoder import Geocoder
import pickle
import time


remove_acentos = lambda x:  normalize('NFKD', x).encode('ASCII','ignore')

users = open('users.csv')

pk3 = open('geo_cities.pk3', 'rb')
pk4 = open('geo_cities.pk4', 'rb')

pk_final = open('atepassar_geo.pk', 'wb+')

geo = pickle.load(pk3)
tmp = pickle.load(pk3)

geo2 = pickle.load(pk4)
tmp2 = pickle.load(pk4)

print len(geo) + len(geo2)
geo.update(geo2)

user_friends = open('user_friends.csv')
user_followers = open('users_followers.csv')

user_cities = {}
user_fr = {}
user_fo = {}

for usr in user_friends:
    usr = usr.strip().split(';')
    usr, friends = usr[0], usr[1:]
    friends = map(int, filter(lambda x: x not in [''], friends))
    user_fr[int(usr)] = friends + [int(usr)]

#print len(user_fr)
#print user_fr[1]

for usr in user_followers:
    usr = usr.strip().split(';')
    usr, followers = usr[0], usr[1:]
    followers = map(int, filter(lambda x: x not in [''], followers))
    user_fo[int(usr)] = followers + [int(usr)]

#print len(user_fo)
#print user_fo[1]

mutual_friends = user_fr.items() + user_fo.items()

final_sn = {}

for user,relationships in mutual_friends:
    final_sn.setdefault(user,[])
    final_sn[user].extend(relationships)
    final_sn[user] = list(set(final_sn[user]))
        
#print len(final_sn)
#print final_sn[1]


'''
user_cities = {}


for user in users:
   user = user.strip()
   user_id, city, state, abbr = user.split(';')
   city = remove_acentos(city.decode('utf-8').lower()).title()
   user_cities.setdefault((city, state, abbr), [])
   user_cities[(city, state, abbr)].append(user_id)

print len(user_cities)


'''

atepassar_users =  {}


for user in geo:
    if user == 39:
	    continue #mascote..no!
    print user
    friends = final_sn[user]
    print user, friends
    for friend in friends:
        try:
            atepassar_users.setdefault((geo[user], geo[friend]), 0)
            atepassar_users[(geo[user], geo[friend])] +=1
        except KeyError:
            print friend

print atepassar_users.items()[-1]
pickle.dump(atepassar_users, pk_final)
pk_final.close()

'''
cities_user = {}


temp_cities = []

for city, state, abbr in user_cities:
    achou = False
    for user in user_cities[(city, state, abbr)]:
        if (city, state, abbr, user) in tmp:
            print 'achei'
            achou = True
    if achou:
        continue
    endereco =  '%s, %s, Brasil' % (city, state)
    results = Geocoder.geocode(endereco)
    coords, end = results[0].coordinates, results[0]
    print coords, end
    for user in user_cities[(city, state, abbr)]:
         cities_user[int(user)] = coords
         temp_cities.append((city, state, abbr, user))

pickle.dump(cities_user, pk4)
pickle.dump(temp_cities, pk4)
pk4.close()

'''



'''
for city, state, abbr in user_cities:
    if len(user_cities[(city, state, abbr)]) <= 1:
        count+=1

print count / float(len(user_cities))

'''
