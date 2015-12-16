from django.shortcuts import render_to_response
from .models import Wine
import json


def index(request):
    return render_to_response('wine_db/index.html')


def json_file(request):
    wines = Wine.wines.all()

    data = {}

    colors = []
    whites = []
    riesling = []

    riesling.append({"name": "Dr Loosen", "count": 1})
    whites.append({"name": "riesling", "children": riesling})
    colors.append({"name": "white", "children": whites})
    data['children'] = colors
    data['name'] = 'color'

    # wine -> berry -> color

    # for wine in wines:
        # print(wine)

    with open('templates/wine_db/data.json', 'w') as text_file:
        json.dump(data, text_file, ensure_ascii=False)

    return render_to_response('wine_db/data.json')
