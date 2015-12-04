from django.core.management.base import BaseCommand, CommandError
from src.models import History, Wines
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
import requests
import re


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
        # multi 1
        req = requests.get('http://www.joshlikeswine.com/2015/11/08/canadian-wines-with-rhodanien-and-tuscan-influence/')
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

        # Figure out if single or multi wine post by searching for tasting note
        tasting_search = re.compile(r"""(tasting note)""", re.I)
        is_tasting = tasting_search.findall(str(article))

        if is_tasting:
            # Single wine post
            single_wine_regex = re.compile(r"""<strong>(.*)<\/strong>(.*)<""", re.M)
            results = single_wine_regex.findall(str(article))

            # Process single-wine results
            if results:
                for result in results:
                    print(result)

        else:
            # Multi wine post
            multi_wine_regex = re.compile(
                r"""<p><(.*?)<\/strong>(.*?)(<br>|<br\/>)(.*?)<\/p>""",
                re.M | re.S | re.I)
            results = multi_wine_regex.findall(str(article))

            # print(article)
            # Process multi-wine results
            if results:
                for result in results:
                    print(result)

        exit()

        self.stdout.write('Harvested')
