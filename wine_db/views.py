# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, render
from .models import Wine
from .models import History
import json

def json_file(request):
    if request.GET and request.GET['refresh'] == 'true':
        wines = Wine.objects.all()

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
                     "harvested_from": str(wine.harvested_from), "count": 1})
            if "White" in wine.color:
                if wine.variety not in white_berry_dict:
                    white_berry_dict[wine.variety] = []
                white_berry_dict[wine.variety].append(
                    {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                     "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                     "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                     "harvested_from": str(wine.harvested_from), "count": 1})
            if "Rosé" in wine.color:
                if wine.variety not in rose_berry_dict:
                    rose_berry_dict[wine.variety] = []
                rose_berry_dict[wine.variety].append(
                    {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                     "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                     "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                     "harvested_from": str(wine.harvested_from), "count": 1})
            if "N/A" in wine.color:
                if wine.variety not in unknown_berry_dict:
                    unknown_berry_dict[wine.variety] = []
                unknown_berry_dict[wine.variety].append(
                    {"name": wine.name, "eyes": wine.eyes, "nose": wine.nose, "mouth": wine.mouth, "overall": wine.overall,
                     "producer": wine.producer, "abv": wine.abv, "region": wine.region, "sub_region": wine.sub_region,
                     "variety": wine.variety, "vintage": wine.vintage, "price": wine.price, "description": wine.description,
                     "harvested_from": str(wine.harvested_from), "count": 1})

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
    if request.GET and request.GET['refresh'] == 'true':
        wines = Wine.objects.all()

        data = []
        for wine in wines:
            wine.variety = wine.variety.strip()
            if not wine.variety or wine.variety is '':
                wine.variety = 'N/A'

            if wine.abv is '':
                wine.abv = 'N/A'

            if wine.vintage is '':
                wine.vintage = 'N/A'

            if wine.price is '0' or wine.price is 0 or not wine.price:
                wine.price = 'N/A'
            else :
                wine.price = '$' + str(wine.price)

            if wine.region is '':
                wine.region = 'N/A'

            if wine.sub_region is '':
                wine.sub_region = 'N/A'

            if wine.eyes is '':
                wine.eyes = 'N/A'

            if wine.nose is '':
                wine.nose = 'N/A'

            if wine.mouth is '':
                wine.mouth = 'N/A'

            if wine.producer is '':
                wine.producer = 'N/A'

            wine.description = str(wine.description).strip()
            if wine.description is '' or not wine.description:
                wine.description = 'N/A'

            wine_dict = dict()
            wine_dict['name'] = str(wine.name).strip()
            wine_dict['color'] = str(wine.color).strip()
            wine_dict['price'] = str(wine.price).strip()
            wine_dict['abv'] = str(wine.abv).strip()
            wine_dict['region'] = str(wine.region).strip()
            wine_dict['sub_region'] = str(wine.sub_region).strip()
            wine_dict['eyes'] = str(wine.eyes).strip()
            wine_dict['nose'] = str(wine.nose).strip()
            wine_dict['mouth'] = str(wine.mouth).strip()
            wine_dict['overall'] = str(wine.overall).strip()
            wine_dict['producer'] = str(wine.producer).strip()
            wine_dict['vintage'] = str(wine.vintage).strip()
            wine_dict['producer'] = str(wine.producer).strip()
            wine_dict['variety'] = str(wine.variety).strip()
            wine_dict['description'] = str(wine.description)

            wine_dict['link'] = "<a href='" + str(wine.harvested_from) + "' target='_blank'>" + str(
                wine.harvested_from) + "</a>"

            data.append(wine_dict)

        formatted_data = {'data': data}

        with open('templates/wine_db/data-tables.json', 'w', encoding='utf8') as text_file:
            json.dump(formatted_data, text_file, ensure_ascii=False)

    return render(request, 'wine_db/data-tables.json')
