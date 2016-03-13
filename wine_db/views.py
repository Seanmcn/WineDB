from django.shortcuts import render_to_response
from .models import Wine
import json


def index(request):
    return render_to_response('wine_db/home.html')


def json_file(request):
    wines = Wine.wines.all()

    red_by_berry = []
    white_by_berry = []
    rose_by_berry = []
    unknown_by_berry = []

    white_berry_dict = {}
    red_berry_dict = {}
    rose_berry_dict = {}
    unknown_berry_dict = {}

    for wine in wines:
        wine.variety = wine.variety.strip()
        if not wine.variety or wine.variety is '':
            wine.variety = 'N/A'

        if "Red" in wine.color:
            if wine.variety not in red_berry_dict:
                red_berry_dict[wine.variety] = []
            red_berry_dict[wine.variety].append(
                {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                 "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                 "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                 "count": 1})
        if "White" in wine.color:
            if wine.variety not in white_berry_dict:
                white_berry_dict[wine.variety] = []
            white_berry_dict[wine.variety].append(
                {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                 "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                 "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                 "count": 1})
        if "Rosé" in wine.color:
            if wine.variety not in rose_berry_dict:
                rose_berry_dict[wine.variety] = []
            rose_berry_dict[wine.variety].append(
                {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                 "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                 "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                 "count": 1})
        if "N/A" in wine.color:
            if wine.variety not in unknown_berry_dict:
                unknown_berry_dict[wine.variety] = []
            unknown_berry_dict[wine.variety].append(
                {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                 "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                 "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                 "count": 1})

    for key, value in red_berry_dict.items():
        red_by_berry.append({"name": key, "children": value})

    for key, value in white_berry_dict.items():
        white_by_berry.append({"name": key, "children": value})

    for key, value in rose_berry_dict.items():
        rose_by_berry.append({"name": key, "children": value})

    for key, value in unknown_berry_dict.items():
        unknown_by_berry.append({"name": key, "children": value})

    colors = []
    colors.append({"name": "White", "children": white_by_berry, "color": "#00A6ED"})
    colors.append({"name": "Red", "children": red_by_berry, "color": "#DD1C1A"})
    colors.append({"name": "Rose", "children": rose_by_berry, "color": "#D90368"})
    colors.append({"name": "N/A", "children": unknown_by_berry, "color": "#000000"})

    data = {}
    data['children'] = colors
    data['name'] = ''

    with open('templates/wine_db/data.json', 'w') as text_file:
        json.dump(data, text_file, ensure_ascii=True)

    return render_to_response('wine_db/data.json')


def json_dt(request):
    wines = Wine.wines.all()

    data = []
    for wine in wines:
        wine.variety = wine.variety.strip()
        if not wine.variety or wine.variety is '':
            wine.variety = 'N/A'
            
        data.append(
            [wine.name, wine.color, wine.variety, wine.price, wine.abv, wine.region, wine.sub_region,
             wine.eyes, wine.nose, wine.mouth, wine.overall, wine.producer, wine.vintage, wine.description
             ])

    with open('templates/wine_db/data-tables.json', 'w') as text_file:
        json.dump(data, text_file, ensure_ascii=True)

    return render_to_response('wine_db/data-tables.json')
