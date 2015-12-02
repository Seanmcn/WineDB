from django.core.management.base import BaseCommand, CommandError
from src.models import History, Wines
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    help = 'Harvests the wine from JoshLikesWine.com'

    def handle(self, *args, **options):
        posts = set()
        pages = 37  # Current WP page count on JLW.

        # Get all the JLW WP posts
        for x in range(1, pages + 1):
            page = 'http://www.joshlikeswine.com/page/' + str(x)
            req = requests.get(page)
            soup = BeautifulSoup(req.content, 'html.parser')
            post_titles = soup.findAll('h2', class_='eltdf-post-title')
            for post_title in post_titles:
                posts.add(post_title.find('a')['href'])

        self.stdout.write('Harvested')
