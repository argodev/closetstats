
from pymongo import MongoClient
import os
import pprint
import csv

# read in important enviornment variables
DBUSER = os.environ["CSTATS_DATABASE_USER"]
DBPWD = os.environ["CSTATS_DATABASE_PWD"]
DBSVR = os.environ["CSTATS_DATABASE_SERVER"]
DBSHARD = os.environ["CSTATS_DATABASE_SHARD"]
CSVFILE = "/home/ru7/Downloads/uszips.csv"

DBCONNSTR = "mongodb+srv://{0}:{1}@{2}/test".format(DBUSER, DBPWD, DBSVR)

client = MongoClient(DBCONNSTR)

db = client.closet_stats
visits = db.visits


def xlate_to_num(entry, field):
    if entry[field]:
        entry[field] = float(entry[field])
    else:
        entry.pop(field, None)


def xlate_to_arr(entry, field):
    if entry[field]:
        entry[field] = entry[field].split('|')
    else:
        entry.pop(field, None)


def load_zip_data(db, code):
    # get the collection
    zipdata = db.zipdata

    reader = csv.DictReader(open(CSVFILE, 'r'))
    entries = []
    for line in reader:
        if code in line['state_id']:
            xlate_to_num(line, 'lat')
            xlate_to_num(line, 'lng')
            xlate_to_num(line, 'population')
            xlate_to_num(line, 'density')
            xlate_to_num(line, 'age_median')
            xlate_to_num(line, 'male')
            xlate_to_num(line, 'female')
            xlate_to_num(line, 'married')
            xlate_to_num(line, 'family_size')
            xlate_to_num(line, 'income_household_median')
            xlate_to_num(line, 'income_household_six_figure')
            xlate_to_num(line, 'home_ownership')
            xlate_to_num(line, 'home_value')
            xlate_to_num(line, 'rent_median')
            xlate_to_num(line, 'education_college_or_above')
            xlate_to_num(line, 'labor_force_participation')
            xlate_to_num(line, 'unemployment_rate')
            xlate_to_num(line, 'race_white')
            xlate_to_num(line, 'race_black')
            xlate_to_num(line, 'race_asian')
            xlate_to_num(line, 'race_native')
            xlate_to_num(line, 'race_pacific')
            xlate_to_num(line, 'race_other')
            xlate_to_num(line, 'race_multiple')

            line['zcta'] = bool(line['zcta'])
            line['imprecise'] = bool(line['imprecise'])
            line['military'] = bool(line['military'])

            xlate_to_arr(line, 'county_names_all')
            xlate_to_arr(line, 'county_fips_all')

            # change lat/lng to GeoJSON Point
            geo = {"type": "Point", "coordinates": []}
            geo["coordinates"].append(line['lng'])
            geo["coordinates"].append(line['lat'])
            line["location"] = geo
            line.pop('lng', None)
            line.pop('lat', None)

            entries.append(line)

#    pprint.pprint(entries[0])
    print("Sending entries to MongoDB...")
    for idx, entry in enumerate(entries):
        print("Sending entry %d" % idx)
        zipdata.insert_one(entry)

def update_visits_with_zip(db):
    visits = db.visits
    zipdata = db.zipdata

    # get all the zip data and cache it
    zipdata = list(db.zipdata.find({}))

    # now, we loop through the visits and update them
    for ndx, visit in enumerate(visits.find({})):
        print("Processing visit #%d" % ndx)
        zipCode = visit.get('zipCode', None)
        if zipCode:
            for zip in zipdata:
                if zipCode == zip['zip']:
                    print(visit["_id"])
                    db.visits.update_one({"_id": visit["_id"]},
                                         {"$set": {
                                             "county": zip['county_name'],
                                             "location": zip['location']
                                         }})
#                    visit['county'] = zip['county_name']
#                    visit['location'] = zip['location']


def served_by_county(db):
    visits = db.visits
    counties = {}
    for _, visit in enumerate(visits.find({})):
        county = visit.get('county', None)
        if county:
            if county in counties:
                counties[county] += visit["numKidsServed"]
            else:
                counties[county] = visit["numKidsServed"]
    pprint.pprint(counties)



# load the zip data
# load_zip_data(db, "TN")
# load_zip_data(db, "KY")
# load_zip_data(db, "GA")
# load_zip_data(db, "NC")
# load_zip_data(db, "SC")
# load_zip_data(db, "AL")

# update visit records with zipcode data
# add/update county, add/update location
# all other zip demographics remain in zipdata
# update_visits_with_zip(db)




# Now, we want to get the children served by county and output that
# served_by_county(db)


# Next, we need to create a fancy map
from colour import Color

counties = {'Anderson': 42,
             'Blount': 10,
             'Grainger': 3,
             'Jefferson': 4,
             'Knox': 102,
             'Loudon': 15,
             'Monroe': 44,
             'Roane': 6,
             'Sevier': 17}
# find max
max = 0
for key in counties.keys():
    if counties[key] > max:
        max = counties[key]

print(max)

white = Color("white")
blue = Color("blue")
blues = list(white.range_to(blue, max + 1))
#pprint.pprint(colors)

for key in counties.keys():
    my_blue = blues[counties[key]]
    print("%s\t%s\n" % (key, my_blue))




#"zip","lat","lng","city","state_id","state_name","zcta","parent_zcta","population","density","county_fips","county_name","county_weights","county_names_all","county_fips_all","imprecise","military","timezone","age_median","male","female","married","family_size","income_household_median","income_household_six_figure","home_ownership","home_value","rent_median","education_college_or_above","labor_force_participation","unemployment_rate","race_white","race_black","race_asian","race_native","race_pacific","race_other","race_multiple"
#"00501","40.81308","-73.04639","Holtsville","NY","New 
#York","FALSE","11742","","","36103","Suffolk","{""36103"": 
#100}","Suffolk","36103","FALSE","FALSE","America/New_York","","","","","","","","","","","","","","","","","","","",""


# let's get the distinct zipcodes
#zipcodes = []
#for visit in visits.find():
#    zipcodes.append(visit.get('zipCode', ''))
#    pprint.pprint(visit)

#zipcodes = set(zipcodes)
#pprint.pprint(zipcodes)







# Things we need to do:
# - get zipcodes --> geo mapping list
# - get zipcode/geo --> county list
# - update insert to apply or use aggregation?
# - create county-based Choropleth
# - get 2019 and 2018 data into Mongo
# - share access to dashboard with staff/board
