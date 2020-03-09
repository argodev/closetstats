# load the json file
import json
import pprint

with open('geojson-counties-fips.json') as f:
    x = json.load(f)

#for entry in x:
#    pprint.pprint(x)
#    break

#pprint.pprint(x[0])
#print(len(x))

print(len(x['features']))

new_features = []

#for k in x['features']:
#    if k['properties']['NAME'] == "Sevier":
#        k['id'] = k['properties']['NAME']
#        new_features.append(k)
#        pprint.pprint(k)


# I don't know why, but the number 47 is 
# the TN state ID in this file
for k in x['features']:
    if k['properties']['STATE'] == "47":
        k['id'] = k['properties']['NAME']
        new_features.append(k)

x['features'] = new_features
print(len(new_features))

with open('tncounties.json', 'w', encoding='utf-8') as f:
    json.dump(x, f, ensure_ascii=False, indent=5)
