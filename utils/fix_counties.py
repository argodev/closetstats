
from pymongo import MongoClient
import os
import pprint
import csv
from datetime import datetime
import json

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

    # now, let's loop through the counties, set up some structure and dump
    county_data = []
    for k in counties.keys():
        county_data.append({
            "name": k,
            "numkids": counties[k]
        })

    with open('countydata.json', 'w', encoding='utf-8') as f:
        json.dump(county_data, f, ensure_ascii=False, indent=5)



def xlate_provider_name(name):
    nn = 'Not Specified'

    if name == 'Bethany':
        nn = 'Bethany Christian Services'
    elif name == 'Camelot':
        nn = 'Camelot'
    elif name == 'ChildHelp':
        nn = 'Child Help'
    elif name == 'DCS':
        nn = 'DCS (Knox Region)'
    elif name == 'DCS (ANDERSON)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (BLOUNT)':
        nn = 'DCS (Smoky Mountain Region)'
    elif name == 'DCS (CAMPBELL)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (CLAIRBON)':
        nn = 'DCS (Smoky Mountain Region)'
    elif name == 'DCS (EAST)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (GRAINGER)':
        nn = 'DCS (Smoky Mountain Region)'
    elif name == 'DCS (GREENE)':
        nn = 'DCS (Northeast Region)'
    elif name == 'DCS (HAWKINS)':
        nn = 'DCS (Northeast Region)'
    elif name == 'DCS (KNOX)':
        nn = 'DCS (Knox Region)'
    elif name == 'DCS (LOUDON)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (MONROE)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (MORGAN)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (ROANE)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (SCOTT)':
        nn = 'DCS (East Region)'
    elif name == 'DCS (SEVIER)':
        nn = 'DCS (Smoky Mountain Region)'
    elif name == 'DCS (SMOKY)':
        nn = 'DCS (Smoky Mountain Region)'
    elif name == 'DCS (Sevier)':
        nn = 'DCS (Smoky Mountain Region)'
    elif name == 'DCS (Union)':
        nn = 'DCS (East Region)'
    elif name == 'Destiny Adoptions':
        nn = 'Destiny Adoption Services'
    elif name == 'Florence Crittendon':
        nn = 'Florence Crittendon'
    elif name == 'Helen Ross McNabb':
        nn = 'Helen Ross McNabb'
    elif name == 'Holston Homes':
        nn = "Holston Homes"
    elif name == 'Hope Resource Center':
        nn = "Hope Resource Center"
    elif name == 'Kinship':
        nn = "Kinship"
    elif name == "Omni":
        nn = "OmniVision"
    elif name == 'Safe Families':
        nn = "Safe Families"
    elif name == 'Smoky Mountain Childrens Home':
        nn = "Smoky Mountain Children's Home"
    elif name == 'TBCH':
        nn = "Tennessee Baptist Children's Home"
    elif name == 'Youth Villages':
        nn = "Youth Villages"

    return nn


def csv_to_json(db):
    """ Load the CSV data from the prior years, convert to JSON and send to
    mongodb """

    visits = db.visits

    oldfile = "VisitLog.csv"
    reader = csv.DictReader(open(oldfile, 'r'))
    entries = []
    for line in reader:
        ts = line['\ufeffDate']
        line['timestamp'] = datetime.strptime(ts + " 11-00", "%b-%y %H-%M")
        line.pop('\ufeffDate', None)

        cl = line["Location"]
        if cl == "Knox":
            line["closetLocation"] = "Knoxville"
        else:
            line["closetLocation"] = "Oak Ridge"
        line.pop("Location", None)
        line.pop("State", None)
        line.pop("County", None)
        xlate_to_num(line, 'Kids Served')
        xlate_to_num(line, 'Num_Boys')
        xlate_to_num(line, 'Num_Girls')
        line['numKidsServed'] = int(line['Kids Served'])
        line.pop("Kids Served", None)
        line['numBoysServed'] = int(line.get('Num_Boys', 0))
        line.pop("Num_Boys", None)
        line['numGirlsServed'] = int(line.get('Num_Girls', 0))
        line.pop("Num_Girls", None)
        line['zipCode'] = line['ZipCode']
        line.pop("ZipCode", None)
        line['agencyConnection'] = line['Agency/Connection']
        line['agencyConnection'] = xlate_provider_name(line['agencyConnection'])
        line.pop("Agency/Connection", None)
        line['childrenAges0'] = bool(line['0yr'])
        line['childrenAges1'] = bool(line['1yr'])
        line['childrenAges2'] = bool(line['2yr'])
        line['childrenAges3'] = bool(line['3yr'])
        line['childrenAges4'] = bool(line['4yr'])
        line['childrenAges5'] = bool(line['5yr'])
        line['childrenAges6'] = bool(line['6yr'])
        line['childrenAges7'] = bool(line['7yr'])
        line['childrenAges8'] = bool(line['8yr'])
        line['childrenAges9'] = bool(line['9yr'])
        line['childrenAges10'] = bool(line['10yr'])
        line['childrenAges11'] = bool(line['11yr'])
        line['childrenAges12'] = bool(line['12yr'])
        line['childrenAges13'] = bool(line['13yr'])
        line['childrenAges14'] = bool(line['14yr'])
        line['childrenAges15'] = bool(line['15yr'])
        line['childrenAges16'] = bool(line['16yr'])
        line['childrenAges17'] = bool(line['17yr'])
        line['childrenAges18'] = bool(line['18yr'])
        line.pop("0yr", None)
        line.pop("1yr", None)
        line.pop("2yr", None)
        line.pop("3yr", None)
        line.pop("4yr", None)
        line.pop("5yr", None)
        line.pop("6yr", None)
        line.pop("7yr", None)
        line.pop("8yr", None)
        line.pop("9yr", None)
        line.pop("10yr", None)
        line.pop("11yr", None)
        line.pop("12yr", None)
        line.pop("13yr", None)
        line.pop("14yr", None)
        line.pop("15yr", None)
        line.pop("16yr", None)
        line.pop("17yr", None)
        line.pop("18yr", None)
        line.pop(">18yr", None)

        entries.append(line)
        #pprint.pprint(line)
        #break
    print("Sending entries to MongoDB...")
    for idx, entry in enumerate(entries):
        print("Sending entry %d" % idx)
        visits.insert_one(entry)

#
# This only needs to happen one time to get the data
# into the MongoDB
#
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
update_visits_with_zip(db)



#csv_to_json(db)



# Now, we want to get the children served by county and output that
#served_by_county(db)


# Next, we need to create a fancy map
#from colour import Color
#
#counties = {'Anderson': 42,
#             'Blount': 10,
#             'Grainger': 3,
#             'Jefferson': 4,
#             'Knox': 102,
#             'Loudon': 15,
#             'Monroe': 44,
#             'Roane': 6,
#             'Sevier': 17}
# counties = { 'Anderson': 280,
#            'Blount': 160,
#            'Campbell': 17,
#            'Claiborne': 25,
#            'Grainger': 35,
#            'Greene': 9,
#            'Hamblen': 13,
#            'Hawkins': 1,
#            'Jefferson': 34,
#            'Knox': 1245,
#            'Loudon': 111,
#            'McMinn': 4,
#            'Monroe': 79,
#            'Morgan': 2,
#            'Polk': 1,
#            'Roane': 85,
#            'Scott': 11,
#            'Sevier': 94,
#            'Union': 5}

# find max
# max = 0
# for key in counties.keys():
#     if counties[key] > max:
#         max = counties[key]

# print(max)

# white = Color("lightblue")
# blue = Color("darkblue")
# blues = list(white.range_to(blue, max + 1))
#pprint.pprint(colors)

# for key in counties.keys():
#     my_blue = blues[counties[key]]
#     print("%s\t%s" % (key, my_blue))




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
