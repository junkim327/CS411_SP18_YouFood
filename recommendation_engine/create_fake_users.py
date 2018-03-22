from datetime import datetime, timedelta

from tqdm import tqdm

categories = ["Scandinavian",
              "Cheese Shops",
              "Soul Food",
              "Southern",
              "Beverage Store",
              "Mexican",
              "Fish & Chips",
              "Bakeries",
              "Whiskey Bars",
              "Egyptian",
              "Breweries",
              "Beer Gardens",
              "Seafood Markets",
              "French",
              "Cafes",
              "Hawaiian",
              "Gastropubs",
              "Pubs",
              "Syrian",
              "Specialty Food",
              "Arabian",
              "Tapas Bars",
              "Szechuan",
              "Portuguese",
              "Puerto Rican",
              "Beer, Wine & Spirits",
              "Modern European",
              "Shaved Ice",
              "Steakhouses",
              "Fondue",
              "Vegan",
              "Chicken Wings",
              "Filipino",
              "Poke",
              "Moroccan",
              "Japanese",
              "Austrian",
              "Fast Food",
              "Pop-Up Restaurants",
              "Noodles",
              "Vegetarian",
              "Karaoke",
              "Sardinian",
              "Tapas/Small Plates",
              "Czech",
              "Patisserie/Cake Shop",
              "Himalayan/Nepalese",
              "Polish",
              "Cheesesteaks",
              "Italian",
              "Russian",
              "Taiwanese",
              "Pizza",
              "Pasta Shops",
              "International Grocery",
              "Chinese",
              "Hot Dogs",
              "Champagne Bars",
              "Cajun/Creole",
              "Empanadas",
              "Beer Bar",
              "Coffee & Tea",
              "Belgian",
              "Jazz & Blues",
              "Thai",
              "Armenian",
              "Venues & Event Spaces",
              "Food Stands",
              "Caribbean",
              "Halal",
              "Malaysian",
              "Live/Raw Food",
              "Peruvian",
              "Pakistani",
              "Afghan",
              "Kebab",
              "Mongolian",
              "Tex-Mex",
              "Comfort Food",
              "Bubble Tea",
              "Themed Cafes",
              "Dim Sum",
              "Wine Bars",
              "Cuban",
              "Tea Rooms",
              "African",
              "Venezuelan",
              "Juice Bars & Smoothies",
              "Supper Clubs",
              "Dance Clubs",
              "Burmese",
              "Cantonese",
              "Hot Pot",
              "Basque",
              "Shanghainese",
              "Cocktail Bars",
              "Indonesian",
              "Korean",
              "Waffles",
              "Singaporean",
              "Barbeque",
              "Pan Asian",
              "British",
              "Grocery",
              "Performing Arts",
              "Salvadoran",
              "Diners",
              "Ice Cream & Frozen Yogurt",
              "Middle Eastern",
              "Mediterranean",
              "Vietnamese",
              "Brazilian",
              "Gelato",
              "Gluten-Free",
              "Argentine",
              "Laotian",
              "Food Trucks",
              "Teppanyaki",
              "Desserts",
              "Creperies",
              "Chicken Shop",
              "Cambodian",
              "Latin American",
              "Turkish",
              "Sandwiches",
              "Indian",
              "Tacos",
              "Burgers",
              "Spanish",
              "Ethiopian",
              "Seafood",
              "Conveyor Belt Sushi",
              "American (Traditional)",
              "Lounges",
              "Ramen",
              "Hungarian",
              "Cideries",
              "German",
              "Salad",
              "Brasseries",
              "Persian/Iranian",
              "Kosher",
              "Arcades",
              "Lebanese",
              "Falafel",
              "Tiki Bars",
              "Asian Fusion",
              "Greek",
              "New Mexican Cuisine",
              "American (New)",
              "Dive Bars",
              "Delis",
              "Izakaya",
              "Soup",
              "Eatertainment",
              "Breakfast & Brunch",
              "Meat Shops",
              "Japanese Curry",
              "Bars",
              "Sports Bars",
              "Sushi Bars", ]

import psycopg2
from random import choices, random

connection = psycopg2.connect(dbname="youfood", user="youfood", password="wizard11", host="localhost")

users_list = []
names_list = []
tastes_list = []
for i in range(2000):
    users_list += [f"test{i}@illinois.net"]
    names_list += [f"Test {i}"]
    tastes_list += [choices(categories, k=3)]

with connection as conn:
    with conn.cursor() as cur:
        for email, username, tastes in tqdm(zip(users_list, names_list, tastes_list)):
            cur.execute("""SELECT restaurant_name, restaurant_address FROM "RestaurantCategories"
                            WHERE category = %s
                            OR category = %s
                            OR category = %s
                        ORDER BY random() ASC LIMIT 10;""", tastes)
            tuples = cur.fetchall()
            cur.execute("""INSERT INTO "User"(email, name, hashedpass) VALUES (%s, %s, %s);""",
                        [email, username, "123"])
            subinserts = []
            for name, address in tuples:
                subinserts += [
                    f"""(%s, {repr(email)}, {20}, '{name.replace("'", "''")}', '{address.replace("'", "''")}')"""]
            start = datetime.now()
            end = start + timedelta(hours=1)
            nows = [start + (end - start) * random() for _ in range(len(tuples))]
            g_query = f"""INSERT INTO "Transaction" VALUES {", ".join(subinserts)};"""
            cur.execute(g_query, nows)
        conn.commit()
