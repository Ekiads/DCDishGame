# import statements

import requests
import pandas as pd
from json import loads
import time
from bs4 import BeautifulSoup
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

def scrape_cuarto_dc_menu(verbose=False):
    url = "https://housing.ucdavis.edu/dining/menus/dining-commons/cuarto/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    menu = {}
    current_day = None
    current_meal = None
    current_station = None

    valid_meals = ['Breakfast', 'Lunch', 'Dinner', 'Late Night']

    for tag in soup.find_all(['h3', 'h4', 'h5', 'ul']):
        if tag.name == 'h3':
            current_day = tag.get_text(strip=True)
            if ',' in current_day:
                menu[current_day] = {}
            else:
                current_day = None
        elif tag.name == 'h4':
            text = tag.get_text(strip=True)
            if text in valid_meals and current_day:
                current_meal = text
                menu[current_day][current_meal] = {}
            else:
                current_meal = None
        elif tag.name == 'h5':
            if current_day and current_meal:
                current_station = tag.get_text(strip=True)
                menu[current_day][current_meal][current_station] = []
        elif tag.name == 'ul':
            if current_day and current_meal and current_station:
                for li in tag.find_all('li'):
                    if 'trigger' in li.get('class', []):
                        span = li.find('span')
                        if span:
                            dish_name = span.get_text(strip=True)

                            nutrition = li.find('ul', class_='nutrition')
                            description = None
                            if nutrition:
                                p_tag = nutrition.find('p')
                                if p_tag:
                                    desc_text = p_tag.get_text(strip=True)
                                    if not any(char.isdigit() for char in desc_text) and desc_text.lower() != ": n/a":
                                        description = desc_text

                            if dish_name:
                                menu[current_day][current_meal][current_station].append({
                                    'name': dish_name,
                                    'description': description
                                })

    if verbose:
        for day, meals in menu.items():
            print(f"\n{day}")
            for meal, stations in meals.items():
                print(f"  {meal}")
                for station, dishes in stations.items():
                    print(f"    {station}")
                    for dish in dishes:
                        print(f"      - {dish['name']}")
                        if dish['description']:
                            print(f"        {dish['description']}")

    return menu


def upload_menu_to_db(menu, service_account_path):
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    for date, meals in menu.items():
        for meal_type, locations in meals.items():
            for section, dishes in locations.items():
                for dish in dishes:
                    name = dish["name"]
                    desc = dish.get("description")

                    dish_doc_ref = db.collection("dishes").document(name)

                    doc = dish_doc_ref.get()
                    if doc.exists:
                        dish_doc_ref.update({
                            "dates": firestore.ArrayUnion([{
                                "date": date,
                                "meal": meal_type,
                                "sectionID": section,
                                "dishName": name
                            }])
                        })
                    else:
                        dish_doc_ref.set({
                            "description": desc,
                            "dates": [{
                                "date": date,
                                "meal": meal_type,
                                "sectionID": section,
                                "dishName": name
                            }]
                        })

