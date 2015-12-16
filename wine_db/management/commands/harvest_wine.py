from django.core.management.base import BaseCommand, CommandError
from wine_db.models import History, Wine
from bs4 import BeautifulSoup
from django.utils.html import strip_tags
import requests
import re
import datetime


class Command(BaseCommand):
    help = 'Harvests the wine from JoshLikesWine.com'

    def add_arguments(self, parser):

        parser.add_argument('--update_urls',
                            action='store_true',
                            default=False,
                            help='Truncate and remake the post_urls.txt file')

    @staticmethod
    def create_single_wine(wine, title, url, article, tags):

        color, eyes, nose, mouth, overall, producer = ('N/A',) * 6
        price = 0
        region, sub_region, variety, vintage, description, abv = ('',) * 6

        h = History(url=url, wine_count=1, date=datetime.datetime.now(datetime.timezone.utc))
        h.save()

        # Description
        single_wine_descrip = re.compile(r"""<p><strong>|<p.*?>(.*?)<\/p>""", re.M | re.S)
        descrip_results = single_wine_descrip.findall(str(article))
        description_soup = BeautifulSoup(' '.join(descrip_results), 'html.parser')
        description = description_soup.getText()

        # Try figure out the colour
        if ('white' in tags) or ('White' in tags):
            color = 'White'
        if ('red' in tags) or ('Red' in tags):
            color = 'Red'

        # Process single-wine results
        if wine:
            for key, value in wine:
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

            w = Wine(name=title, color=color, eyes=eyes, nose=nose, mouth=mouth, overall=overall,
                      producer=producer, price=price, region=region, sub_region=sub_region, variety=variety,
                      vintage=vintage, abv=abv, description=description, tags=tags,
                      harvest_data=str(article),
                      harvested_from=h,
                      harvested_date=datetime.datetime.now(datetime.timezone.utc))
            w.save()

    @staticmethod
    def create_multi_wines(wines, url, article, tags):

        # Regex
        title_regex = re.compile(r"""<strong>(.*)""", re.M | re.S | re.I)
        alt_title_regex = re.compile(r"""<span .*>(.*?)</span>""")
        # Create history
        h = History(url=url, wine_count=len(wines), date=datetime.datetime.now(datetime.timezone.utc))
        h.save()
        print("Length of wines:" + str(len(wines)))

        for wine in wines: # ['title', 'subregion/region price', 'description']
            print(wine)
            title = title_regex.findall(wine[0])
            if title:
                title = title[0]
            else:
                title = alt_title_regex.findall(wine[0])
                if not title:
                    # If there is no title there is no wine so break this loop
                    print("No wine??")
                    h.wine_count -= 1
                    h.save()
                    continue

            title = strip_tags(title)
            color, eyes, nose, mouth, overall, producer = ('N/A',) * 6
            price = 0
            region, sub_region, variety, vintage, description, abv = ('',) * 6

            if 'Riesling' in title:
                variety = 'Riesling'
            elif 'Chardonnay' in title:
                variety = 'Chardonnay'
            elif 'Sauvignon Blanc' in title:
                variety = 'Sauvignon Blanc'
            elif 'Syrah' in title:
                variety = 'Syrah'
            elif 'Shiraz' in title:
                variety = 'Shiraz'
            elif 'Cabernet Sauvignon' in title:
                variety = 'Cabernet Sauvignon'
            elif 'Merlot' in title:
                variety = 'Merlot'
            elif 'Pinot Noir' in title:
                variety = 'Pinot Noir'
            else:
                variety = ''

            if '#ff99cc' in wine[0]:
                color = 'Rosé'
            if '#339966' in wine[0]:
                color = 'White'
            if '#800000' in wine[0]:
                color = 'Red'

            region_price_regex = re.compile(r"""\((.*?)\) \$(.+)|\((.*?)\)""", re.M | re.S | re.I)
            region_price = region_price_regex.findall(wine[1])
            total_region = []
            if region_price:
                region_price = region_price[0]

                if region_price[0]:
                    total_region = region_price[0]

                if region_price[1]:
                    price = region_price[1]

                if region_price[2]:
                    total_region = region_price[2]

                # print('TOTAL REGION')

                if total_region:
                    region_list = total_region.split(',')
                    # print(len(region_list))
                    region_count = len(region_list)
                    if region_count is 1:
                        region = region_list[0].strip()
                    elif region_count is 2:
                        region = region_list[1].strip()
                        sub_region = region_list[0].strip()
                    elif region_count > 2:
                        # print(region_list)
                        region_number = region_count - 1
                        sub_region_number = region_count - 2
                        alt_sub_region_number = region_count - 3

                        region = region_list[region_number].strip()
                        # print(region)

                        sub_region = region_list[alt_sub_region_number].strip() + ", " + region_list[sub_region_number].strip()
                        # print(sub_region)
                            # print(total_region)
            # exit()
            description = str(wine[2].strip())

            w = Wine(name=title, color=color, eyes=eyes, nose=nose, mouth=mouth, overall=overall,
                      producer=producer, price=price, region=region, sub_region=sub_region,
                      variety=variety,
                      vintage=vintage, abv=abv, description=str(description), tags=str(tags),
                      harvest_data=str(article),
                      harvested_from=h,
                      harvested_date=datetime.datetime.now(datetime.timezone.utc))
            w.save()
        return True

    @staticmethod
    def create_multi_wines_exception_a(url, article):
        wines_regex = re.compile(r"""<span style="text-decoration: underline;">(.*?)(?=<span)""",
                                 re.M | re.S | re.I)
        wines = wines_regex.findall(str(article))

        title_regex = re.compile(r"""<strong>(.*?) –""")
        wine_info_regex = re.compile(r"""<strong>(.*?)<\/strong>(.*?)(?=<)""", re.I | re.M | re.S)

        h = History(url=url, wine_count=len(wines), date=datetime.datetime.now(datetime.timezone.utc))
        h.save()

        for wine in wines:
            info = wine_info_regex.findall(wine)

            color, eyes, nose, mouth, overall, producer = ('N/A',) * 6
            price = 0
            region, sub_region, variety, vintage, description, abv = ('',) * 6

            title = title_regex.findall(wine)

            if title:
                title = title[0]
            else:
                print("Couldn't determine title!")
                continue

            if 'Riesling' in title:
                variety = 'Riesling'
            elif 'Chardonnay' in title:
                variety = 'Chardonnay'
            elif 'Sauvignon Blanc' in title:
                variety = 'Sauvignon Blanc'
            elif 'Syrah':
                variety = 'Syrah'
            elif 'Shiraz':
                variety = 'Shiraz'
            elif 'Cabernet Sauvignon':
                variety = 'Cabernet Sauvignon'
            elif 'Merlot':
                variety = 'Merlot'
            elif 'Pinot Noir':
                variety = 'Pinot Noir'

            for key, value in info:
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

            w = Wine(name=title, color=color, eyes=eyes, nose=nose, mouth=mouth, overall=overall,
                      producer=producer, price=price, region=region, sub_region=sub_region,
                      variety=variety,
                      vintage=vintage, abv=abv, description=description, tags='',
                      harvest_data=str(article),
                      harvested_from=h,
                      harvested_date=datetime.datetime.now(datetime.timezone.utc))
            w.save()

    def handle(self, *args, **options):
        posts = set()
        pages = 37  # Current WP page count on JLW. // 369 posts currently

        # Create text file of all the JLW post URLs
        if options['update_urls']:
            # Truncate the file.
            open('post_urls.txt', 'w')
            # Loop through blog pages
            for x in range(1, pages + 1):
                print("Getting page " + str(x))
                page = 'http://www.joshlikeswine.com/page/' + str(x)
                req = requests.get(page)
                soup = BeautifulSoup(req.content, 'html.parser')
                post_titles = soup.findAll('h2', class_='eltdf-post-title')
                for post_title in post_titles:
                    # Add URL to file
                    with open("post_urls.txt", "a") as text_file:
                        print(format(post_title.find('a')['href']), file=text_file)
                    posts.add(post_title.find('a')['href'])

        # Load post_urls.txt into list
        for line in open("post_urls.txt", "r"):
            posts.add(line.strip('\n'))

        #####################
        # Process each post #
        #####################
        exceptions = set()
        exceptions.add('http://www.joshlikeswine.com/2015/03/25/wset-diploma-unit-3-week-18-workshop-4/')
        exceptions.add('http://www.joshlikeswine.com/2012/12/06/bud-break-2013-winter-courses/')
        exceptions.add('http://www.joshlikeswine.com/2015/11/18/looking-to-bone-in-beaune/')

        no_wine = set()
        no_wine.add('http://www.joshlikeswine.com/2012/12/06/bud-break-2013-winter-courses/')
        no_wine.add('http://www.joshlikeswine.com/2013/06/15/wset-diploma-section-1-week-10/')
        no_wine.add('http://www.joshlikeswine.com/2014/10/08/wset-diploma-unit-3-week-1/')
        no_wine.add('http://www.joshlikeswine.com/2012/05/29/wset-advanced-course/')
        no_wine.add('http://www.joshlikeswine.com/2015/02/26/vancouver-international-wine-festival-2015-decades-apart/')
        no_wine.add('http://www.joshlikeswine.com/2013/03/29/wines-to-pair-with-people-that-you-want-to-die/bitterwine/')
        no_wine.add('http://www.joshlikeswine.com/2013/01/05/2013-term-2-week-1-omg-course-outlines/')

        multi_wine_list = set()
        multi_wine_list.add('http://www.joshlikeswine.com/2015/09/16/josh-tastes-41-new-york-wines/')
        multi_wine_list.add('http://www.joshlikeswine.com/2015/09/18/josh-tastes-118-wines-at-top-drop/')

        single_wine_list = set()

        # # DEBUG##
        # posts = set()
        # posts.add('http://www.joshlikeswine.com/2015/11/18/looking-to-bone-in-beaune/') # todo: might become new standard regex perhaps?
        # posts.add('http://www.joshlikeswine.com/2015/09/18/josh-tastes-118-wines-at-top-drop/') # todo: working exception multi wine
        # http://www.joshlikeswine.com/2015/06/10/exams-and-grand-slams/ #check, had length zero in multi wine?
        # http://www.joshlikeswine.com/2014/07/31/wine-bloggers-conference-2014-blends-2-2-5/ #todo: failing multi wine
        # http://www.joshlikeswine.com/2015/08/17/josh-is-alone-in-new-york-city-day-1/ #todo : needs special attention

        ##END DEBUG##

        for url in posts:
            # Request URL and get article
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')
            article = soup.find('article')

            # Find the post tags
            tags = soup.find('div', class_="eltdf-tags")
            if tags:
                tags = tags.getText().replace('/', ', ')
            else:
                tags = ''

            # Handle exceptions
            if url in exceptions:
                if url in no_wine:
                    print('No wine on: ' + url)
                    h = History(url=url, wine_count=0, date=datetime.datetime.now(datetime.timezone.utc))
                    h.save()
                    continue
                elif url == 'http://www.joshlikeswine.com/2015/03/25/wset-diploma-unit-3-week-18-workshop-4/':
                    print('Processing Exception: ' + url)
                    Command.create_multi_wines_exception_a(url, article)
                elif url == 'http://www.joshlikeswine.com/2015/11/18/looking-to-bone-in-beaune/':
                    print('Processing Exeption + url')
                    exception_multi_wine_regex = re.compile(
                        r"""<p>.*?(?=<span)(.*?)<\/strong>(.*?)(<br>|<br\/>)(.*?)<\/p>""",
                        re.M | re.S | re.I)
                    wines = exception_multi_wine_regex.findall(str(article))
                    Command.create_multi_wines(wines, url, article, tags)

            else:
                print("Processing: " + url)
                # Figure out if single or multi wine post by searching for tasting note
                tasting_search = re.compile(r"(tasting.note)", re.M | re.I)
                is_single_wine = tasting_search.findall(str(article))

                if url in multi_wine_list:
                    is_single_wine = False

                if url in single_wine_list:
                    is_single_wine = True

                if is_single_wine:
                    # Single wine post
                    print("Single wine")

                    # Work out the title
                    h2_title = soup.find('h2', class_='eltdf-post-title')
                    title_regex = re.compile(r""":(.*)""")  # Regex for Witty Title : Wine Name
                    alt_regex = re.compile(r""">(.*)</h2>""", re.M | re.S)  # Regex for title that is just wine.
                    title = title_regex.findall(str(h2_title))  # Try first regex.
                    if not title:
                        # If that's failed try alternative regex
                        title = alt_regex.findall(str(h2_title))
                        if not title:
                            # Last resort, title unknown
                            # title = 'Unknown'
                            print("Couldn't determine title 2!")
                            continue
                        else:
                            title = title[0]
                    else:
                        title = title[0]
                    title = strip_tags(title).strip()  # Strip any leftover

                    # Regex out the wine info
                    single_wine_regex = re.compile(r"""<strong>(.*?)<\/strong>(.*?)(?=<)""", re.M | re.S)
                    wine = single_wine_regex.findall(str(article))
                    Command.create_single_wine(wine, title, url, article, tags)

                else:
                    print("Multi wine")
                    # Multi wine post
                    multi_wine_regex = re.compile(
                        r"""<p><(.*?)<\/strong>(.*?)(<br>|<br\/>)(.*?)<\/p>""", # todo sean: this needs to change
                        re.M | re.S | re.I)
                    wines = multi_wine_regex.findall(str(article))
                    Command.create_multi_wines(wines, url, article, tags)
