from credentials import USER, PASSWORD, DATABASE, HOST
import psycopg2
import json
from pprint import pprint

FILENAME = 'data.json'

data = json.load(open(FILENAME))
businesses = data['businesses']

conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST)
cur = conn.cursor()

for business in businesses:
    # insert restaurant
    cur.execute('''
    INSERT INTO Restaurant (address, pricerange, cuisine, name, phone, image_url) 
    VALUES (%s, %d, %s, %s, %s, %s)
    ''',
                (business['location']['display_address'], len(business['price']), business['categories'][0]['title'],
                 business['name'], business['display_phone'], business['image_url']))
    # insert categories
    for category in business['categories']:
        cur.execute('''
        INSERT INTO RestaurantCategories (restaurant, category) 
        VALUES (%s, %s)
        ''',
                    (business['location']['display_address'], category['title']))

    

# For present purposes, I use the first item in categories as the cuisine. It should be a list that links to another table but for now this is should get us started
# Note also that I use display_phone instead of the normal phone

"""
SAMPLE ENTRY
{ 'categories': [ {'alias': 'vietnamese', 'title': 'Vietnamese'},
                    {'alias': 'chinese', 'title': 'Chinese'},
                    {'alias': 'noodles', 'title': 'Noodles'}],
    'coordinates': {'latitude': 37.76368, 'longitude': -122.46879},
    'display_phone': '(415) 566-4722',
    'distance': 2863.684176093556,
    'id': 'yummy-yummy-san-francisco',
    'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/iNtuo93WsV9t8dU3Njiwbw/o.jpg',
    'is_closed': False,
    'location': { 'address1': '1015 Irving St',
                  'address2': '',
                  'address3': '',
                  'city': 'San Francisco',
                  'country': 'US',
                  'display_address': [ '1015 Irving St',
                                       'San Francisco, CA 94122'],
                  'state': 'CA',
                  'zip_code': '94122'},
    'name': 'Yummy Yummy',
    'phone': '+14155664722',
    'price': '$$',
    'rating': 4.0,
    'review_count': 1263,
    'transactions': ['pickup', 'delivery'],
    'url': 'https://www.yelp.com/biz/yummy-yummy-san-francisco?adjust_creative=09CWf82V7c_xrYOTHH6wKw&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=09CWf82V7c_xrYOTHH6wKw'}

"""




