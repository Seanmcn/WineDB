from django.core.management.base import BaseCommand, CommandError
from src.models import History, Wines
from bs4 import BeautifulSoup
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

        # for post in posts:
        #     print(post)
        #     exit()

        # new format: http://www.joshlikeswine.com/2015/11/08/canadian-wines-with-rhodanien-and-tuscan-influence/
        # old format: http://www.joshlikeswine.com/2012/05/07/2010-tranchero-moscato-dasti/
        req = requests.get('http://www.joshlikeswine.com/2012/05/07/2010-tranchero-moscato-dasti/')
        soup = BeautifulSoup(req.content, 'html.parser')
        article = soup.find('article')

        new_format_regex = re.compile(r"""<p><strong>(.*?)<\/strong>(.*?)<br>(.*?)<\/p>""", re.M | re.S)
        results = new_format_regex.findall(str(article))

        if not results:
            old_format_regex = re.compile(r"""<strong>(.*)<\/strong>(.*)<""", re.M)
            results = old_format_regex.findall(str(article))

        print(results)

        self.stdout.write('Harvested')
