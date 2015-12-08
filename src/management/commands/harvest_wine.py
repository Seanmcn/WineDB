from django.core.management.base import BaseCommand, CommandError
from src.models import History, Wines
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
import requests
import re
import datetime


class Command(BaseCommand):
    help = 'Harvests the wine from JoshLikesWine.com'

    def handle(self, *args, **options):
        posts = set()
        pages = 37  # Current WP page count on JLW.

        # Get all the JLW WP posts

        # for x in range(1, pages + 1):
        #     page = 'http://www.joshlikeswine.com/page/' + str(x)
        #     req = requests.get(page)
        #     soup = BeautifulSoup(req.content, 'html.parser')
        #     post_titles = soup.findAll('h2', class_='eltdf-post-title')
        #     for post_title in post_titles:
        #         posts.add(post_title.find('a')['href'])

        #####################
        # Process each post #
        #####################

        # for post in posts:
        #     print(post)
        #     exit()

        # new format: http://www.joshlikeswine.com/2015/11/08/canadian-wines-with-rhodanien-and-tuscan-influence/
        # old format: http://www.joshlikeswine.com/2012/05/07/2010-tranchero-moscato-dasti/

        # single
        # req = requests.get('http://www.joshlikeswine.com/2012/05/07/2010-tranchero-moscato-dasti/')
        # single 2
        # req = requests.get('http://www.joshlikeswine.com/2014/01/13/2012-artero-macabeo-verdejo/')
        # single 3
        req = requests.get(
            'http://www.joshlikeswine.com/2014/12/22/cantina-valpantena-2012-torre-del-falasco-valpolicella-ripasso/')

        # multi 1
        # req = requests.get('http://www.joshlikeswine.com/2015/11/08/canadian-wines-with-rhodanien-and-tuscan-influence/')
        # multi 2
        # req = requests.get('http://www.joshlikeswine.com/2015/12/02/16-wines-to-pair-with-your-disappointing-new-years-resolutions-of-2016/')

        soup = BeautifulSoup(req.content, 'html.parser')

        ##########################################################
        # Work out the wine name for if it's a single wine post. #
        ##########################################################
        h2_title = soup.find('h2', class_='eltdf-post-title')
        title_regex = re.compile(r""":(.*)""")  # Regex for Witty Title : Wine Name
        alt_regex = re.compile(r""">(.*)</h2>""", re.M | re.S)  # Regex for title that is just wine.
        title = title_regex.findall(str(h2_title))  # Try first regex.
        if not title:
            # If that's failed try alternative regex
            title = alt_regex.findall(str(h2_title))
            if not title:
                # Last resort, title unknown
                title = 'Unknown'
            else:
                title = title[0]
        else:
            title = title[0]

        title = strip_tags(title).strip()  # Strip any leftover HTML

        #########################
        # Try get the wine data #
        #########################
        article = soup.find('article')
        tags = soup.find('div', class_="eltdf-tags").getText().replace('/', ', ')

        # Figure out if single or multi wine post by searching for tasting note
        tasting_search = re.compile(r"""(tasting note)""", re.I)
        is_tasting = tasting_search.findall(str(article))

        if is_tasting:
            # Single wine post
            single_wine_descrip = re.compile(r"""<p><strong>|<p.*?>(.*?)<\/p>""", re.M | re.S)
            single_wine_regex = re.compile(r"""<strong>(.*?)<\/strong>(.*?)(?=<)""", re.M | re.S)
            results = single_wine_regex.findall(str(article))
            descrip_results = single_wine_descrip.findall(str(article))

            color, eyes, nose, mouth, overall, producer = ('N/A',) * 6
            price = 0
            region, sub_region, variety, vintage, description, abv = ('',) * 6

            h = History.objects.get(url='http://www.joshlikeswine.com/2014/01/13/2012-artero-macabeo-verdejo/')

            # Try figure out the colour
            if ('white' in tags) or ('White' in tags):
                color = 'White'
            if ('red' in tags) or ('Red' in tags):
                color = 'Red'

            # Process single-wine results
            if results:
                for key, value in results:
                    value_soup = BeautifulSoup(value, 'html.parser')
                    value = value_soup.getText()
                    key_soup = BeautifulSoup(key, 'html.parser')
                    key = key_soup.getText()

                    if ("Eyes" in key) or ("eyes" in key):
                        eyes = value
                    elif ("Nose" in key) or ("nose" in key):
                        nose = value
                    elif ("Mouth" in key) or ("mouth" in key):
                        mouth = value
                    elif ("All in all" in key) or ("all in all" in key):
                        overall = value
                    elif ("Producer" in key) or ("producer" in key):
                        producer = value
                    elif ("Price" in key) or ("price" in key):
                        price = value.replace("$", "")
                    elif ("Sub-Region" in key) or ("sub-region" in key):
                        sub_region = value
                    elif ("Region" in key) or ("region" in key):
                        region = value
                    elif ("Variety" in key) or ("variety" in key):
                        variety = value
                    elif ("Vintage" in key) or ("vintage" in key):
                        vintage = value
                    elif ("ABV" in key) or ("abv" in key):
                        abv = value

                description_soup = BeautifulSoup(' '.join(descrip_results), 'html.parser')
                description = description_soup.getText()

                w = Wines(name=title, color=color, eyes=eyes, nose=nose, mouth=mouth, overall=overall,
                          producer=producer, price=price, region=region, sub_region=sub_region, variety=variety,
                          vintage=vintage, abv=abv, description=description, tags=tags, harvest_data=str(article),
                          harvested_from=h,
                          harvested_date=datetime.datetime.now(datetime.timezone.utc))
                w.save()

        else:
            # Multi wine post
            multi_wine_regex = re.compile(
                r"""<p><(.*?)<\/strong>(.*?)(<br>|<br\/>)(.*?)<\/p>""",
                re.M | re.S | re.I)
            results = multi_wine_regex.findall(str(article))

            # Process multi-wine results
            if results:
                for result in results:
                    print(result)

        exit()

        self.stdout.write('Harvested')
